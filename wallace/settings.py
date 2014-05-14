from wallace.fitness_evaluation_methods.fitness_evaluation_method import MeanSquaredError

from wallace.dataset_transformations.log_transformation import LogTransformation
from wallace.dataset_transformations.scale_transformation import ScaleTransformation
from wallace.dataset_transformations.sqrt_transformation import SqrtTransformation
from wallace.dataset_transformations.box_cox_transformation import BoxCoxTransformation

class AbstractSettings(object):
    DESCRIPTIONS = {
            "fitness_evaluation.crossfold_partitions": "Default number of partitions (k) to use when doing k-fold cross validation.",
            "fitness_evaluation.evaluation_method": "Default method for evaluating the fitness of a model.",
            "model_tracking.models_to_track": "Specify the number of the best models to return after the run has completed.",
            "optimization_algorithm_tracking.tracking_log_filename": "The file which all tracking on the optimization algorithm will be written to.",
            "dataset.maximum_dataset_size": "When reading in a dataset, this is the maximum number of rows allowed.",
            "dataset.randomize_file_reader": "If a file has more rows than `dataset.maximum_dataset_size` allows, then read in all of rows and randomly choose the rows to keep.",
            "dataset.remove_rows_with_missing_data": "Remove a row if it has missing data.",
            "dataset_transformation.transform_datasets": "Perform the default transformations defined in `dataset_transformations.default_transformations` on a dataset when it is being read into memory.",
            "dataset_transformation.log_transformation_base": "Default base for performing a log transformation.",
            "dataset_transformation.default_transformations": "Transformations to be applied to a dataset automatically if `dataset_transformation.transform_datasets` is True.",
            "differential_evolution.crossover_probability": "The probability of mutating a given value in differential evolution (CR).",
            "differential_evolution.differential_weight": "Used for weighting differences in differential evolution (F).",
            "optimization_algorithm.population_size": "Default number of models in the population for a given step of an optimization algorithm.",
            "independent_variable_selection.initial_independent_variables_percentage": "Percentage of total number of variables to start with when initializing an optimization algorithm."
        }

    DEFAULTS = {
            "fitness_evaluation.crossfold_partitions": 10,
            "fitness_evaluation.evaluation_method": MeanSquaredError,
            "model_tracking.models_to_track": 50,
            "optimization_algorithm_tracking.tracking_log_filename": "logs/optimization_algorithm_logs.log",
            "dataset.maximum_dataset_size": 50000,
            "dataset.randomize_file_reader": False,
            "dataset.remove_rows_with_missing_data": True,
            "dataset_transformation.transform_datasets": False,
            "dataset_transformation.log_transformation_base": 10,
            "dataset_transformation.default_transformations": [LogTransformation, ScaleTransformation, SqrtTransformation, BoxCoxTransformation],
            "differential_evolution.crossover_probability": 0.5,
            "differential_evolution.differential_weight": 0.8,
            "optimization_algorithm.population_size": 40,
            "independent_variable_selection.initial_independent_variables_percentage": 0.25
        }

    def __init__(self, settings=None):
        self.settings = {}
        if settings != None:
            for attribute_name, value in settings.iteritems():
                self.set(attribute_name, value)

    def _resolve_attribute(self, attribute, *args):
        if hasattr(attribute, "__call__"):
            return attribute(*args)
        else:
            return attribute

    def set(self, attribute_name, value):
        self.settings[attribute_name] = value

    def get(self, attribute_name, *args):
        if attribute_name in self.settings:
            return self._resolve_attribute(self.settings[attribute_name], *args)
        elif attribute_name in self.DEFAULTS:
            return self._resolve_attribute(self.DEFAULTS[attribute_name], *args)
        else:
            raise ValueError("Settings have no attribute '%s'" % attribute_name)

    def get_description(self, attribute_name):
        if attribute_name in self.DESCRIPTIONS:
            return self.DESCRIPTIONS[attribute_name]
        else:
            raise ValueError("No description exists for attribute '%s'" % attribute_name)

    def has(self, attribute_name):
        return (attribute_name in self.settings) or (attribute_name in self.DEFAULTS)

    @classmethod
    def set_default(klass, attribute_name, value):
        klass.DEFAULTS[attribute_name] = value
