from typing import Callable

from jkg_evaluators.core import CasePerformance, CompleteEvaluation, EvalCase


class BasicEggCase(EvalCase):

    performance_bigger_better = False
    main_complexity_var = "max_floor"

    def __init__(self, max_floor: int, egg_count: int, floor_count: int):
        self.max_floor = max_floor
        self.egg_count = egg_count
        self.floor_count = floor_count
        self.attempts = 0
        self.broken_eggs = 0
        self.attempted_after_ran_out = False

    def _evaluate(self, solution: Callable) -> CasePerformance:

        out = solution(self.throw_attempt)

        is_success = (out == self.max_floor) and (
            not self.attempted_after_ran_out
        )

        return CasePerformance(
            is_successful=is_success, performance=self.attempts
        )

    def throw_attempt(self, k):
        if self.broken_eggs == self.egg_count:
            self.attempted_after_ran_out = True
        self.attempts += 1
        if k <= self.max_floor:
            return False
        else:
            self.broken_eggs += 1
            return True


def get_egg_kwargs():
    return [
        {"egg_count": 2, "floor_count": 100, "max_floor": i}
        for i in range(0, 101)
    ]


eggdrop_100floor_2egg = CompleteEvaluation(
    get_case_kwarg_list=get_egg_kwargs, case=BasicEggCase,
)
