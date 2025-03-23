#!/usr/bin/fades

import asyncio
import os
import sys
import pprint

from prompt_toolkit import PromptSession  # fades
from prompt_toolkit.patch_stdout import patch_stdout

sys.path.append(os.getcwd())

from sstpyg.server.main import Engine  # noqa


class AsyncCmd:
    def __init__(self):
        self.prompt_session = PromptSession(self.prompt)

    async def run(self):
        print(self.intro)
        with patch_stdout():
            await asyncio.create_task(self._handle_user_input())

    def _exit(self):
        if self.prompt_session.app.is_running:
            self.prompt_session.app.exit()

    async def _handle_user_input(self):
        while True:
            try:
                user_input = await self.prompt_session.prompt_async()
            except EOFError:
                cmd = "eof"
                rest = ""
            else:
                parts = user_input.split(maxsplit=1)
                match parts:
                    case []:
                        continue
                    case [cmd]:
                        rest = ""
                    case [cmd, rest]:
                        pass
                    case _:
                        raise ValueError("impossible?")

            func_name = "do_" + cmd.lower()
            func = getattr(self, func_name, None)
            if func is None:
                print("Error: command not found")
            else:
                should_exit = await func(rest)
                if should_exit:
                    return self._exit()


class TestShell(AsyncCmd):
    intro = 'Test shell para el SSTPyG\n'
    prompt = '>>> '
    engine = Engine()

    async def do_exit(self, arg):
        print("Chau")
        return True
    do_eof = do_exit

    async def run(self):
        await self.engine.init()
        await super().run()

    # -- commands

    async def do_galaxy(self, arg):
        if not arg:
            print("Error, usage: galaxy x y")
            return

        coords = tuple(map(int, arg.split()))
        quad = await self.engine.get_galaxy(coords)
        quad.show()

    async def do_srs(self, arg):
        quad = await self.engine.command("srs")
        quad.show()

    async def do_lrs(self, arg):
        data = await self.engine.command("lrs")
        pprint.pprint(data)

    async def do_state(self, arg):
        state = await self.engine.get_state()
        pprint.pprint(state)


if __name__ == "__main__":
    client = TestShell()
    asyncio.run(client.run())
