import os, json
from typing import List
from StepRabbit.Program import Program
from StepRabbit.Caller import Caller
from tinydb import TinyDB, Query  # type: ignore
from tinydb.storages import JSONStorage  # type: ignore

# type: ignore

import datetime


class ProgramsManager:
    def __init__(self, host: str, programs_directory: str, executions_db_file: str):
        self.programs_directory = programs_directory
        self.programs: List[Program] = []
        self.simply_programs: List = []
        self.host = host
        self.caller = Caller(host)
        self.reload()
        self.db = TinyDB(executions_db_file)
        self.datetime_format = "%m/%d/%Y, %H:%M:%S"

    def add(self, program_path):
        program = Program(program_path, len(self.programs))
        self.programs.append(program)
        self.simply_programs.append({"name": program.name, "id": program.id})

    def reload(self, id=None):
        if id == None:
            self.programs = []
            self.simply_programs = []
            index = 0
            for entry in os.listdir(self.programs_directory):
                path = os.path.join(self.programs_directory, entry)
                if os.path.isfile(path):
                    if os.path.splitext(path)[1] == ".json":
                        with open(os.path.join(path)) as f:
                            print("PROGRAM : " + path)
                            data = json.load(f)

                            program = Program(path, index)
                            self.programs.append(program)
                            self.simply_programs.append(
                                {"name": program.name, "id": program.id}
                            )
                            index += 1
        else:
            prog_to_reload = self.get_program_by_id(id)
            new_program = Program(prog_to_reload.file_path, id)
            self.programs[id] = new_program
            self.simply_programs[id] = {"name": new_program.name, "id": new_program.id}

            print("PROGRAM RELOADED !")

    def get_programs(self) -> list:
        return self.programs

    def get_program_by_name(self, name: str) -> Program:
        index = 0
        for program in self.programs:
            if program.name == name:
                return self.programs[index]
        raise KeyError("Il n'existe aucun programme de ce nom")

    def get_program_by_id(self, id: int) -> Program:
        if len(self.programs) > id:
            return self.programs[id]
        raise IndexError("Il n'existe aucun programme possédant cet id")

    def run(self, program: Program, args: dict) -> dict:

        execution_id = self.db.insert(
            {
                "program": program.id,
                "program_name": program.name,
                "status": "pending",
                "date": datetime.datetime.now().strftime(self.datetime_format),
            }
        )

        vars = self.caller.execute(program, args)

        if "error" in vars.values():

            self.db.update({"status": "failed"}, doc_ids=[execution_id])
        else:
            self.db.update({"status": "success"}, doc_ids=[execution_id])

        print(vars)
        return vars

    def toJson(self) -> list:
        json_list = []
        id = 0
        for program in self.programs:
            json_prog = program.toJson()
            json_prog["id"] = id
            json_list.append(json_prog)
            id += 1
        return json_list
