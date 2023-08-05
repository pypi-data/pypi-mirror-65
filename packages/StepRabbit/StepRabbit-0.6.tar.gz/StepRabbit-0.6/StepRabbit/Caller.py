from StepRabbit.RabbitClient import RabbitClient
import json
from StepRabbit.Program import Program
from typing import *
from functools import lru_cache


class Caller:
    def __init__(self, host: str):
        self.rabbit = RabbitClient(host)

    def execute(self, program: Program, args) -> dict:
        print("Executing : " + program.name)
        return self.run(program, args)

    @lru_cache(maxsize=0)
    def run(self, program: Program, in_vars) -> dict:
        vars = in_vars
        print("VARS : ")
        print(vars)
        step_index = 0

        for step in program.script.steps:
            exec_vars = []

            print(str(step_index) + " -----> " + step.name)

            for input_name in step.inputs:
                if not input_name in vars.keys():
                    raise ValueError("Value of " + input_name + " not specified")
                else:
                    exec_vars.append(vars[input_name])

            response = self.rabbit.call(exec_vars, step.worker_type)

            output_index = 0
            for output_name in step.outputs:
                print("RESPONSE : ")
                if not response["status"] == "error":

                    vars[output_name] = response["data"][output_index]
                    print(response["data"][output_index])
                else:
                    vars[output_name] = "error"
                output_index += 1
            step_index += 1
        print(vars)
        return vars
