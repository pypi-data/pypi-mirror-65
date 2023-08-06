import numpy as np
from akida import InputConvolutional, ConvolutionMode, PoolingType, BackendType


class InputBCSpike(InputConvolutional):
    """The ``InputBCSpike`` layer is a special type of ``InputConvolutional`` layer
    with pre-defined filters and policies.

    The InputBCSpike layer only accepts 8-bit grayscale images. Images are
    converted to events using proprietary Brainchip convolution filters. In
    order to estimate the number of weights required in the following layer, the
    User must be aware that the output has the same height and width as the
    input image and a feature dimension of size 8.

    """

    def __init__(self, name, input_width, input_height):
        """Create an ``InputBCSpike`` layer from a name and parameters.

        Args:
          name (str): name of the layer.
          input_width (int): input width.
          input_height (int): input height.

        """
        # Call parent constructor to initialize C++ bindings using IputBCSpike
        # predefined parameters
        # Note that we invoke directly __init__ instead of using super, as
        # specified in pybind documentation
        InputConvolutional.__init__(self,
                                    name,
                                    input_width=input_width,
                                    input_height=input_height,
                                    input_channels=1,
                                    kernel_width=5,
                                    kernel_height=5,
                                    convolution_mode=ConvolutionMode.Valid,
                                    stride_x=1,
                                    stride_y=1,
                                    num_neurons=8,
                                    weights_bits=4,
                                    padding_value=0,
                                    activations_enabled=True,
                                    threshold_fire=0,
                                    threshold_fire_step=1,
                                    threshold_fire_bits=1,
                                    pooling_width=-1,
                                    pooling_height=-1,
                                    pooling_type=PoolingType.NoPooling,
                                    pooling_stride_x=-1,
                                    pooling_stride_y=-1)

        # Now load specific weights & set WTA groups
        self.set_variable("weights", InputBCSpike._weights)
        self.set_variable("wta_groups", InputBCSpike._wta_groups)

    # All neurons are in the same WTA group
    _wta_groups = np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    # InputBCSpike weights
    _weights = np.flip(
        np.array(
            [
                [[  # kernel #0
                    [1, 2, 4, 2, 1], [1, 2, 4, 2, 1], [0, 0, 0, 0, 0],
                    [-1, -2, -4, -2, -1], [-1, -2, -4, -2, -1]
                ]],
                [[  # kernel #1
                    [-1, -2, -4, -2, -1], [-1, -2, -4, -2, -1], [0, 0, 0, 0, 0],
                    [1, 2, 4, 2, 1], [1, 2, 4, 2, 1]
                ]],
                [[  # kernel #2
                    [1, 1, 0, -1, -1], [2, 2, 0, -2, -2], [4, 4, 0, -4, -4],
                    [2, 2, 0, -2, -2], [1, 1, 0, -1, -1]
                ]],
                [[  # kernel #3
                    [-1, -1, 0, 1, 1], [-2, -2, 0, 2, 2], [-4, -4, 0, 4, 4],
                    [-2, -2, 0, 2, 2], [-1, -1, 0, 1, 1]
                ]],
                [[  # kernel #4
                    [2, 2, 1, 2, 0], [2, 4, 2, 0, -2], [1, 2, 0, -2, -1],
                    [2, 0, -2, -4, -2], [0, -2, -1, -2, -2]
                ]],
                [[  # kernel #5
                    [-2, -2, -1, -2, 0], [-2, -4, -2, 0, 2], [-1, -2, 0, 2, 1],
                    [-2, 0, 2, 4, 2], [0, 2, 1, 2, 2]
                ]],
                [[  # kernel #6
                    [0, 2, 1, 2, 2], [-2, 0, 2, 4, 2], [-1, -2, 0, 2, 1],
                    [-2, -4, -2, 0, 2], [-2, -2, -1, -2, 0]
                ]],
                [[  # kernel #7
                    [0, -2, -1, -2, -2], [2, 0, -2, -4, -2], [1, 2, 0, -2, -1],
                    [2, 4, 2, 0, -2], [2, 2, 1, 2, 0]
                ]]
            ],
            dtype=np.int8).transpose(),
        axis=(0, 1))
