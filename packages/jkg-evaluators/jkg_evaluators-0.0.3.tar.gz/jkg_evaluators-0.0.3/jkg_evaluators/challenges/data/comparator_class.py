import itertools
import json
import os
import shutil
import subprocess
import time

import numpy as np
import pandas as pd
import yaml


class SolutionComparator:
    def __init__(self, data_sizes, input_sizes, solutions_to_compare="all"):

        if solutions_to_compare == "all":
            self.solutions_to_compare = next(
                os.walk(os.path.join("..", "solutions"))
            )[1]
        elif isinstance(solutions_to_compare, str):
            self.solutions_to_compare = [solutions_to_compare]
        else:
            self.solutions_to_compare = solutions_to_compare

        self.input_dicts = {
            d_size: {isize: self._get_input(isize) for isize in input_sizes}
            for d_size in data_sizes
        }
        self.comparison_data = []
        self._tmp_dir = "tmp"

    def _cleanup(self):
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    @staticmethod
    def _get_input(size):
        return [size]

    @staticmethod
    def _dump_data(size, data_path):
        with open(data_path, "w") as fp:
            fp.write(f"{size} nothing")

    def _try_running_command(
        self, command_dic: dict, command_name: str, act_solution: str
    ):
        command = command_dic.get(command_name)
        if command:
            print(f"running {command_name} for {act_solution}")

            command_start_time = time.time()
            _proc = subprocess.Popen(
                command.split(),
                # stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self._tmp_dir,
            )
            _proc.wait()
            _stdout, _stderr = _proc.communicate()
            command_time = time.time() - command_start_time
            if _proc.returncode != 0:
                self._cleanup()
                print(f"\n\n{act_solution} {command_name} ERROR:\n--")
                print(_stderr.decode("utf-8"))
                raise RuntimeError(_stderr.decode("utf-8"))

        else:
            print(f"no {command_name} for {act_solution}")
            command_time = None

        return command_time

    def run_comparison(self):

        for act_solution in self.solutions_to_compare:
            print(f"solution: {act_solution}")
            self._cleanup()
            act_solution_path = os.path.join("..", "solutions", act_solution)
            shutil.copytree(act_solution_path, self._tmp_dir)
            try:
                commands = yaml.safe_load(
                    open(os.path.join("tmp", "commands.yaml"))
                )
            except FileNotFoundError:
                self._cleanup()
                raise FileNotFoundError(
                    f"no commands.yaml in solution directory: {act_solution}"
                )

            self._try_running_command(
                commands, "setup-env-command", act_solution
            )

            for data_size, input_dict in self.input_dicts.items():

                data_path = os.path.join("data", f"{data_size}.csv")
                shutil.copy(data_path, os.path.join(self._tmp_dir, "data.csv"))

                self._try_running_command(
                    commands, "etl-command", act_solution
                )

                for input_size, input_object in input_dict.items():
                    print(f"input size: {input_size} - data size: {data_size}")

                    json.dump(
                        input_object,
                        open(os.path.join(self._tmp_dir, "inputs.json"), "w"),
                    )

                    calc_time = self._try_running_command(
                        commands, "process-command", act_solution
                    )
                    if calc_time is None:
                        self._cleanup()
                        raise ValueError(
                            "no process-command specified "
                            f"in {act_solution} commands.yaml"
                        )

                    try:
                        output_list = json.load(
                            open(os.path.join(self._tmp_dir, "outputs.json"))
                        )
                    except FileNotFoundError:
                        self._cleanup()
                        raise RuntimeError(
                            f"solution {act_solution} "
                            "did not produce an outputs.json"
                        )

                    self.comparison_data.append(
                        {
                            "calc_time": calc_time,
                            "input_size": input_size,
                            "data_size": data_size,
                            "solution": act_solution,
                            "output_list": output_list.copy(),
                        }
                    )

                self._try_running_command(
                    commands, "cleanup-command", act_solution
                )

        self._cleanup()

    def plot_comparison(self):

        if self.comparison_data:
            pd.DataFrame(self.comparison_data).pivot_table(
                index=["data_size", "input_size"],
                columns="solution",
                values="calc_time",
            ).plot.bar(figsize=(13, 7))
        else:
            print("run the comparison first")

    def output_comparison(self):

        if self.comparison_data:
            return (
                pd.DataFrame(self.comparison_data)
                .groupby("solution")
                .apply(
                    lambda df: pd.DataFrame(
                        itertools.chain(*df["output_list"].tolist())
                    ).reset_index(drop=True)
                )
                .fillna(0)
                .pipe(
                    lambda df: df.reset_index().pivot_table(
                        columns="solution",
                        index=[
                            "level_1",
                            *df.select_dtypes(exclude=np.number).columns,
                        ],
                    )
                )
            )
        else:
            print("run the comparison first")
