import cmd
import os

class TaskmasterShell(cmd.Cmd):
    intro = 'Welcome to the taskmaster shell.   Type help or ? to list commands.\n'
    prompt = '(taskmaster)$> '

    def default(self, line):
        print("return value : " + line)

    def do_shell(self, line):
        "Run a shell command"
        print("running shell command:", line)
        output = os.popen(line).read()
        print(output)

    def do_args(self, args):
        print(args)

    def do_bye(self, line):
        "Exit"
        return True

    def do_EOF(self, line):
        "Exit with Ctrl-D"
        return True


if __name__ == '__main__':
    TaskmasterShell().cmdloop()