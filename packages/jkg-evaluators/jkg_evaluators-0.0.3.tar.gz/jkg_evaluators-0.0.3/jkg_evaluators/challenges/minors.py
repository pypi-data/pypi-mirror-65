from collections import Counter
from typing import Callable

from jkg_evaluators.core import CasePerformance, CompleteEvaluation, EvalCase
from jkg_evaluators.input_kwarg_generators import (
    get_num_lists,
    get_numberlists_with_numbers,
    get_word_lists,
    get_words_with_letter,
)


class IndexWithMostALetters(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_words: list):

        self.list_of_words = list_of_words
        self.n = len(list_of_words)

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = -1
        top_num_as = 0
        for idx, word in enumerate(self.list_of_words):
            act = sum([l.lower() == "a" for l in word])
            if act > top_num_as:
                true_solution = idx
                top_num_as = act

        out = solution(self.list_of_words)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LetterOccurrences(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_words: list, letter: str):

        self.list_of_words = list_of_words
        self.letter = letter

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0
        for word in self.list_of_words:
            if self.letter.lower() in word.lower():
                true_solution += 1

        out = solution(self.list_of_words, self.letter)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class WordWithMostOfLetter(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_words: list, letter: str):

        self.list_of_words = list_of_words
        self.letter = letter

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = ""
        max_num = 0
        for word in self.list_of_words:
            letter_count = sum(
                [ll == self.letter.lower() for ll in word.lower()]
            )
            if letter_count > max_num:
                max_num = letter_count
                true_solution = word

        out = solution(self.list_of_words, self.letter)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LargestMultiple(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        sorted_nums = sorted(self.list_of_numbers)

        out = solution(self.list_of_numbers)

        bot_multi = sorted_nums[-1] * sorted_nums[-2]
        top_multi = sorted_nums[0] * sorted_nums[1]

        if bot_multi > top_multi:
            true_solution = bot_multi
        else:
            true_solution = top_multi

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class SumOfDistinctOddPosInts(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0
        for x in set(self.list_of_numbers):
            if ((x % 2) != 0) and (x > 0):
                true_solution += x

        out = solution(self.list_of_numbers)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LargestAscending(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:
        def check_sorted(num):
            sl = sorted(str(abs(num)))
            return "".join(sl) == str(abs(num))

        filtered = [x for x in self.list_of_numbers if check_sorted(x)]

        try:
            true_solution = max(filtered)
        except ValueError:
            true_solution = 0

        out = solution(self.list_of_numbers)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class SmallestWhereDoubleAlso(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list):

        self.list_of_numbers = list_of_numbers

    def _evaluate(self, solution: Callable) -> CasePerformance:

        filtered = [
            x
            for x in self.list_of_numbers
            if ((x * 2) in self.list_of_numbers)
        ]

        try:
            true_solution = min(filtered)
        except ValueError:
            true_solution = 0

        out = solution(self.list_of_numbers)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LargestEvenDivided(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list, number: int):

        self.list_of_numbers = list_of_numbers
        self.number = number

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = None

        for n in self.list_of_numbers:
            if (n / self.number) % 2 == 0:
                if true_solution is None:
                    true_solution = n
                elif n > true_solution:
                    true_solution = n

        if true_solution is None:
            true_solution = 0

        out = solution(self.list_of_numbers, self.number)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LastWithThreeMultDiff(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_numbers: list, number: int):

        self.list_of_numbers = list_of_numbers
        self.number = number

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = 0

        for n in self.list_of_numbers:
            if (n - self.number) % 3 == 0:
                true_solution = n

        out = solution(self.list_of_numbers, self.number)

        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


class LongestWithThreeSame(EvalCase):
    performance_bigger_better = True

    def __init__(self, list_of_words: list):
        self.list_of_words = list_of_words

    def _evaluate(self, solution: Callable) -> CasePerformance:

        true_solution = ""

        for w in self.list_of_words:
            if (max(Counter(w.lower()).values(), default=0) >= 3) and (
                len(w) > len(true_solution)
            ):
                true_solution = w

        out = solution(self.list_of_words)
        is_success = out == true_solution

        return CasePerformance(
            is_successful=is_success, performance=int(is_success)
        )


string_with_most_a_letters = CompleteEvaluation(
    get_case_kwarg_list=get_word_lists, case=IndexWithMostALetters
)

letter_occurrences = CompleteEvaluation(
    get_case_kwarg_list=get_words_with_letter, case=LetterOccurrences
)

word_with_most_of_letters = CompleteEvaluation(
    get_case_kwarg_list=get_words_with_letter, case=WordWithMostOfLetter
)

largest_multiple = CompleteEvaluation(
    get_case_kwarg_list=get_num_lists, case=LargestMultiple
)

sum_odd_positives = CompleteEvaluation(
    get_case_kwarg_list=get_num_lists, case=SumOfDistinctOddPosInts
)

largest_ascending_num = CompleteEvaluation(
    get_case_kwarg_list=get_num_lists, case=LargestAscending
)

smallest_where_double_also = CompleteEvaluation(
    get_case_kwarg_list=get_num_lists, case=SmallestWhereDoubleAlso
)

largest_even_divided = CompleteEvaluation(
    get_case_kwarg_list=get_numberlists_with_numbers, case=LargestEvenDivided
)

last_with_three_multiple_difference = CompleteEvaluation(
    get_case_kwarg_list=get_numberlists_with_numbers,
    case=LastWithThreeMultDiff,
)

longest_with_three_same_letters = CompleteEvaluation(
    get_case_kwarg_list=get_word_lists, case=LongestWithThreeSame
)
