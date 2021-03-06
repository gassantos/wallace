import sklearn.metrics

class FitnessEvaluationMethod(object):
    @classmethod
    def evaluate_fitness(klass, predicted_results, true_results):
        raise NotImplementedError()

    @classmethod
    def evaluation_type(klass):
        return "minimizer"

##########################
### Regression Metrics ###
##########################

class MeanSquaredError(FitnessEvaluationMethod):
    @classmethod
    def evaluate_fitness(klass, predicted_results, true_results):
        return sklearn.metrics.mean_squared_error(true_results, predicted_results)

class R2Score(FitnessEvaluationMethod):
    @classmethod
    def evaluate_fitness(klass, predicted_results, true_results):
        return sklearn.metrics.r2_score(true_results, predicted_results)

    @classmethod
    def evaluation_type(klass):
        return "maximizer"

class MeanAbsoluteError(FitnessEvaluationMethod):
    @classmethod
    def evaluate_fitness(klass, predicted_results, true_results):
        return sklearn.metrics.mean_absolute_error(true_results, predicted_results)

##############################
### Classification Metrics ###
##############################

class F1Score(FitnessEvaluationMethod):
    @classmethod
    def evaluate_fitness(klass, predicted_results, true_results):
        return sklearn.metrics.f1_score(true_results, predicted_results)

    @classmethod
    def evaluation_type(klass):
        return "maximizer"
