from abc import ABC, abstractmethod
from typing import Literal, Tuple

import torch


class LossFunction(ABC):
    @abstractmethod
    def compute_loss(
        self,
        scores: torch.Tensor,
        targets: torch.Tensor,
    ) -> torch.Tensor:
        raise NotImplementedError(
            "LossFunction.compute_loss must be implemented by subclasses"
        )

    def process_targets(
        self, scores: torch.Tensor, targets: torch.Tensor
    ) -> torch.Tensor:
        if targets.ndim > scores.ndim:
            return targets.max(-1).values
        return targets


class IALossFunction(LossFunction):
    def process_targets(self, targets: torch.Tensor) -> torch.Tensor:
        return targets


class PairwiseLossFunction(LossFunction):
    def get_pairwise_idcs(self, targets: torch.Tensor) -> Tuple[torch.Tensor, ...]:
        # pos items are items where label is greater than other label in sample
        return torch.nonzero(targets[..., None] > targets[:, None], as_tuple=True)


class ListwiseLossFunction(LossFunction):
    pass


class MarginMSE(PairwiseLossFunction):
    def __init__(self, margin: float | Literal["scores"] = 1.0):
        self.margin = margin

    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        query_idcs, pos_idcs, neg_idcs = self.get_pairwise_idcs(targets)
        pos = scores[query_idcs, pos_idcs]
        neg = scores[query_idcs, neg_idcs]
        margin = pos - neg
        if isinstance(self.margin, float):
            target_margin = torch.tensor(self.margin, device=scores.device)
        elif self.margin == "scores":
            target_margin = (
                targets[query_idcs, pos_idcs] - targets[query_idcs, neg_idcs]
            )
        else:
            raise ValueError("invalid margin type")
        loss = torch.nn.functional.mse_loss(margin, target_margin.clamp(min=0))
        return loss


class ConstantMarginMSE(MarginMSE):
    def __init__(self, margin: float = 1.0):
        super().__init__(margin)


class SupervisedMarginMSE(MarginMSE):
    def __init__(self):
        super().__init__("scores")


class RankNet(PairwiseLossFunction):
    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        query_idcs, pos_idcs, neg_idcs = self.get_pairwise_idcs(targets)
        pos = scores[query_idcs, pos_idcs]
        neg = scores[query_idcs, neg_idcs]
        margin = pos - neg
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            margin, torch.ones_like(margin)
        )
        return loss


class KLDivergence(ListwiseLossFunction):
    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        scores = torch.nn.functional.log_softmax(scores, dim=-1)
        targets = torch.nn.functional.log_softmax(targets.to(scores), dim=-1)
        loss = torch.nn.functional.kl_div(scores, targets, log_target=True)
        return loss


class LocalizedContrastiveEstimation(ListwiseLossFunction):
    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        targets = targets.argmax(dim=1)
        loss = torch.nn.functional.cross_entropy(scores, targets)
        return loss


class ApproxLossFunction(ListwiseLossFunction):
    def __init__(self, temperature: float = 1) -> None:
        super().__init__()
        self.temperature = temperature

    @staticmethod
    def get_approx_ranks(scores: torch.Tensor, temperature: float) -> torch.Tensor:
        score_diff = scores[:, None] - scores[..., None]
        normalized_score_diff = torch.sigmoid(score_diff / temperature)
        # set diagonal to 0
        normalized_score_diff = normalized_score_diff * (
            1 - torch.eye(scores.shape[1], device=scores.device)
        )
        approx_ranks = normalized_score_diff.sum(-1) + 1
        return approx_ranks


class ApproxNDCG(ApproxLossFunction):
    def __init__(self, temperature: float = 1, scale_gains: bool = True):
        super().__init__(temperature)
        self.scale_gains = scale_gains

    @staticmethod
    def get_dcg(
        ranks: torch.Tensor,
        targets: torch.Tensor,
        k: int | None = None,
        scale_gains: bool = True,
    ) -> torch.Tensor:
        log_ranks = torch.log2(1 + ranks)
        discounts = 1 / log_ranks
        if scale_gains:
            gains = 2**targets - 1
        else:
            gains = targets
        dcgs = gains * discounts
        if k is not None:
            dcgs = dcgs.masked_fill(ranks > k, 0)
        return dcgs.sum(dim=-1)

    @staticmethod
    def get_ndcg(
        ranks: torch.Tensor,
        targets: torch.Tensor,
        k: int | None = None,
        scale_gains: bool = True,
        optimal_targets: torch.Tensor | None = None,
    ) -> torch.Tensor:
        targets = targets.clamp(min=0)
        if optimal_targets is None:
            optimal_targets = targets
        optimal_ranks = torch.argsort(torch.argsort(optimal_targets, descending=True))
        optimal_ranks = optimal_ranks + 1
        dcg = ApproxNDCG.get_dcg(ranks, targets, k, scale_gains)
        idcg = ApproxNDCG.get_dcg(optimal_ranks, optimal_targets, k, scale_gains)
        ndcg = dcg / (idcg.clamp(min=1e-12))
        return ndcg

    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        approx_ranks = self.get_approx_ranks(scores, self.temperature)
        ndcg = self.get_ndcg(
            approx_ranks, targets, k=None, scale_gains=self.scale_gains
        )
        loss = 1 - ndcg
        return loss.mean()


class ApproxMRR(ApproxLossFunction):
    def __init__(self, temperature: float = 1):
        super().__init__(temperature)

    @staticmethod
    def get_mrr(
        ranks: torch.Tensor, targets: torch.Tensor, k: int | None = None
    ) -> torch.Tensor:
        targets = targets.clamp(None, 1)
        reciprocal_ranks = 1 / ranks
        mrr = reciprocal_ranks * targets
        if k is not None:
            mrr = mrr.masked_fill(ranks > k, 0)
        mrr = mrr.max(dim=-1)[0]
        return mrr

    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        approx_ranks = self.get_approx_ranks(scores, self.temperature)
        mrr = self.get_mrr(approx_ranks, targets, k=None)
        loss = 1 - mrr
        return loss.mean()


class ApproxRankMSE(ApproxLossFunction):
    def __init__(
        self,
        temperature: float = 1,
        discount: Literal["log2", "reciprocal"] | None = None,
    ):
        super().__init__(temperature)
        self.discount = discount

    def compute_loss(self, scores: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        targets = self.process_targets(scores, targets)
        approx_ranks = self.get_approx_ranks(scores, self.temperature)
        ranks = torch.argsort(torch.argsort(targets, descending=True)) + 1
        loss = torch.nn.functional.mse_loss(
            approx_ranks, ranks.to(approx_ranks), reduction="none"
        )
        if self.discount == "log2":
            weight = 1 / torch.log2(ranks + 1)
        elif self.discount == "reciprocal":
            weight = 1 / ranks
        else:
            weight = 1
        loss = loss * weight
        loss = loss.mean()
        return loss


class NeuralLossFunction(ListwiseLossFunction):
    # TODO add neural loss functions

    def __init__(
        self, temperature: float = 1, tol: float = 1e-5, max_iter: int = 50
    ) -> None:
        super().__init__()
        self.temperature = temperature
        self.tol = tol
        self.max_iter = max_iter

    def neural_sort(self, scores: torch.Tensor) -> torch.Tensor:
        # https://github.com/ermongroup/neuralsort/blob/master/pytorch/neuralsort.py
        scores = scores.unsqueeze(-1)
        dim = scores.shape[1]
        one = torch.ones((dim, 1), device=scores.device)

        A_scores = torch.abs(scores - scores.permute(0, 2, 1))
        B = torch.matmul(A_scores, torch.matmul(one, torch.transpose(one, 0, 1)))
        scaling = dim + 1 - 2 * (torch.arange(dim, device=scores.device) + 1)
        C = torch.matmul(scores, scaling.to(scores).unsqueeze(0))

        P_max = (C - B).permute(0, 2, 1)
        P_hat = torch.nn.functional.softmax(P_max / self.temperature, dim=-1)

        P_hat = self.sinkhorn_scaling(P_hat)

        return P_hat

    def sinkhorn_scaling(self, mat: torch.Tensor) -> torch.Tensor:
        # https://github.com/allegro/allRank/blob/master/allrank/models/losses/loss_utils.py#L8
        idx = 0
        while True:
            if (
                torch.max(torch.abs(mat.sum(dim=2) - 1.0)) < self.tol
                and torch.max(torch.abs(mat.sum(dim=1) - 1.0)) < self.tol
            ) or idx > self.max_iter:
                break
            mat = mat / mat.sum(dim=1, keepdim=True).clamp(min=1e-12)
            mat = mat / mat.sum(dim=2, keepdim=True).clamp(min=1e-12)
            idx += 1

        return mat

    def get_sorted_targets(
        self, scores: torch.Tensor, targets: torch.Tensor
    ) -> torch.Tensor:
        permutation_matrix = self.neural_sort(scores)
        pred_sorted_targets = torch.matmul(
            permutation_matrix, targets[..., None].to(permutation_matrix)
        ).squeeze(-1)
        return pred_sorted_targets


class InBatchLossFunction(LossFunction):
    def __init__(
        self,
        pos_sampling_technique: Literal["all", "first"] = "all",
        neg_sampling_technique: Literal["all", "first"] = "all",
    ):
        super().__init__()
        self.pos_sampling_technique = pos_sampling_technique
        self.neg_sampling_technique = neg_sampling_technique

    def get_ib_masks(
        self, batch_size: int, depth: int
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        min_idx = torch.arange(batch_size)[:, None] * depth
        max_idx = min_idx + depth
        if self.pos_sampling_technique == "all":
            pos_mask = torch.arange(batch_size * depth)[None].greater_equal(
                min_idx
            ) & torch.arange(batch_size * depth)[None].less(max_idx)
        elif self.pos_sampling_technique == "first":
            pos_mask = torch.arange(batch_size * depth)[None].eq(min_idx)
        else:
            raise ValueError("invalid pos sampling technique")
        if self.neg_sampling_technique == "all":
            neg_mask = torch.arange(batch_size * depth)[None].less(
                min_idx
            ) | torch.arange(batch_size * depth)[None].greater_equal(max_idx)
        elif self.neg_sampling_technique == "first":
            neg_mask = torch.arange(batch_size * depth)[None, None].eq(min_idx).any(
                1
            ) & torch.arange(batch_size * depth)[None].ne(min_idx)
        else:
            raise ValueError("invalid neg sampling technique")
        return pos_mask, neg_mask

    def compute_loss(self, scores: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError(
            "InBatchLossFunction.compute_loss must be implemented by subclasses"
        )


class InBatchCrossEntropy(InBatchLossFunction):
    def compute_loss(self, scores: torch.Tensor) -> torch.Tensor:
        targets = torch.zeros(scores.shape[0], dtype=torch.long, device=scores.device)
        loss = torch.nn.functional.cross_entropy(scores, targets)
        return loss
