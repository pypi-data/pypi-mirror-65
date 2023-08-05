from typing import List
import os, json

import datetime


class Step:
    def __init__(self, json_step: dict):
        self.name: str = json_step["name"]
        self.inputs: List[str] = json_step["inputs"]
        self.outputs: List[str] = json_step["outputs"]
        self.worker_type: str = json_step["worker_type"]

    def toJson(self) -> dict:
        return {
            "name": self.name,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "worker_type": self.worker_type,
        }


class Script:
    def __init__(self, json_script: dict):
        self.steps: List[Step] = []
        for step in json_script:
            self.steps.append(Step(step))

    def toJson(self) -> list:
        json_steps: List[dict] = []
        for step in self.steps:
            json_steps.append(step.toJson())
        return json_steps


class Program:
    def __init__(self, file_path: str, index: int):
        with open(os.path.join(file_path)) as f:
            self.json_program = json.load(f)
        self.id = index
        self.file_path = file_path
        self.smcat_path = os.path.splitext(file_path)[0] + ".smcat"
        self.svg_path = os.path.splitext(file_path)[0] + ".svg"
        self.reload()

    def reload(self):
        self.name = self.json_program["name"]
        self.script: Script = Script(self.json_program["script"])
        self.generateSmcat()
        self.required_inputs: List[str] = []
        self.get_required_inputs()

    def get_required_inputs(self):
        for step in self.script.steps:
            for input_name in step.inputs:
                if not input_name in self.required_inputs:
                    self.required_inputs.append(input_name)

    def generateSmcat(self):
        instructions = []
        index = 0
        for step in self.script.steps:
            step_name = step.name.replace(" ", "")
            if index == 0:

                instructions.append(("initial => {};").format(step_name))

            if index != 0 and (index) < len(self.script.steps):
                prev_step_name = self.script.steps[index - 1].name.replace(" ", "")
                instructions.append(("{} => {};").format(prev_step_name, step_name))
            if (index + 1) >= len(self.script.steps):
                instructions.append(("{} => final;").format(step_name))
            index += 1

        open(self.smcat_path, "w").write(("\n").join(instructions))
        os.system("smcat " + self.smcat_path)

    def toJson(self) -> dict:
        return {"name": self.name, "script": self.script.toJson()}

    def getSvg(self):
        return open(self.svg_path, "rb").read()

    def update(self, new_json):
        open(self.file_path, "w").write(new_json)
        # self.reload()
