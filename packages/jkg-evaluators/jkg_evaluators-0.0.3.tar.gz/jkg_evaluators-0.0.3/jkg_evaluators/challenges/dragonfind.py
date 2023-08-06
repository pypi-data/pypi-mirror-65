from typing import Callable

from jkg_evaluators.core import CasePerformance, CompleteEvaluation, EvalCase


class DragonFindCase(EvalCase):
    performance_bigger_better = False
    main_complexity_var = "number_of_cows"

    def __init__(self, number_of_cows: int, dragon_coming_to: int):
        self.number_of_cows = number_of_cows
        self.dragon_coming_to = dragon_coming_to
        self.looks = 0

    def _evaluate(self, solution: Callable) -> CasePerformance:

        out = solution(self.is_dead, self.number_of_cows)

        is_success = out == self.dragon_coming_to

        return CasePerformance(
            is_successful=is_success, performance=self.looks
        )

    def is_dead(self, k):
        self.looks += 1
        return k < self.dragon_coming_to


def get_dragon_kwargs():
    dragon_kwargs_list = []

    for cownum in range(10, 501):
        for _dragon_coming_to in range(1, cownum):
            dragon_kwargs_list.append(
                {
                    "number_of_cows": cownum,
                    "dragon_coming_to": _dragon_coming_to,
                }
            )
    return dragon_kwargs_list


dragonfind_10_to_500 = CompleteEvaluation(
    get_case_kwarg_list=get_dragon_kwargs, case=DragonFindCase
)
