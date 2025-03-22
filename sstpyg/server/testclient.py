import cmd
import os
import sys
import pprint

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
        self.engine.command("galaxy")

    def do_fake_srs(self, arg):
        print("==== fake")
        self.engine.cmd_srs()

    def do_srs(self, arg):
        print("==== real")
        self.engine.command("srs")
    def do_state(self, arg):
        pprint.pprint(self.engine.get_state())


if __name__ == '__main__':
    TestShell().cmdloop()
