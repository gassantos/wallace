import random

from wallace.predictive_models.predictive_model import PredictiveModel
from wallace.parameters import ParameterSet, ParametersGeneralValidityCheck
from wallace.weighted_selection import WeightedSelection

class PredictiveModelGenerator(object):
    def __init__(self, settings, default_validity_check=None):
        self.settings = settings
        self.model_types = {}
        self.default_validity_check = default_validity_check
        self.weighted_selection = WeightedSelection()

    def set_model_types(self, model_klasses_and_probabilities):
        weighted_selection_hash = {}
        for model_klass, weight in model_klasses_and_probabilities.iteritems():
            model_name, parameter_validity_check = self._get_model_information(model_klass)
            self.model_types[model_name] = {
                    "model_class": model_klass,
                    "parameter_validity_check": parameter_validity_check
                    }
            weighted_selection_hash[model_name] = weight
        self.weighted_selection = WeightedSelection(weighted_selection_hash)

    # TODO: deprecate this along with `add_selection` in `WeightedSelection` class.
    def add_model_type(self, model_klass, parameter_validity_check=None, weight=None):
        model_name, parameter_validity_check = self._get_model_information(model_klass, parameter_validity_check)
        self.model_types[model_name] = {
                "model_class": model_klass,
                "parameter_validity_check": parameter_validity_check
                }
        self.weighted_selection.add_selection(model_name, weight)

    def _get_model_information(self, model_klass, parameter_validity_check=None):
        if not issubclass(model_klass, PredictiveModel):
            raise ValueError("Model types added to the model generator must be subclasses of PredictiveModel.")
        model_name = model_klass.__name__
        if parameter_validity_check == None:
            if self.default_validity_check == None:
                parameter_validity_check = model_klass.validity_check()
            else:
                parameter_validity_check = self.default_validity_check

        return (model_name, parameter_validity_check)

    def increase_weight(self, model_klass, learning_parameter=0.05, taper=True):
        if isinstance(model_klass, PredictiveModel):
            model_name = model_klass.__class__.__name__
        elif issubclass(model_klass, PredictiveModel):
            model_name = model_klass.__name__
        else:
            model_name = model_klass
        self.weighted_selection.increase_weight(model_name, learning_parameter, taper)

    def choose_model_type(self):
        model_name = self.weighted_selection.choose()
        return self.model_types[model_name]

    def get_parameter_set_from_class(self, model_klass):
        model_name = model_klass.__name__
        return self.get_parameter_set(model_name)

    def model_probabilities(self):
        probabilities = {}
        for selection in self.weighted_selection.selections():
            probabilities[selection] = self.weighted_selection.get_probability(selection)
        return probabilities

    def list_model_types(self):
        return self.model_types.values()

    def get_full_validity_check(self):
        full_validity_check = ParametersGeneralValidityCheck()
        for model_name in self.model_types.iterkeys():
            _, validity_check = self._get_parameter_values(model_name)
            full_validity_check.merge(validity_check)

        return full_validity_check

    def get_full_parameter_set(self):
        full_parameter_values = {}
        full_validity_check = ParametersGeneralValidityCheck()
        for model_name in self.model_types.iterkeys():
            parameter_values, validity_check = self._get_parameter_values(model_name)
            full_parameter_values.update(parameter_values)
            full_validity_check.merge(validity_check)

        return ParameterSet(full_parameter_values, validity_check=full_validity_check)

    def get_parameter_set(self, model_name):
        parameter_values, validity_check = self._get_parameter_values(model_name)
        return ParameterSet(parameter_values, validity_check=validity_check)

    def _get_parameter_values(self, model_name):
        if model_name not in self.model_types:
            raise ValueError("Model '%s' is not a valid model type for this model generator." % model_name)

        model_information = self.model_types[model_name]
        validity_check = model_information["parameter_validity_check"]

        parameter_values = {}
        for parameter_name in model_information["model_class"].validity_check().list_parameter_names():
            value = validity_check.get_valid_value(parameter_name)
            parameter_values[parameter_name] = value

        return (parameter_values, validity_check)

