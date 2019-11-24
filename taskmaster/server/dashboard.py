from taskmaster.common.program import Program


class Dashboard:
    def __init__(self):
        self.programs = {}
        self.pid_procs = {}  # {pid: process}
        self.name_procs = {}  # {name: process}
        self.pid_wexit = []  # tuples returned by waitpid, (pid, exit code)
        self.pid_alive = []
        self.fds_buff = {}

    def init(self, data: dict):
        self.programs = load_programs(data)


def load_programs(data: dict) -> {str: Program}:
    programs = {}
    for prog in data.get('programs'):
        for prog_name, prog_data in prog.items():
            programs[prog_name] = Program(prog_name, prog_data)
    return programs


dashboard = Dashboard()
