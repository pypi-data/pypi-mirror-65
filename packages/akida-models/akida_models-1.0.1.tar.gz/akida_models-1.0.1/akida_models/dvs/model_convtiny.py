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

# System imports
import os
import warnings

# Tensorflow/Keras Imports
from tensorflow.keras.utils import get_file
from tensorflow.keras import backend, Model
from tensorflow.keras.layers import (Input, BatchNormalization, MaxPool2D,
                                     GlobalAvgPool2D, Reshape, Dropout,
                                     Activation)

# cnn2snn Imports
from cnn2snn.quantization_ops import WeightQuantizer, WeightFloat
from cnn2snn.quantization_layers import conv2d, separable_conv2d, dense

# Local utils
from ..quantization_blocks import _add_activation_layer, _get_weight_quantizer

# Locally fixed config options
# The number of neurons in the penultimate dense layer
# This layer has binary output spikes, and could be a bottleneck
# if care isn't taken to ensure enough info capacity
NUM_SPIKING_NEURONS = 256

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/convtiny/'


def _depthwise_block(inputs, filters, name, add_maxpool, weight_quantizer,
                     activ_quantization):
    """Returns a depthwise block.

    Args:
        inputs (tuple): 4D tensor previous layer output shape
        filters (int): number of neurons
        name (str): the depthwise block name
        add_maxpool (bool): add MaxPool2D block
        weight_quantizer (int):
        activ_quantization (int): sets all activations in the model

    Returns:
        tuple: the output shape as 4D tensor
    """
    x = separable_conv2d(filters=filters,
                         kernel_size=(3, 3),
                         use_bias=False,
                         padding='same',
                         name=name,
                         modifier=weight_quantizer)(inputs)

    if add_maxpool:
        x = MaxPool2D(pool_size=(2, 2), padding='same',
                      name=name + '_maxpool')(x)
    x = BatchNormalization(name=name + '_BN')(x)
    x = _add_activation_layer(x, activ_quantization, name + '_relu')

    return x


def convtiny_dvs(input_shape,
                 weights=None,
                 classes=None,
                 weight_quantization=0,
                 activ_quantization=0):
    """Instantiates a CNN for the "IBM DVS Gesture" example.

    Args:
        input_shape (tuple): input shape tuple of the model
        weights (str): one of `None` (random initialization), 'dvs_gesture' for
            pretrained weights or the path to the weights file to be loaded.
        classes (int): number of classes to classify images into.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 1-8 bits.

    Returns:
        tf.keras.model: a quantized Keras convolutional model for DVS Gesture.
    """
    # Check weights
    if not (weights in {None, 'dvs_gesture'} or os.path.exists(weights)):
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization) '
                         'or `dvs_gesture` to load weights over http '
                         'or the path to the weights file to be loaded.')

    # Check if dvs_gesture pretrained weights are compatible with given arguments
    if weights == 'dvs_gesture':
        quant_params = (weight_quantization, activ_quantization)
        if quant_params != (2, 4):
            raise ValueError("If 'weights' is 'dvs_gesture', quantization"
                             " parameters (weight_quantization, "
                             " activ_quantization, input_weight_quantization)"
                             " must be (2, 4); "
                             f" got quantization parameters={quant_params}")
        if input_shape != (64, 64, 2):
            raise ValueError(
                "If 'weights' is 'dvs_gesture', input shape must be "
                f" (64,64,2) ; got input_shape={input_shape}")

    img_input = Input(input_shape)

    # Set quantization
    weight_quantizer = _get_weight_quantizer(weight_quantization)

    num_blocks = 4
    x = img_input
    for block in range(num_blocks):
        x = conv2d(filters=16 * 2**block,
                   kernel_size=(3, 3),
                   use_bias=False,
                   strides=(1, 1),
                   padding='same',
                   name='conv_' + str(block),
                   modifier=weight_quantizer)(x)
        if block < (num_blocks - 2):
            x = MaxPool2D(pool_size=(3, 3),
                          padding='same',
                          name='block_' + str(block) + '_maxpool')(x)
        elif block == (num_blocks - 1):
            x = GlobalAvgPool2D(name='global_avg')(x)
        elif block >= (num_blocks - 2):
            x = MaxPool2D(pool_size=(2, 2),
                          padding='same',
                          name='block_' + str(block) + '_maxpool')(x)

        x = BatchNormalization(name='block_' + str(block) + '_BN')(x)
        x = _add_activation_layer(x, activ_quantization,
                                  'block_' + str(block) + '_relu')

    bm_outshape = (1, 1, 128)

    x = Reshape(bm_outshape, name='reshape_1')(x)
    x = Dropout(1e-3, name='dropout')(x)

    aq = 0
    if weight_quantization > 0:
        # Assume that if we're quantizing weights, we want the Spiking Layer to
        # generate spikes
        aq = 1
        # Assume that if we're quantizing weights, we want the Dense layer to
        # be HW compatible, => WQ=2
        fc_weight_quantizer = _get_weight_quantizer(2)
    else:
        aq = activ_quantization
        fc_weight_quantizer = _get_weight_quantizer(weight_quantization)

    x = _depthwise_block(x, NUM_SPIKING_NEURONS, 'spiking_layer', False,
                         weight_quantizer, aq)

    x = dense(classes, modifier=fc_weight_quantizer, use_bias=False)(x)
    x = Activation('softmax', name='act_softmax')(x)
    x = Reshape((classes,), name='reshape_2')(x)

    model = Model(inputs=img_input, outputs=x, name='dvs_network')

    # Load weights.
    if weights == 'dvs_gesture':
        model_name = (f'convtiny_dvs_gesture_wq{weight_quantization}'
                      f'_aq{activ_quantization}.h5')
        weights_path = get_file(fname=model_name,
                                origin=BASE_WEIGHT_PATH + model_name,
                                cache_subdir='models')
        model.load_weights(weights_path)
    elif weights is not None:
        model.load_weights(weights)

    return model
