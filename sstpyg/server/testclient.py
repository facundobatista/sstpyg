import cmd

from .main import Engine


class TestShell(cmd.Cmd):
    intro = 'Test shell para el SSTPyG\n'
    prompt = '>>> '
    engine = Engine()

    def precmd(self, line):
        line = line.lower()

    def do_exit(self, arg):
        print("Chau")
        return True
    do_eof = do_exit

    # -- commands

    def do_galaxy(self, arg):
        self.engine.cmd_galaxy()


if __name__ == '__main__':
    TestShell().cmdloop()
