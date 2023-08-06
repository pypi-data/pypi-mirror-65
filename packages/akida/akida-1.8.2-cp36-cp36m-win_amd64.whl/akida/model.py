from copy import copy
import numpy as np
import yaml
import os
import warnings

from . import (Sparse, Dense, BackendType, ConvolutionMode, PoolingType,
               LearningType, InputData, InputConvolutional, InputBCSpike,
               FullyConnected, Convolutional, SeparableConvolutional)
from .core import ModelBase, Layer, LayerType
from .parameters_serializer import (deserialize_parameters,
                                    serialize_learning_type)
from .layer_statistics import LayerStatistics
from .observer import Observer
from .compatibility import layer_hardware_incompatibilities


class Model(ModelBase):
    """An Akida neural ``Model``, represented as a hierarchy of layers.

    The ``Model`` class is the main interface to Akida.

    It provides methods to instantiate, train, test and save models.

    """

    def __init__(self, filename=None, backend=BackendType.Software):
        """
        Creates an empty ``Model``, a ``Model`` template from a YAML file,
        or a full ``Model`` from a serialized file.

        Args:
            filename (str, optional): path of the YAML file containing the model
                architecture, or a serialized Model.
                If None, an empty sequential model will be created.
            backend (:obj:`BackendType`, optional): backend to run the model on.

        """
        try:
            if filename is not None:
                # get file extension
                extension = os.path.splitext(filename)[1].lower()
                if extension == ".yml" or extension == ".yaml":
                    ModelBase.__init__(self, backend)
                    self._build_model(filename)
                else:
                    ModelBase.__init__(self, filename, backend)
            else:
                ModelBase.__init__(self, backend)
        except:
            self = None
            raise

    def __repr__(self):
        out_dims = self.output_dims if self.get_layer_count() else []
        data = "<akida.Model, layer_count=" + str(self.get_layer_count())
        data += ", output_dims=" + str(out_dims)
        data += ", backend_type=" + str(self.get_backend_type()) + ">"
        return data

    def get_statistics(self):
        """Get statistics by layer for this network.

        Returns:
            a dictionary of obj:`LayerStatistics` indexed by layer_name.

        """
        self._layers_stats = {}
        for i in range(self.get_layer_count()):
            layer = self.get_layer(i)
            self._layers_stats[layer.name] = self.get_layer_statistics(layer)
        return self._layers_stats

    def _build_model(self, filename):
        """Builds a model from a YAML description file of the layers.

        Args:
            filename (str): path of the YAML file containing the model
                architecture, or a serialized Model.

        """
        # test whether the yml file can be found
        if not os.path.isfile(filename):
            raise ValueError("The ymlfile ({}) could not be found, "
                             "instance not initialised".format(filename))
        # load the file
        yaml_content = yaml.load(open(filename), Loader=yaml.FullLoader)

        if "Layers" not in yaml_content:
            raise ValueError(
                "Invalid model configuration: missing 'Layers' section.")

        layers = yaml_content["Layers"]
        if len(layers) == 0:
            raise ValueError("Empty model configuration.")

        # build and add layers to the model
        for layer_description in layers:
            name = layer_description["Name"]

            # deserialize YAML into a kwargs dict for the layer
            if "Parameters" not in layer_description:
                raise ValueError("Invalid model configuration: "
                                 "missing 'Parameters' section in layer " +
                                 name)
            type, params_dict = deserialize_parameters(
                layer_description["Parameters"])

            # create a layer object from the dict
            layer = None
            if type == "inputData":
                layer = InputData(name, **params_dict)
            elif type == "inputConvolutional":
                layer = InputConvolutional(name, **params_dict)
            elif type == "inputBCSpike":
                layer = InputBCSpike(name, **params_dict)
            elif type == "fullyConnected":
                layer = FullyConnected(name, **params_dict)
            elif type == "convolutional":
                layer = Convolutional(name, **params_dict)
            elif type == "separableConvolutional":
                layer = SeparableConvolutional(name, **params_dict)
            elif type == "depthwiseConvolutional":
                warnings.warn("depthwiseConvolutional layer name is deprecated,"
                              " please use separableConvolutional instead.")
                layer = SeparableConvolutional(name, **params_dict)
            elif type == str():
                raise ValueError("Invalid model configuration: missing"
                                 " 'layerType' parameter in layer " + name)
            else:
                raise ValueError("Invalid model configuration, unknown"
                                 " layerType " + type + " in layer " + name)

            # add the layer
            self.add(layer)

    def predict(self, input, num_classes=None):
        """Returns the model class predictions.

        Forwards an input tensor (images or events) through the model
        and compute predictions based on the neuron id.
        If the number of output neurons is greater than the number of classes,
        the neurons are automatically assigned to a class by dividing their id
        by the number of classes.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        Note that the predictions are based on the activation values of the last
        layer: for most use cases, you may want to disable activations for that
        layer (ie setting ``activations_enabled=False``) to get a better
        accuracy.

        Args:
            input (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray
            num_classes (int, optional): optional parameter (defaults to the
                number of neurons in the last layer).

        Returns:
            :obj:`numpy.ndarray`: an array of shape (n).

        """
        if num_classes is None:
            w, h, f = self.output_dims
            num_classes = f

        if isinstance(input, np.ndarray):
            if input.flags['C_CONTIGUOUS']:
                dense = Dense(input)
            else:
                dense = Dense(np.ascontiguousarray(input))
            labels = super(Model, self).predict(dense, num_classes)
        elif isinstance(input, Sparse):
            labels = super(Model, self).predict(input, num_classes)
        else:
            raise TypeError("predict expects Sparse or numpy array as input")
        return labels

    def fit(self, input, input_labels=None):
        """Trains a set of images or events through the model.

        Trains the model with the specified input tensor.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output tensor is a
        Sparse object.

        If activations are disabled for the last layer, the output tensor is a
        numpy array.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            input (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray
            input_labels (list(int), optional): input labels.
                Must have one label per input, or a single label for all inputs.
                If a label exceeds the defined number of classes, the input will
                be discarded. (Default value = None).

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).
            ValueError: if the input doesn't match the required shape,
                format, etc.

        """
        if input_labels is None:
            input_labels = []
        elif isinstance(input_labels, (int, np.integer)):
            input_labels = [input_labels]
        elif isinstance(input_labels, (list, np.ndarray)):
            if any(not isinstance(x, (int, np.integer)) for x in input_labels):
                raise TypeError("fit expects integer as labels")
        if isinstance(input, Sparse):
            outputs = super(Model, self).fit(input, input_labels)
        elif isinstance(input, np.ndarray):
            if input.flags['C_CONTIGUOUS']:
                dense = Dense(input)
            else:
                dense = Dense(np.ascontiguousarray(input))
            outputs = super(Model, self).fit(dense, input_labels)
        else:
            raise TypeError("fit expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def forward(self, input):
        """Forwards a set of images or events through the model.

        Forwards an input tensor through the model and returns an output tensor.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        If activations are enabled for the last layer, the output tensor is a
        Sparse object.

        If activations are disabled for the last layer, the output tensor is a
        numpy array.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            input (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray

        Returns:
            a numpy array of shape (n, out_w, out_h, out_c).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).
            ValueError: if the input doesn't match the required shape,
                format, etc.

        """
        if isinstance(input, Sparse):
            outputs = super(Model, self).forward(input)
        elif isinstance(input, np.ndarray):
            if input.flags['C_CONTIGUOUS']:
                dense = Dense(input)
            else:
                dense = Dense(np.ascontiguousarray(input))
            outputs = super(Model, self).forward(dense)
        else:
            raise TypeError("forward expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def evaluate(self, input):
        """Evaluates a set of images or events through the model.

        Forwards an input tensor through the model and returns a float array.

        It applies ONLY to models without an activation on the last layer.
        The output values are obtained from the model discrete potentials by
        applying a shift and a scale.

        The expected input tensor dimensions are:

        - n, representing the number of frames or samples,
        - w, representing the width,
        - h, representing the height,
        - c, representing the channel, or more generally the feature.

        If the inputs are events, the input shape must be (n, w, h, c), but if
        the inputs are images (numpy array), their shape must be (n, h, w, c).

        Note: only grayscale (c=1) or RGB (c=3) images (arrays) are supported.

        The output tensor shape is always (n, out_w, out_h, out_c).

        Args:
            input (:obj:`Sparse`,`numpy.ndarray`): a (n, w, h, c) Sparse or a
                (n, h, w, c) numpy.ndarray

        Returns:
           :obj:`numpy.ndarray`: a float array of shape (n, w, h, c).

        Raises:
            TypeError: if the input doesn't have the correct type
                (Sparse, numpy.ndarray).
            RuntimeError: if the model last layer has an activation.
            ValueError: if the input doesn't match the required shape,
                format, or if the model only has an InputData layer.

        """
        if isinstance(input, Sparse):
            outputs = super(Model, self).evaluate(input)
        elif isinstance(input, np.ndarray):
            if input.flags['C_CONTIGUOUS']:
                dense = Dense(input)
            else:
                dense = Dense(np.ascontiguousarray(input))
            outputs = super(Model, self).evaluate(dense)
        else:
            raise TypeError("forward expects Sparse or numpy array as input")
        return outputs.to_numpy()

    def summary(self):
        """Prints a string summary of the model.

        This method prints a summary of the model with details for every layer:

        - name and type in the first column
        - hardware compatibility in the 'HW' column. When the layer is not
          compatible, a list of incompatibilities is given below the summary.
        - input shape
        - output shape
        - kernel shape
        - learning type and number of classes
        - a group of 3 metrics to check for training configuration: number of
          input connections (#InConn) is the input space (or kernel space for
          convolutional layers) for the weights. The number of weights (#Weights)
          is given to check that it is well below the number of input connections
          and threshold fire (ThFire) must be less that the number of weights.

        """
        # Formating of the table
        first_col_width = 23
        hw_col_width = 4
        col_width = 14
        last_col_width = 26
        headers = [
            'Layer (type)', 'HW', 'Input shape', 'Output shape', 'Kernel shape',
            'Learning (#classes)', '#InConn/#Weights/ThFire'
        ]
        simple_sep = "-" * (first_col_width + hw_col_width + col_width *
                            (len(headers) - 4) + 2 * last_col_width)
        double_sep = "=" * (first_col_width + hw_col_width + col_width *
                            (len(headers) - 4) + 2 * last_col_width)
        hardware_compatibility = []

        # Data formating nested function
        def get_column_data(data, col_width):
            """Adds data to the current line string and crop or fill to reach
            column width.

            Args:
                data: data to add.
                col_width (int): column width.

            """
            if len(data) > col_width - 1:
                formatted_data = data[:col_width - 1] + ' '
            else:
                formatted_data = data + ' ' * (col_width - len(data))

            return formatted_data

        # Line printing nested function
        def print_layer(index):
            """Prints a summary line for a given layer.

            Args:
                index (int): index of the Layer.

            """
            layer = self.get_layer(index)
            params_names = dir(layer.parameters)

            # layer name (type)
            current_line = get_column_data(
                "{} ({})".format(
                    layer.name,
                    str(layer.parameters.layer_type).split(".")[-1]),
                first_col_width)

            # hardware compatible
            incompatiblities = layer_hardware_incompatibilities(self, index)
            if incompatiblities:
                current_line += get_column_data("no", hw_col_width)
                hardware_compatibility.append(incompatiblities)
            else:
                current_line += get_column_data("yes", hw_col_width)

            # input shape
            input_dims = layer.input_dims
            num_filters = input_dims[-1]
            current_line += get_column_data(str(input_dims), col_width)

            # output shape
            current_line += get_column_data(str(layer.output_dims), col_width)

            # kernel shape
            if ("kernel_width" in params_names and
                    "kernel_height" in params_names):
                kw = layer.parameters.kernel_width
                kh = layer.parameters.kernel_height
                kernel_data = f"({kw} x {kh} x {num_filters})"
                input_connections = str(kw * kh * num_filters)
            else:
                kernel_data = "N/A"
                input_connections = "N/A"
            current_line += get_column_data(kernel_data, col_width)

            # learning type (#classes)
            if layer.learning is not None:
                learning_type = serialize_learning_type(
                    layer.learning.learning_type)
            else:
                learning_type = "N/A"
            if layer.learning is not None and layer.learning.num_classes > 1:
                current_line += get_column_data(
                    f"{learning_type} " + f"({layer.learning.num_classes})",
                    last_col_width)
            else:
                current_line += get_column_data(f"{learning_type}",
                                                last_col_width)

            # input connections
            if (layer.parameters.layer_type == LayerType.FullyConnected):
                input_connections = str(input_dims[0] * input_dims[1] *
                                        input_dims[2])

            # weights
            if ("weights" in layer.get_variable_names()):
                num_weights_data = np.count_nonzero(
                    layer.get_variable("weights"))
                num_neurons = layer.parameters.num_neurons
                if ("weights_pw" in layer.get_variable_names()):
                    num_weights_data += np.count_nonzero(
                        layer.get_variable("weights_pw"))
                    num_neurons += layer.parameters.num_pointwise_neurons
                num_weights_data //= num_neurons
            else:
                num_weights_data = "N/A"

            # threshold fire
            if "activations_params" in params_names:
                th_fire_data = str(
                    layer.parameters.activations_params.threshold_fire)
            else:
                th_fire_data = "N/A"

            current_line += get_column_data(
                f"{input_connections} / " + f"{str(num_weights_data)} / " +
                f"{th_fire_data}", last_col_width)

            print(current_line)
            print(simple_sep)

        # header
        print(simple_sep)
        current_line = get_column_data(headers[0], first_col_width)
        current_line += get_column_data(headers[1], hw_col_width)
        for h in headers[2:-2]:
            current_line += get_column_data(h, col_width)
        current_line += get_column_data(headers[-2], last_col_width)
        current_line += get_column_data(headers[-1], last_col_width)
        print(current_line)
        print(double_sep)

        #layers
        for i in range(self.get_layer_count()):
            print_layer(i)

        if len(hardware_compatibility):
            if len(hardware_compatibility) == 1:
                print("\nHardware incompatibility:\n")
            else:
                print("\nHardware incompatibilities:\n")

            print("\n".join(hardware_compatibility))

    def get_observer(self, layer):
        """Get the Observer object attached to the specified layer.

        Observers are containers attached to a ``Layer`` that allows to
        retrieve layer output spikes and potentials.

        Args:
            layer (:obj:`Layer`): the layer you want to observe.
        Returns:
            :obj:`Observer`: the observer attached to the layer.

        """
        return Observer(self, layer)

    def get_layer_statistics(self, layer):
        """Get the LayerStatistics object attached to the specified layer.

        LayerStatistics are containers attached to an akida.Layer that allows to
        retrieve layer statistics:

            (average sparsity, number of operations and number of possible
            spikes, row_sparsity).

        Args:
            layer (:obj:'Layer'): layer where you want to obtain the ``LayerStatistics`` object.

        Returns:
            a ``LayerStatistics`` object.

        """
        prev_layer = None
        for i in range(1, self.get_layer_count()):
            if self.get_layer(i).name == layer.name:
                prev_layer = self.get_layer(i - 1)
                break

        return LayerStatistics(self, layer, prev_layer)

    def add_classes(self, num_add_classes):
        """Adds classes to the last layer of the model.

        A model with a compiled last layer is ready to learn using the Akida
        built-in learning algorithm. This function allows to add new classes
        (i.e. new neurons) to the last layer, keeping the previously learned
        neurons.

        Args:
            num_add_classes (int): number of classes to add to the last layer

        Raises:
            RuntimeError: if the last layer is not compiled
        """
        # Get current layer's parameters and variables
        layer = self.get_layer(self.get_layer_count() - 1)
        params = copy(layer.parameters)
        old_num_neurons = params.num_neurons
        learn_params = {
            attr: getattr(layer.learning, attr)
            for attr in dir(layer.learning)
            if not '__' in attr and not 'learning_type' in attr
        }
        if not learn_params:
            raise RuntimeError("'add_classes' function must be called when "
                               "the last layer of the model is compiled.")
        num_nrns_per_class = old_num_neurons // learn_params['num_classes']
        var_names = layer.get_variable_names()
        vars = {var: layer.get_variable(var) for var in var_names}

        # Update parameters for new future layer
        learn_params['num_classes'] += num_add_classes
        params.num_neurons = learn_params['num_classes'] * num_nrns_per_class

        # Replace last layer with new one
        self.pop_layer()
        new_layer = Layer(params, layer.name)
        self.add(new_layer)
        new_layer.compile(**learn_params)

        # Fill variables with previous values
        for var in var_names:
            new_var = new_layer.get_variable(var)
            new_var[..., :old_num_neurons] = vars[var]
            new_layer.set_variable(var, new_var)
