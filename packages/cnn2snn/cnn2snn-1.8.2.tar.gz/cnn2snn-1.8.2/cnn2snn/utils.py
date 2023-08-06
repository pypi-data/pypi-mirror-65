#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************
"""
A set of functions to convert a Keras (tf.keras) model to a new
equivalent model with different characteristics. Then, the new model
can be quantized.

"""
import numpy as np
from tensorflow.keras.layers import InputLayer
from tensorflow.keras.models import Model, load_model
from .quantization_ops import WeightFloat, WeightQuantizer
from .quantization_layers import (QuantizedConv2D, QuantizedDepthwiseConv2D,
                                  QuantizedSeparableConv2D, QuantizedDense,
                                  ActivationDiscreteRelu)


def merge_separable_conv(model):
    """Returns a new model where all depthwise conv2d layers followed by conv2d
    layers are merged into single separable conv layers.

    The new model is strictly equivalent to the previous one.

    Args:
        model (:obj:`tf.keras.Model`): a Keras model.

    Returns:
        :obj:`tf.keras.Model`: a tf.keras.Model.

    """
    # If no layers are Depthwise, there is nothing to be done, return.
    if not any([isinstance(l, QuantizedDepthwiseConv2D) for l in model.layers]):
        return model

    if isinstance(model.layers[0], InputLayer):
        x = model.layers[0].output
        i = 1
    else:
        x = model.layers[0].input
        i = 0
    while i < len(model.layers) - 1:
        layer = model.layers[i]
        next_layer = model.layers[i + 1]

        if isinstance(layer, QuantizedDepthwiseConv2D):
            # Check layers expected order
            if not isinstance(next_layer, QuantizedConv2D):
                raise AttributeError(f"Layer {layer.name} "
                                     "QuantizedDepthwiseConv2D should be "
                                     "followed by QuantizedConv2D layers.")

            if layer.bias is not None:
                raise AttributeError(f"Unsupported bias in "
                                     "QuantizedDepthwiseConv2D Layer "
                                     "{layer.name} ")

            # Get weights and prepare new ones
            dw_weights = layer.get_weights()[0]
            pw_weights = next_layer.get_weights()[0]
            new_weights = [dw_weights, pw_weights]
            if next_layer.use_bias:
                bias = next_layer.get_weights()[1]
                new_weights.append(bias)

            # Create new layer
            new_name = f'{layer.name}_{next_layer.name}'
            new_layer = QuantizedSeparableConv2D(next_layer.filters,
                                                 layer.kernel_size,
                                                 quantizer=layer.quantizer,
                                                 padding=layer.padding,
                                                 use_bias=next_layer.use_bias,
                                                 name=new_name)
            x = new_layer(x)
            new_layer.set_weights(new_weights)
            i = i + 2

        else:
            x = layer(x)
            i = i + 1

    # Add last layer if not done already
    if i == (len(model.layers) - 1):
        if isinstance(model.layers[-1], QuantizedDepthwiseConv2D):
            raise AttributeError(f"Layer {layer.name} "
                                 "QuantizedDepthwiseConv2D should be followed "
                                 "by QuantizedConv2D layers.")
        x = model.layers[-1](x)

    return Model(inputs=model.input, outputs=[x], name=model.name)


def load_quantized_model(filepath, compile=True):
    """Loads a quantized model saved in TF or HDF5 format.

    If the model was compiled and trained before saving, its training state
    will be loaded as well.
    This function is a wrapper of `tf.keras.models.load_model`.

    Args:
        filepath (string): path to the saved model.
        compile (bool): whether to compile the model after loading.

    Returns:
        :obj:`tensorflow.keras.Model`: a Keras model instance.
    """
    custom_objects = {
        'WeightFloat': WeightFloat,
        'WeightQuantizer': WeightQuantizer,
        'QuantizedConv2D': QuantizedConv2D,
        'QuantizedSeparableConv2D': QuantizedSeparableConv2D,
        'QuantizedDense': QuantizedDense,
        'ActivationDiscreteRelu': ActivationDiscreteRelu
    }

    return load_model(filepath, custom_objects, compile)
