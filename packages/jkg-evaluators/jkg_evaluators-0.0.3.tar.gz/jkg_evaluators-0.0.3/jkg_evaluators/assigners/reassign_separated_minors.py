import itertools
import json
import os
from typing import Optional

import unidecode

from jkg_evaluators.util import get_code_nb_cell, get_md_nb_cell, zip_dir


def distribute_originals(
    original_directory: str,
    members: list,
    task_name: str,
    collective_task_name: str,
    output_directory: Optional[str] = None,
    zip_dir_path: Optional[str] = None,
):

    if output_directory is None:
        output_directory = original_directory
    os.makedirs(output_directory, exist_ok=True)

    mem_task_dic = {}
    for m in members:
        nb_path = os.path.join(
            original_directory, m, "{}.ipynb".format(task_name)
        )
        with open(nb_path) as fp:
            nb_js = json.load(fp)

        for line in itertools.chain(*[c["source"] for c in nb_js["cells"]]):
            if line.startswith("from jkg_evaluators import"):
                mem_task_dic[m] = line.split()[-1]
                break

    import_file_source = "\n".join(
        [
            "from jkg_evaluators import {} as {}".format(
                task, unidecode.unidecode(m)
            )
            for m, task in mem_task_dic.items()
        ]
    )
    import_file_path = os.path.join(output_directory, "__import_file__.py")

    with open(import_file_path, "w") as fp:
        fp.write(import_file_source)

    member_imports = [
        "from __import_file__ import {}".format(unidecode.unidecode(m))
        for m in members
    ]

    import_cell_source = "\n".join(
        ["import sys", "sys.path.insert(0, '..')", *member_imports]
    )

    all_cells = [get_code_nb_cell(import_cell_source)]

    for m in members:
        all_cells += get_member_task_solution_cells(m)

    nb_js["cells"] = all_cells

    for m in members:
        os.makedirs(os.path.join(output_directory, m), exist_ok=True)
        out_nb_path = os.path.join(
            output_directory, m, "{}.ipynb".format(collective_task_name)
        )
        with open(out_nb_path, "w") as fp:
            json.dump(nb_js, fp)

    if zip_dir_path is not None:
        zip_dir(zip_dir_path, output_directory, collective_task_name)


def get_member_task_solution_cells(m):
    dem = unidecode.unidecode(m)
    return [
        get_md_nb_cell("## {}".format(m)),
        get_code_nb_cell(
            "\n".join(
                [
                    "def {}_solution():".format(dem),
                    "    # modify this function",
                    "    # return value and parameters and all",
                    "    return 0",
                ]
            )
        ),
        get_code_nb_cell("{}.evaluate({}_solution)".format(dem, dem)),
    ]
