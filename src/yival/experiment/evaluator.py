from typing import List, Union

from ..evaluators.base_evaluator import BaseEvaluator
from ..schemas.evaluator_config import (
    ComparisonEvaluatorConfig,
    EvaluatorConfig,
    EvaluatorOutput,
    EvaluatorType,
)
from ..schemas.experiment_config import Experiment, ExperimentResult


class Evaluator:
    """
    Utility class to evaluate ExperimentResult.
    """

    def __init__(
        self, configs: List[Union[EvaluatorConfig, ComparisonEvaluatorConfig]]
    ):
        self.configs = configs

    def evaluate_individual_result(
        self, result: ExperimentResult
    ) -> List[EvaluatorOutput]:
        res = []
        for config in self.configs:
            config_dict = config.asdict()
            if config_dict["evaluator_type"] == EvaluatorType.INDIVIDUAL.value:
                evaluator_cls = BaseEvaluator.get_evaluator(
                    config_dict["name"]
                )
                if evaluator_cls:
                    config_cls = BaseEvaluator.get_config_class(
                        config_dict["name"]
                    )
                    if config_cls:
                        if isinstance(config_dict, dict):
                            config_data = config_dict
                        else:
                            config_data = config_dict.asdict()
                        config_instance = config_cls(**config_data)
                        evaluator = evaluator_cls(config_instance)
                        res.append(evaluator.evaluate(result))
        return res

    # TODO: Add comaparison evaluator.
    def evaluate_group_result(
        self, results: List[ExperimentResult]
    ) -> List[EvaluatorOutput]:
        return []

    def evaluate_based_on_all_results(
        self, experimnet: List[Experiment]
    ) -> None:

        for config in self.configs:
            config_dict = config.asdict(
            ) if not isinstance(config, dict) else config
            if config_dict["evaluator_type"] == EvaluatorType.ALL.value:

                evaluator_cls = BaseEvaluator.get_evaluator(
                    config_dict["name"]
                )

                if evaluator_cls:
                    config_cls = BaseEvaluator.get_config_class(
                        config_dict["name"]
                    )
                    if config_cls:
                        if isinstance(config_dict, dict):
                            config_data = config_dict
                        else:
                            config_data = config_dict.asdict()

                        config_instance = config_cls(**config_data)
                        evaluator = evaluator_cls(config_instance)

                        evaluator.evaluate_based_on_all_results(experimnet)
