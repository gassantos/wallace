from datetime import datetime

class ResultsLogger(object):
    def __init__(self, settings, model_tracking):
        self.settings = settings
        self.model_tracking = model_tracking

    def write_results(self, results_filename=None):
        message_list = [
                self.print_header() + "\n\n",
                self.print_dataset_source(),
                self.print_best_models(),
                self.print_settings()
                ]
        message = "\n".join(message_list)

        if results_filename == None:
            results_filename = self.settings.get("optimization_algorithm_tracking.final_results_filename")

        with open(results_filename, 'w+') as f:
            f.write(message)

    def print_header(self):
        return "Wallace Optimization Results - %s\n" % datetime.now().isoformat()

    def print_dataset_source(self):
        if self.settings.has("dataset.dataset_filename"):
            return "Dataset Source: '%s'" % self.settings.get("dataset.dataset_filename")
        else:
            return ""

    def print_settings(self):
        setting_strings = []
        for setting_name, value in self.settings.iteritems():
            setting_strings.append("%s: %s" % (setting_name, value))
        return "\n".join(setting_strings)

    def print_best_models(self, number=1):
        best_models = self.model_tracking.best_models()[:number]
        descriptions = []
        for i in xrange(len(best_models)):
            model, fitness = best_models[i]

            model_description = "\n".join([
                                "Model Rank: %s" % str(i+1),
                                "Model Fitness: %s" % fitness,
                                "Model Name: %s" % model.model_name(),
                                "Model Dependent Variable: %s" % model.dependent_variable.variable,
                                "Model Independent Variables: %s" % ", ".join([var.variable for var in model.independent_variables]),
                                "Model Parameters: %s" % model.get_parameters()
                                ])
            descriptions.append(model_description)

        return "\n".join(descriptions)