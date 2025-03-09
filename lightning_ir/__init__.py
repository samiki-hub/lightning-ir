from transformers import AutoConfig, AutoModel, AutoTokenizer

from ._register_external_models import _register_external_models
from .base import (
    LightningIRClassFactory,
    LightningIRConfig,
    LightningIRConfigClassFactory,
    LightningIRModel,
    LightningIRModelClassFactory,
    LightningIRModule,
    LightningIROutput,
    LightningIRTokenizer,
    LightningIRTokenizerClassFactory,
)
from .bi_encoder import (
    BiEncoderConfig,
    BiEncoderEmbedding,
    BiEncoderModel,
    BiEncoderModule,
    BiEncoderOutput,
    BiEncoderTokenizer,
    ScoringFunction,
)
from .callbacks import IndexCallback, RankCallback, RegisterLocalDatasetCallback, ReRankCallback, SearchCallback
from .cross_encoder import (
    CrossEncoderConfig,
    CrossEncoderModel,
    CrossEncoderModule,
    CrossEncoderOutput,
    CrossEncoderTokenizer,
)
from .data import (
    DocDataset,
    DocSample,
    IndexBatch,
    LightningIRDataModule,
    QueryDataset,
    QuerySample,
    RankBatch,
    RankSample,
    RunDataset,
    SearchBatch,
    TrainBatch,
    TupleDataset,
)
from .data.external_datasets import _register_external_datasets
from .loss import (
    ApproxMRR,
    ApproxNDCG,
    ApproxRankMSE,
    ConstantMarginMSE,
    FLOPSRegularization,
    InBatchCrossEntropy,
    InfoNCE,
    KLDivergence,
    L1Regularization,
    L2Regularization,
    RankNet,
    ScoreBasedInBatchCrossEntropy,
    ScoreBasedInBatchLossFunction,
    SupervisedMarginMSE,
)
from .main import LightningIRTrainer, LightningIRWandbLogger
from .models import (
    ColConfig,
    ColModel,
    SpladeConfig,
    SpladeModel,
    T5CrossEncoderConfig,
    T5CrossEncoderModel,
    T5CrossEncoderTokenizer,
    XTRConfig,
    XTRModel,
)
from .retrieve import (
    FaissFlatIndexConfig,
    FaissFlatIndexer,
    FaissIVFIndexConfig,
    FaissIVFIndexer,
    FaissIVFPQIndexConfig,
    FaissIVFPQIndexer,
    FaissPQIndexConfig,
    FaissPQIndexer,
    FaissSearchConfig,
    FaissSearcher,
    IndexConfig,
    Indexer,
    SearchConfig,
    Searcher,
    SeismicIndexConfig,
    SeismicIndexer,
    SeismicSearchConfig,
    SeismicSearcher,
    TorchDenseIndexConfig,
    TorchDenseIndexer,
    TorchDenseSearchConfig,
    TorchDenseSearcher,
    TorchSparseIndexConfig,
    TorchSparseIndexer,
    TorchSparseSearchConfig,
    TorchSparseSearcher,
)
from .schedulers import (
    ConstantLRSchedulerWithLinearWarmup,
    GenericConstantSchedulerWithLinearWarmup,
    GenericConstantSchedulerWithQuadraticWarmup,
    GenericLinearSchedulerWithLinearWarmup,
    LinearLRSchedulerWithLinearWarmup,
    WarmupLRScheduler,
)

AutoConfig.register(BiEncoderConfig.model_type, BiEncoderConfig)
AutoModel.register(BiEncoderConfig, BiEncoderModel)
AutoTokenizer.register(BiEncoderConfig, BiEncoderTokenizer)
AutoConfig.register(CrossEncoderConfig.model_type, CrossEncoderConfig)
AutoModel.register(CrossEncoderConfig, CrossEncoderModel)
AutoTokenizer.register(CrossEncoderConfig, CrossEncoderTokenizer)
AutoConfig.register(ColConfig.model_type, ColConfig)
AutoModel.register(ColConfig, ColModel)
AutoTokenizer.register(ColConfig, BiEncoderTokenizer)
AutoConfig.register(SpladeConfig.model_type, SpladeConfig)
AutoModel.register(SpladeConfig, SpladeModel)
AutoTokenizer.register(SpladeConfig, BiEncoderTokenizer)
AutoConfig.register(T5CrossEncoderConfig.model_type, T5CrossEncoderConfig)
AutoModel.register(T5CrossEncoderConfig, T5CrossEncoderModel)
AutoTokenizer.register(T5CrossEncoderConfig, T5CrossEncoderTokenizer)
AutoConfig.register(XTRConfig.model_type, XTRConfig)
AutoModel.register(XTRConfig, XTRModel)
AutoTokenizer.register(XTRConfig, BiEncoderTokenizer)

_register_external_models()
_register_external_datasets()

__version__ = "0.0.2"

__all__ = [
    "ApproxMRR",
    "ApproxNDCG",
    "ApproxRankMSE",
    "BiEncoderConfig",
    "BiEncoderEmbedding",
    "BiEncoderModel",
    "BiEncoderModule",
    "BiEncoderOutput",
    "BiEncoderTokenizer",
    "ColConfig",
    "ConstantLRSchedulerWithLinearWarmup",
    "ConstantMarginMSE",
    "CrossEncoderConfig",
    "CrossEncoderModel",
    "CrossEncoderModule",
    "CrossEncoderOutput",
    "CrossEncoderTokenizer",
    "DocDataset",
    "DocSample",
    "FaissFlatIndexConfig",
    "FaissFlatIndexer",
    "FaissIVFIndexConfig",
    "FaissIVFIndexer",
    "FaissIVFPQIndexConfig",
    "FaissIVFPQIndexer",
    "FaissPQIndexConfig",
    "FaissPQIndexer",
    "FaissSearchConfig",
    "FaissSearcher",
    "FLOPSRegularization",
    "GenericConstantSchedulerWithLinearWarmup",
    "GenericConstantSchedulerWithQuadraticWarmup",
    "GenericLinearSchedulerWithLinearWarmup",
    "InBatchCrossEntropy",
    "IndexBatch",
    "IndexCallback",
    "IndexConfig",
    "Indexer",
    "KLDivergence",
    "L1Regularization",
    "L2Regularization",
    "LightningIRClassFactory",
    "LightningIRConfig",
    "LightningIRConfigClassFactory",
    "LightningIRDataModule",
    "LightningIRModel",
    "LightningIRModelClassFactory",
    "LightningIRModule",
    "LightningIROutput",
    "LightningIRTokenizer",
    "LightningIRTokenizerClassFactory",
    "LightningIRTrainer",
    "LightningIRWandbLogger",
    "LinearLRSchedulerWithLinearWarmup",
    "InfoNCE",
    "QueryDataset",
    "QuerySample",
    "RankCallback",
    "RankBatch",
    "RankNet",
    "RankSample",
    "RegisterLocalDatasetCallback",
    "ReRankCallback",
    "RunDataset",
    "ScoreBasedInBatchCrossEntropy",
    "ScoreBasedInBatchLossFunction",
    "ScoringFunction",
    "SearchBatch",
    "SearchCallback",
    "SearchConfig",
    "Searcher",
    "SeismicIndexConfig",
    "SeismicIndexer",
    "SeismicSearchConfig",
    "SeismicSearcher",
    "TorchDenseIndexConfig",
    "TorchDenseIndexer",
    "TorchDenseSearchConfig",
    "TorchDenseSearcher",
    "TorchSparseIndexConfig",
    "TorchSparseIndexer",
    "TorchSparseSearchConfig",
    "TorchSparseSearcher",
    "SupervisedMarginMSE",
    "T5CrossEncoderConfig",
    "T5CrossEncoderModel",
    "T5CrossEncoderTokenizer",
    "TrainBatch",
    "TupleDataset",
    "WarmupLRScheduler",
    "XTRConfig",
    "XTRModel",
]
