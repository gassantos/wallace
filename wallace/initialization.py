from settings import AbstractSettings
from weighted_selection import WeightedSelection
from dataset import DatasetVariable
from dataset_file_reader import DatasetFileReader
from optimization_algorithms.predictive_model_generator import PredictiveModelGenerator

from wallace.predictive_models.lasso_regression import LassoRegression
from wallace.predictive_models.ols_linear_regression import OLSLinearRegression
from wallace.predictive_models.ridge_regression import RidgeRegression

from wallace.optimization_algorithms.differential_evolution import DifferentialEvolution

class WallaceInitialization(object):

    DEFAULT_PREDICTIVE_MODELS = {
            LassoRegression: None,
            OLSLinearRegression: None,
            RidgeRegression: None
        }

    def __init__(self, settings, models=None):
        if isinstance(settings, AbstractSettings):
            self.settings = settings
        else:
            self.settings = AbstractSettings(settings)
        self.models = models

    def create_predictive_model_generator(self, models=None):
        if models == None:
            models = WeightedSelection(self.DEFAULT_PREDICTIVE_MODELS).normalize_weights()
        elif isinstance(models, list):
            predictive_models = {}
            for model in models:
                predictive_models[model] = None
            models = WeightedSelection(predictive_models).normalize_weights()
        else:
            models = WeightedSelection(models).normalize_weights()

        predictive_model_generator = PredictiveModelGenerator(self.settings)
        for model, weight in models.iteritems():
            predictive_model_generator.add_model_type(model, weight=weight)

        return predictive_model_generator

    def run_differential_evolution(self, dataset, dependent_variable):
        predictive_model_generator = self.create_predictive_model_generator()
        differential_evolution = DifferentialEvolution(dataset, dependent_variable, self.settings, predictive_model_generator)
        differential_evolution.run()

    def read_filename(self, dataset_filename):
        return DatasetFileReader(self.settings, dataset_filename).read()

    @classmethod
    def initialize(klass, settings, dependent_variable, dataset_filename):
        initialization = WallaceInitialization(settings)
        dataset = initialization.read_filename(dataset_filename)
        if not isinstance(dependent_variable, DatasetVariable):
            dependent_variable = DatasetVariable(dependent_variable)

        initialization.run_differential_evolution(dataset, dependent_variable)