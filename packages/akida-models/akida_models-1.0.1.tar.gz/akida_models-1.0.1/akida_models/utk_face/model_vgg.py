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

import os

from tensorflow.keras import Model
from tensorflow.keras.layers import Dropout, Flatten, Input
from tensorflow.keras.utils import get_file

from ..quantization_blocks import conv_block, dense_block

BASE_WEIGHT_PATH = 'http://data.brainchip.com/models/vgg/'


def vgg_utk_face(input_shape,
                 weights=None,
                 weight_quantization=0,
                 activ_quantization=0,
                 input_weight_quantization=None):
    """Instantiates a VGG-like model for the regression example on age
    estimation using UTKFace dataset.

    Args:
        input_shape (tuple): input shape tuple of the model
        weights (str): one of `None` (random initialization), 'utkface' for
            pretrained weights or the path to the weights file to be loaded.
        weight_quantization (int): sets all weights in the model to have
            a particular quantization bitwidth except for the weights in the
            first layer.

            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.
        activ_quantization: sets all activations in the model to have a
            particular activation quantization bitwidth.

            * '0' implements floating point 32-bit activations.
            * '1' through '8' implements n-bit weights where n is from 1-8 bits.
        input_weight_quantization: sets weight quantization in the first layer.
            Defaults to weight_quantization value.

            * 'None' implements the same bitwidth as the other weights.
            * '0' implements floating point 32-bit weights.
            * '2' through '8' implements n-bit weights where n is from 2-8 bits.

    Returns
        tf.keras.model: a quantized Keras model for VGG/UTKFace
    """
    # Overrides input weight quantization if None
    if input_weight_quantization is None:
        input_weight_quantization = weight_quantization

    # Check weights
    if not (weights in {None, 'utkface'} or os.path.exists(weights)):
        raise ValueError('The `weights` argument should be either '
                         '`None` (random initialization) '
                         'or `utkface` to load weights over http '
                         'or the path to the weights file to be loaded.')

    # Check if UTKFace pretrained weights are compatible with given arguments
    if weights == 'utkface':
        quant_params = (weight_quantization, activ_quantization,
                        input_weight_quantization)
        if quant_params != (2, 2, 8):
            raise ValueError(
                "If 'weights' is 'utkface', quantization parameters "
                "(weight_quantization, activ_quantization, "
                " input_weight_quantization) must be (2, 2, 8); "
                f" got quantization parameters={quant_params}")
        if input_shape != (32, 32, 3):
            raise ValueError("If 'weights' is 'utkface', input shape must be "
                             f" (32,32,3) ; got input_shape={input_shape}")

    img_input = Input(shape=input_shape)

    x = conv_block(img_input,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_0',
                   use_bias=False,
                   add_batchnorm=True,
                   weight_quantization=input_weight_quantization,
                   activ_quantization=activ_quantization)

    x = conv_block(x,
                   filters=32,
                   kernel_size=(3, 3),
                   name='conv_1',
                   padding='same',
                   pooling='max',
                   pool_size=2,
                   use_bias=False,
                   add_batchnorm=True,
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization)

    x = Dropout(0.3)(x)

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_2',
                   use_bias=False,
                   add_batchnorm=True,
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization)

    x = conv_block(x,
                   filters=64,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_3',
                   pooling='max',
                   pool_size=2,
                   use_bias=False,
                   add_batchnorm=True,
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization)

    x = Dropout(0.3)(x)

    x = conv_block(x,
                   filters=84,
                   kernel_size=(3, 3),
                   padding='same',
                   name='conv_4',
                   use_bias=False,
                   add_batchnorm=True,
                   weight_quantization=weight_quantization,
                   activ_quantization=activ_quantization)

    x = Dropout(0.3)(x)
    x = Flatten()(x)

    x = dense_block(x,
                    units=64,
                    name='dense_1',
                    use_bias=False,
                    add_batchnorm=True,
                    weight_quantization=weight_quantization,
                    activ_quantization=activ_quantization)

    x = dense_block(x,
                    units=1,
                    name='dense_2',
                    weight_quantization=weight_quantization,
                    activ_quantization=None)

    model = Model(img_input, x, name='vgg_utk_face')

    # Load weights.
    if weights == 'utkface':
        model_name = (f'vgg_utk_face_wq{weight_quantization}'
                      f'_aq{activ_quantization}'
                      f'_iq{input_weight_quantization}.hdf5')
        weights_path = get_file(fname=model_name,
                                origin=BASE_WEIGHT_PATH + model_name,
                                cache_subdir='models')
        model.load_weights(weights_path)
    elif weights is not None:
        model.load_weights(weights)

    return model
