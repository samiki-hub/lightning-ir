from transformers import AutoConfig, AutoModel, AutoTokenizer

from .bi_encoder import BiEncoderConfig, BiEncoderTokenizer
from .cross_encoder import CrossEncoderConfig, CrossEncoderTokenizer
from .models import (
    ColConfig,
    ColModel,
    ColTokenizer,
    DprConfig,
    DprModel,
    MonoConfig,
    MonoModel,
    SetEncoderConfig,
    SetEncoderModel,
    SetEncoderTokenizer,
    SpladeConfig,
    SpladeModel,
)


def _register_internal_models():
    AutoTokenizer.register(BiEncoderConfig, BiEncoderTokenizer)
    AutoTokenizer.register(CrossEncoderConfig, CrossEncoderTokenizer)
    AutoConfig.register(ColConfig.model_type, ColConfig)
    AutoModel.register(ColConfig, ColModel)
    AutoTokenizer.register(ColConfig, ColTokenizer)
    AutoConfig.register(DprConfig.model_type, DprConfig)
    AutoModel.register(DprConfig, DprModel)
    AutoTokenizer.register(DprConfig, BiEncoderTokenizer)
    AutoConfig.register(MonoConfig.model_type, MonoConfig)
    AutoModel.register(MonoConfig, MonoModel)
    AutoTokenizer.register(MonoConfig, CrossEncoderTokenizer)
    AutoConfig.register(SetEncoderConfig.model_type, SetEncoderConfig)
    AutoModel.register(SetEncoderConfig, SetEncoderModel)
    AutoTokenizer.register(SetEncoderConfig, SetEncoderTokenizer)
    AutoConfig.register(SpladeConfig.model_type, SpladeConfig)
    AutoModel.register(SpladeConfig, SpladeModel)
    AutoTokenizer.register(SpladeConfig, BiEncoderTokenizer)
