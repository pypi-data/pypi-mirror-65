# -*- coding: utf-8 -*-
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : March 2020
| Copyright           : © 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
|
| This file is part of the QGIS Neural Network MLP Classifier plugin and mlp-image-classifier python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License along with Foobar.  If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingContext,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterFileDestination)

from lnns.in_out import run_algorithm_images, tuple_int


class NeuralNetworkProcessingAlgorithm(QgsProcessingAlgorithm):
    """
    The Neural Network Algorithm create a neural network using the sklearn.neural_network.MLPClassifier.
    The network can be used to predict classified images using supervised classification.
    """

    # Constants used to refer to parameters and outputs.
    # They will be used when calling the algorithm from another algorithm, or when calling from the QGIS console.
    INPUT = 'INPUT'
    TRAINING = 'TRAINING'
    HIDDEN_LAYERS = 'HIDDEN_LAYERS'
    ITERATIONS = 'ITERATIONS'
    NO_DATA = 'NO_DATA'
    TEST_SIZE = 'TEST_SIZE'
    ACTIVATION = 'ACTIVATION'
    ACTIVATIONS = ['logistic', 'identity', 'tanh', 'relu']
    PROBABILITY_CLASS = 'PROBABILITY_CLASS'
    PLOT = 'PLOT'
    OUTPUT = 'OUTPUT'

    @staticmethod
    def tr(string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return NeuralNetworkProcessingAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This string should be: fixed for the algorithm;
        not localised; unique within each provider; lowercase alphanumeric char only; no spaces or other formatting char
        """
        return 'lumos:mlpclassifier'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Neural Network MLPClassifier')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside the Processing toolbox.
        """
        return QIcon(':/lumos')

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string should provide a basic description about
        what the algorithm does and the parameters and outputs associated with it.
        """
        return self.tr(
            "Predict classified images using supervised classification (MLPClassifier by sklearn). \n"
            "Image: Raster file to be classified with at least 2 bands.\n"
            "Training image: Raster file with area's of known class for training.\n"
            "No data value: Value that describes pixels with no known class in the training image.\n"
            "Number of hidden neurons: Comma separated values. The ith element represents the number of neurons in "
            "the ith hidden layer.\n"
            "Maximum number of iterations: Number of iterations when training the neural network.\n"
            "Test size: Proportion of training pixels that will be used to evaluate the trained network.\n"
            "Activation function: Function for the hidden layer. "
            "IDENTITY: no-op activation, useful to implement linear bottleneck, returns f(x) = x; "
            "LOGISTIC: logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)); "
            "TANH: hyperbolic tan function, returns f(x) = tanh(x); "
            "RELU: rectified linear unit function, returns f(x) = max(0, x).\n"
            "Predict probability of selected class: instead of classifying the image, "
            "for each image pixel predict the probability of finding this class.\n"
            "Plot file: Set path [.PNG] if you would like an image with the plot of the training progress.\n"
            "Output file: Set path for saving the classified output image to file.\n"
            "Sklearn MLPClassifier also used the following input: the seed used by the random number generator is 100;"
            "a constant learning rate; 0 tolerance for optimization"
        )

    def initAlgorithm(self, configuration, p_str=None, Any=None, *args, **kwargs):
        """
        Here we define the inputs and output of the algorithm, along with some other properties.
        """

        # We add the input image
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT,
                self.tr('Image'),
                'TIFF files (*.tiff)'
            )
        )

        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.TRAINING,
                self.tr('Training image'),
                'TIFF files (*.tiff)'
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.NO_DATA,
                self.tr('No data value'),
                type=0,  # type=1 is Double, 0 is int
                defaultValue=-1
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.HIDDEN_LAYERS,
                self.tr("Number of hidden neurons for each layer (separated by comma's)"),
                defaultValue='10,'
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.ITERATIONS,
                self.tr('Maximum number of iterations'),
                type=0,  # type=1 is Double, 0 is int
                defaultValue=200,
                minValue=1,
                maxValue=1000000000
            )
        )

        param_test_size = QgsProcessingParameterNumber(
            self.TEST_SIZE,
            self.tr('Test size'),
            type=1,  # type=1 is Double, 0 is int
            defaultValue=0.33,
            minValue=0.00,
            maxValue=1.00
        )
        param_test_size.setMetadata({'widget_wrapper': {'decimals': 2}})
        self.addParameter(param_test_size)

        self.addParameter(
            QgsProcessingParameterEnum(
                self.ACTIVATION,
                self.tr('Activation function'),
                options=self.ACTIVATIONS,
                defaultValue=0
            )
        )

        self.addParameter(
            QgsProcessingParameterNumber(
                self.PROBABILITY_CLASS,
                self.tr('Predict probability of a selected class'),
                type=0,  # type=1 is Double, 0 is int
                optional=True
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.PLOT,
                self.tr('Plot file'),
                'PNG files (*.png)',
                optional=True,
                createByDefault=False
            )
        )

        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr('Output file'),
                'TIFF files (*.tiff)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        # Read input values
        probability_of_class = self.parameterAsInt(parameters, self.PROBABILITY_CLASS, context) \
            if parameters[self.PROBABILITY_CLASS] is not None else None

        # run LNNS
        result_path = run_algorithm_images(
            image_paths=[self.parameterAsRasterLayer(parameters, self.INPUT, context).source()],
            hidden_layer_size=tuple_int(self.parameterAsString(parameters, self.HIDDEN_LAYERS, context)),
            iterations=self.parameterAsInt(parameters, self.ITERATIONS, context),
            activation=self.ACTIVATIONS[self.parameterAsInt(parameters, self.ACTIVATION, context)],
            classified_path=self.parameterAsRasterLayer(parameters, self.TRAINING, context).source(),
            no_data_value=self.parameterAsInt(parameters, self.NO_DATA, context),
            test_size=self.parameterAsDouble(parameters, self.TEST_SIZE, context),
            probability_of_class=probability_of_class,
            update_process_bar=feedback.setProgress,
            log_function=feedback.pushInfo,
            output_path=self.parameterAsFileOutput(parameters, self.OUTPUT, context),
            plot_path=self.parameterAsFileOutput(parameters, self.PLOT, context),
            feedback=feedback,
            context=context
        )

        # Return outputs
        output = {self.OUTPUT: result_path}
        context.addLayerToLoadOnCompletion(
            result_path,
            QgsProcessingContext.LayerDetails(name='Classified', project=context.project()))

        return output
