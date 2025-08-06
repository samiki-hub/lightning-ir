from ir_datasets.util import GzipExtract

from .ir_datasets_utils import ParquetScoredDocs, register_new_dataset


def register_rank_distillm():

    base_url = "https://zenodo.org/records/15753974/files/"

    dlc_contents = {
        "url": f"{base_url}__rankzephyr-colbert-10000-" "sampled-100__msmarco-passage-train-judged.run?download=1",
        "expected_md5": "49f8dbf2c1ee7a2ca1fe517eda528af6",
        "cache_path": "msmarco-passage/train/rank-distillm-rankzephyr.run",
    }
    register_new_dataset(
        "msmarco-passage/train/rank-distillm-rankzephyr",
        docs="msmarco-passage",
        queries="msmarco-passage/train",
        qrels="msmarco-passage/train",
        scoreddocs=dlc_contents,
    )

    dlc_contents = {
        "url": f"{base_url}__set-encoder-colbert__" "msmarco-passage-train-judged.run.gz?download=1",
        "expected_md5": "1f069d0daa9842a54a858cc660149e1a",
        "cache_path": "msmarco-passage/train/rank-distillm-set-encoder.run",
        "extractors": [GzipExtract],
    }
    register_new_dataset(
        "msmarco-passage/train/rank-distillm-set-encoder",
        docs="msmarco-passage",
        queries="msmarco-passage/train",
        qrels="msmarco-passage/train",
        scoreddocs=dlc_contents,
    )

    dlc_contents = {
        "url": f"{base_url}__monoelectra-colbert__" "msmarco-passage-train-judged.run.gz?download=1",
        "expected_md5": "5abc9a6c2cdf986c0aedcea853f0b34c",
        "cache_path": "msmarco-passage/train/rank-distillm-monoelectra.run",
        "extractors": [GzipExtract],
    }
    register_new_dataset(
        "msmarco-passage/train/rank-distillm-monoelectra",
        docs="msmarco-passage",
        queries="msmarco-passage/train",
        qrels="msmarco-passage/train",
        scoreddocs=dlc_contents,
    )

    dlc_contents = {
        "url": f"{base_url}__colbert__msmarco-passage-train-judged.parquet?download=1",
        "expected_md5": "1e927d52af085516bf5a3de2865809d5",
        "cache_path": "msmarco-passage/train/rank-distillm-colbert.parquet",
    }
    register_new_dataset(
        "msmarco-passage/train/rank-distillm-colbert",
        docs="msmarco-passage",
        queries="msmarco-passage/train",
        qrels="msmarco-passage/train",
        scoreddocs=dlc_contents,
        ScoreddocsType=ParquetScoredDocs,
    )
