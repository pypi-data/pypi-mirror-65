import json
import os
import random
from typing import Optional

from jkg_evaluators.util import zip_dir


def dump_separated_minor_nb(
    notebook_path: str,
    output_directory: str,
    members: list,
    task_name: str,
    zip_dir_path: Optional[str] = None,
):
    nb_dic = json.load(open(notebook_path))
    cells = nb_dic.pop("cells")
    task_cell_lists = []
    for idx, cell in enumerate(cells):
        if cell["source"][0].startswith("####"):
            start_ind = idx
            end_ind = idx + 4
            task_cell_lists.append(cells[start_ind:end_ind])
    random.shuffle(members)
    os.makedirs(output_directory, exist_ok=True)

    for idx, member in enumerate(members):
        member_path = os.path.join(output_directory, member)
        os.makedirs(member_path, exist_ok=True)
        member_nb_path = os.path.join(
            member_path, "{}.ipynb".format(task_name)
        )
        member_nb = nb_dic.copy()
        member_nb["cells"] = task_cell_lists[idx]
        json.dump(member_nb, open(member_nb_path, "w"))

    if zip_dir_path is not None:
        zip_dir(zip_dir_path, output_directory, task_name)
