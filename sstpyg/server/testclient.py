import cmd
import os
import sys

sys.path.append(os.getcwd())

from sstpyg.server.main import Engine  # noqa


class TestShell(cmd.Cmd):
    intro = 'Test shell para el SSTPyG\n'
    prompt = '>>> '
    engine = Engine()

    def precmd(self, line):
        line = line.lower()
        return line

    def do_exit(self, arg):
        print("Chau")
        return True
    do_eof = do_exit

    # -- commands

    def do_galaxy(self, arg):
        self.engine.cmd_galaxy()


if __name__ == '__main__':
    TestShell().cmdloop()
