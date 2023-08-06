from akida.core import (Layer, ConvolutionalParams, LearningType,
                        ConvolutionMode, PoolingType, BackendType)
from .parameters_filler import fill_conv_params


class Convolutional(Layer):
    """Convolutional or "weight-sharing" layers are commonly used in visual
    processing. However, the convolution operation is extremely useful in any
    domain where translational invariance is required – that is, where localized
    patterns may be of interest regardless of absolute position within the
    input. The convolution implemented here is typical of that used in visual
    processing, i.e., it is a 2D convolution (across the x- and y-dimensions),
    but a 3D input with a 3D filter. No convolution occurs across the third
    dimension; events from input feature 1 only interact with connections to
    input feature 1 – likewise for input feature 2 and so on. Typically,
    the input feature is the identity of the event-emitting neuron in the
    previous layer.

    Outputs are returned from convolutional layers as a list of events, that is,
    as a triplet of x, y and feature (neuron index) values. Note that for a
    single packet processed, each neuron can only generate a single event at a
    given location, but can generate events at multiple different locations and
    that multiple neurons may all generate events at a single location.

    """

    def __init__(self,
                 name,
                 kernel_width,
                 kernel_height,
                 num_neurons,
                 convolution_mode=ConvolutionMode.Same,
                 weights_bits=1,
                 pooling_width=-1,
                 pooling_height=-1,
                 pooling_type=PoolingType.NoPooling,
                 pooling_stride_x=-1,
                 pooling_stride_y=-1,
                 activations_enabled=True,
                 threshold_fire=0,
                 threshold_fire_step=1,
                 threshold_fire_bits=1):
        """Create a ``Convolutional`` layer from a name and parameters.

        Args:
            name (str): name of the layer.
            kernel_width (int): convolutional kernel width.
            kernel_height (int): convolutional kernel height.
            num_neurons (int): number of neurons (filters).
            convolution_mode (:obj:`ConvolutionMode`, optional): type of convolution.
            weights_bits (int, optional): number of bits used to quantize weights.
            pooling_width (int, optional): pooling window width. If set to -1 it
                will be global.
            pooling_height (int, optional): pooling window height. If set to -1
                it will be global.
            pooling_type (:obj:`PoolingType`, optional): pooling type
                (None, Max or Average).
            pooling_stride_x (int, optional): pooling stride on x dimension.
            pooling_stride_y (int, optional): pooling stride on y dimension.
            activations_enabled (bool, optional): enable or disable activation
                function.
            threshold_fire (int, optional): threshold for neurons to fire or
                generate an event.
            threshold_fire_step (float, optional): length of the potential
                quantization intervals.
            threshold_fire_bits (int, optional): number of bits used to quantize
                the neuron response.

        """
        params = ConvolutionalParams()
        fill_conv_params(params,
                         kernel_width=kernel_width,
                         kernel_height=kernel_height,
                         num_neurons=num_neurons,
                         convolution_mode=convolution_mode,
                         weights_bits=weights_bits,
                         pooling_width=pooling_width,
                         pooling_height=pooling_height,
                         pooling_type=pooling_type,
                         pooling_stride_x=pooling_stride_x,
                         pooling_stride_y=pooling_stride_y,
                         activations_enabled=activations_enabled,
                         threshold_fire=threshold_fire,
                         threshold_fire_step=threshold_fire_step,
                         threshold_fire_bits=threshold_fire_bits)

        # Call parent constructor to initialize C++ bindings
        # Note that we invoke directly __init__ instead of using super, as
        # specified in pybind documentation
        Layer.__init__(self, params, name)
