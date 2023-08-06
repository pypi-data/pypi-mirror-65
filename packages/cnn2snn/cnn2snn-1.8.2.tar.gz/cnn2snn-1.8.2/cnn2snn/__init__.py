# Tensorflow is provided by two packages, tensorflow and tensorflow-gpu.
# This check will check if something is already installed: if that is the case,
# it will just require a given version, otherwise it will throw a RuntimeError
try:
    import tensorflow
    assert int(tensorflow.__version__[0]) >= 2
except:
    raise RuntimeError('cnn2snn requires either tensorflow or tensorflow-gpu '
                       'version >= 2.0 to be installed')

from .utils import merge_separable_conv, load_quantized_model
from .converter import convert
from .mapping_generator import check_model_compatibility
from .quantization_ops import WeightQuantizer, WeightFloat
from .quantization_layers import (QuantizedConv2D, QuantizedDepthwiseConv2D,
                                  QuantizedDense, QuantizedSeparableConv2D,
                                  ActivationDiscreteRelu)
