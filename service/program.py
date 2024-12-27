from models.Program import get_program_by_program_id, get_program_by_program_id_and_department_id


def get_program_info_list(program_id: str):
    programs = get_program_by_program_id(program_id)
    if not programs:
        return False

    return programs


def get_one_program(program_id: str, department_id: str):
    program = get_program_by_program_id_and_department_id(program_id, department_id)
    if not program:
        return False

    return program
