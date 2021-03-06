from taskmaster.common.program import Program


class Dashboard:
    """
    Main data panel which contains all necessary information about:
    programs, created processes, alive processes, alive fds, signaled pid list etc...
    """
    def __init__(self):
        self.programs = {}
        self.pid_procs = {}  # {pid: process}
        self.name_procs = {}  # {name: process}
        self.pid_wexit = []  # tuples returned by waitpid, (pid, exit code)
        self.pid_alive = []
        self.fds_buff = {}
        self.fds_zombie = []
        self.prog_to_remove = []

    def init(self, data: dict):
        self.programs = load_programs(data)


def load_programs(data: dict) -> {str: Program}:
    """\
    This is used for loading configuration data and parsing it into a dict of Program objects.
    :param data: Main configuration dictionary
    :return: a dict of Program objects {program_name: program_object}
    """
    programs = {}
    for prog in data.get('programs'):
        for prog_name, prog_data in prog.items():
            program = Program(prog_name, prog_data)
            if program.is_valid(): # recheck
                programs[prog_name] = program
    return programs


dashboard = Dashboard()
