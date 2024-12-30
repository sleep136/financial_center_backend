from models.Program import get_program_by_program_id, get_program_by_program_id_and_department_id
from pydantic import BaseModel

def get_program_info_list(program_id: str):
    programs = get_program_by_program_id(program_id)
    if not programs:
        return False
    list_programs = []
    for program in programs:
        list_programs.append(Program(program_name=program.xmmc, program_id=program.xmbh,department_id=program.bmbh))

    return list_programs


def get_one_program(program_id: str, department_id: str):
    program = get_program_by_program_id_and_department_id(program_id, department_id)
    if not program:
        return False

    return Program(program_name=program.xmmc, program_id=program.xmbh,department_id=program.bmbh)


class Program(BaseModel):
    program_name: str
    program_id: str
    department_id: str

