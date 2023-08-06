import akida.core as ak


def fill_num_neurons_params(params, params_dict):
    params.num_neurons = params_dict["num_neurons"]
    if params.num_neurons == 0:
        raise ValueError("Parameter num_neurons cannot be 0")


def fill_weights_bits_params(params, params_dict):
    if params_dict["weights_bits"] > 8:
        raise ValueError(
            "The maximum number of bits for quantized weights is 8.")
    if params_dict["weights_bits"] < 1:
        raise ValueError(
            "The minimum number of bits for quantized weights is 1.")
    params.weights_bits = params_dict["weights_bits"]


def fill_activations_params(params, params_dict):
    if params_dict['threshold_fire_bits'] not in range(1, 5):
        raise ValueError("threshold_fire_bits must be an integer between "
                         "1 and 4. Receives threshold_fire_bits="
                         f"{params_dict['threshold_fire_bits']}")
    params.activations_params.activations_enabled = params_dict[
        "activations_enabled"]
    params.activations_params.threshold_fire = params_dict["threshold_fire"]
    params.activations_params.threshold_fire_step = params_dict[
        "threshold_fire_step"]
    if params.activations_params.threshold_fire_step <= 0:
        raise ValueError("Parameter threshold_fire_step cannot be <= 0")
    params.activations_params.threshold_fire_bits = params_dict[
        "threshold_fire_bits"]


def fill_convolution_kernel_params(params, params_dict):
    params.kernel_width = params_dict["kernel_width"]
    params.kernel_height = params_dict["kernel_height"]
    params.convolution_mode = params_dict["convolution_mode"]
    if params.kernel_width <= 0:
        raise ValueError("Parameter kernel_width cannot be <= 0")
    elif params.kernel_height <= 0:
        raise ValueError("Parameter kernel_height cannot be <= 0")
    if params.kernel_width % 2 == 0:
        raise ValueError("Parameter kernel_width cannot be even")
    elif params.kernel_height % 2 == 0:
        raise ValueError("Parameter kernel_height cannot be even")


def fill_input_params(params, params_dict):
    params.input_width = params_dict["input_width"]
    params.input_height = params_dict["input_height"]
    if params.input_width == 0:
        raise ValueError("Parameter input_width cannot be 0")
    elif params.input_height == 0:
        raise ValueError("Parameter input_height cannot be 0")


def fill_pooling_params(params, params_dict):
    params.pooling_width = params_dict["pooling_width"]
    params.pooling_height = params_dict["pooling_height"]
    params.pooling_type = params_dict["pooling_type"]
    params.pooling_stride_x = params_dict["pooling_stride_x"]
    params.pooling_stride_y = params_dict["pooling_stride_y"]
    if params.pooling_width == 0:
        raise ValueError("Parameter pooling_width cannot be 0")
    elif params.pooling_height == 0:
        raise ValueError("Parameter pooling_height cannot be 0")
    if (params.pooling_width != -1 and params.pooling_height != -1 and
            params.pooling_type == ak.PoolingType.NoPooling):
        raise ValueError(
            "Incoherent pooling parameters: cannot have pooling_width or "
            "pooling_height > 0 while pooling_type is set to "
            "PoolingType.NoPooling")
    if params.pooling_stride_x == 0:
        raise ValueError("Parameter pooling_stride_x cannot be 0")
    elif params.pooling_stride_y == 0:
        raise ValueError("Parameter pooling_stride_y cannot be 0")
    if params.pooling_stride_x < 0:
        params.pooling_stride_x = params.pooling_width
    if params.pooling_stride_y < 0:
        params.pooling_stride_y = params.pooling_height


def fill_input_data_params(params, **params_dict):
    fill_input_params(params, params_dict)
    params.input_channels = params_dict["input_channels"]
    if params.input_channels == 0:
        raise ValueError("Parameter input_channels cannot be 0")


def fill_stride_params(params, params_dict):
    params.stride_x = params_dict["stride_x"]
    params.stride_y = params_dict["stride_y"]
    if params.stride_x < 1:
        raise ValueError("stride_x must be positive")
    elif params.stride_y < 1:
        raise ValueError("stride_y must be positive")


def fill_data_processing_params(params, params_dict):
    fill_num_neurons_params(params, params_dict)
    fill_weights_bits_params(params, params_dict)
    fill_activations_params(params, params_dict)


def fill_fully_connected_params(params, **params_dict):
    fill_data_processing_params(params, params_dict)


def fill_conv_params(params, **params_dict):
    fill_data_processing_params(params, params_dict)
    fill_convolution_kernel_params(params, params_dict)
    fill_pooling_params(params, params_dict)


def fill_separable_conv_params(params, **params_dict):
    fill_conv_params(params, **params_dict)
    params.num_pointwise_neurons = params_dict["num_pointwise_neurons"]
    if params.num_pointwise_neurons == 0:
        raise ValueError("Parameter num_pointwise_neurons cannot be 0")


def fill_input_conv_params(params, **params_dict):
    fill_input_params(params, params_dict)
    fill_convolution_kernel_params(params, params_dict)
    fill_stride_params(params, params_dict)
    fill_num_neurons_params(params, params_dict)
    fill_weights_bits_params(params, params_dict)
    fill_pooling_params(params, params_dict)
    fill_activations_params(params, params_dict)
    params.input_channels = params_dict["input_channels"]
    params.padding_value = params_dict["padding_value"]
