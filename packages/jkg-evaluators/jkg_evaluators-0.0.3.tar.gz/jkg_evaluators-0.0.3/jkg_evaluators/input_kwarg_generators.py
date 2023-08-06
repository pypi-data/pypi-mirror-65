import random
import string
from typing import List


def get_word_lists() -> List[dict]:
    word_lists = [
        {"list_of_words": ["b", "bb", "bBb"]},
        {"list_of_words": ["aa", "aaa", "aa", "a"]},
        {"list_of_words": ["ba", "babab", "AaAaA", "Ahha"]},
        {"list_of_words": ["123", "lala", "", "", "", "aA"]},
    ]
    random.seed(42069)
    for _r in range(10, 501):
        word_lists.append(
            {
                "list_of_words": [
                    "".join(
                        random.choices(
                            string.ascii_letters + string.digits,
                            k=random.randint(0, 120),
                        )
                    )
                    for _ in range(_r)
                ]
            }
        )
    return word_lists


def get_num_lists() -> List[dict]:

    num_lists = [
        {"list_of_numbers": [0, 1, 2, 3, 4]},
        {"list_of_numbers": [0, 0, 10, 3, 10]},
        {"list_of_numbers": [-20, -40, 0, 1, 2, 3, 40]},
        {"list_of_numbers": [-1100, 100, 20]},
        {"list_of_numbers": [0, 1]},
        {"list_of_numbers": [21, 120, 220]},
    ]

    random.seed(42069)
    for _r in range(10, 501):

        num_lists.append(
            {
                "list_of_numbers": [
                    random.randint(-1000, 1000) for _ in range(_r)
                ]
            }
        )

    return num_lists


def get_words_with_letter() -> List[dict]:
    word_lists = get_word_lists()
    return [
        {"letter": random.choice(string.ascii_letters), **kwargs}
        for kwargs in word_lists
    ]


def get_numberlists_with_numbers() -> List[dict]:
    num_lists = get_num_lists()
    return [
        {"number": random.randint(1, 10), **kwargs} for kwargs in num_lists
    ]
