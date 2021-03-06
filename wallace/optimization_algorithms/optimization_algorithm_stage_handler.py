from wallace.interval_storage import IntervalStorage
from wallace.optimization_algorithms.stage.optimization_algorithm_stage import OptimizationAlgorithmStage

class OptimizationAlgorithmStageHandler(object):
    def __init__(self, settings, stages=None):
        self.settings = settings

        if stages == None:
            stages = self.settings.get("optimization_algorithm.default_stages")

        for key in stages.iterkeys():
            if not issubclass(key, OptimizationAlgorithmStage):
                raise ValueError("OptimizationAlgorithmStageHandler must contain OptimizationAlgorithmStage subclasses.")

        self.stage_storage = IntervalStorage(stages)
        self.stages_used = []

    def add_stage(self, stage, start_percentage, end_percentage):
        self.stage_storage.add_interval(stage, start_percentage, end_percentage)

    def has_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.has_entry(step_percentage)

    def get_stage(self, current_step, total_steps=None):
        step_percentage = self._get_step_percentage(current_step, total_steps)
        return self.stage_storage.get_entry(step_percentage)

    # TODO: its possible that an optimization step won't get run if stage == None and
    # on_step doesn't run. Need some way to fix that.
    def run_stage(self, current_step, total_steps=None, payload=None):
        stage = None
        if self.has_stage(current_step, total_steps):
            stage = self.get_stage(current_step, total_steps)

        # If we've started using a new stage, check to see if we have to run the
        # `after_stage` method.
        if (stage == None) or not self._is_used_stage(stage):
            if len(self.stages_used) > 0:
                last_stage, has_run_after_stage = self.stages_used[-1]
                if not has_run_after_stage:
                    last_stage(self.settings).after_stage(payload)
                    self.stages_used[-1] = (last_stage, True)

        # If this is the first time we've seen the stage, then run the `before_stage`
        # method
        if (stage != None) and not self._is_used_stage(stage):
            stage(self.settings).before_stage(payload)
            self.stages_used.append((stage, False))

        # Run the stage if it exists
        if stage != None:
            stage(self.settings).on_step(payload=payload)

        # If this is the last step, then we need to run the after_stage
        total_steps = self._get_total_steps(total_steps)
        if stage != None and (current_step >= total_steps - 1):
            print "Running after stage"
            stage(self.settings).after_stage(payload)

    def _is_used_stage(self, stage):
        for used_stage, _ in self.stages_used:
            if stage == used_stage:
                return True
        return False

    def _get_step_percentage(self, current_step, total_steps=None):
        total_steps = self._get_total_steps(total_steps)
        return float(current_step) / total_steps

    def _get_total_steps(self, total_steps=None):
        if total_steps == None:
            return self.settings.get("optimization_algorithm.finishing_criteria.max_steps")
        else:
            return total_steps

