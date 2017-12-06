import collections
import os.path
import re
import sys


class Cmd:
    def __init__(self, index, count, cmd):
        self.index = index
        self.count = count
        self.cmd = cmd


class BrainfuckModule:
    def __init__(self, source):
        self._source = source
        self._program = self._tokenize(source)

    @staticmethod
    def _tokenize(source):
        program = [
            Cmd(i, len(match[0]), match[0][0])
            for i, match in enumerate(re.finditer(r"(([<>,.+-])\2*)|[\[\]]", source))
        ]
        stack = collections.deque()
        for cmd in program:
            if cmd.cmd == '[':
                stack.append(cmd)
            elif cmd.cmd == ']':
                opener = stack.pop()
                opener.jmp = cmd.index
                cmd.jmp = opener.index
        return program

    def get_ints(self, input=''):
        input_data = (
            ord(c) if isinstance(c, (str, bytes)) else c
            for c in input
        )
        cmd_head = 0
        tape = [0]
        tape_head = 0
        program_length = len(self._program)
        while cmd_head < program_length:
            cmd = self._program[cmd_head]
            cmd_head += 1

            if cmd.cmd == '[':
                if not tape[tape_head]:
                    cmd_head = cmd.jmp + 1
            elif cmd.cmd == ']':
                cmd_head = cmd.jmp
            elif cmd.cmd == ',':
                for _ in range(cmd.count):
                    char = next(input_data, 0)
                    tape[tape_head] = char
            elif cmd.cmd == '.':
                for _ in range(cmd.count):
                    yield tape[tape_head]
            elif cmd.cmd == '+':
                tape[tape_head] += cmd.count
            elif cmd.cmd == '-':
                tape[tape_head] -= cmd.count
            elif cmd.cmd == '<':
                tape_head -= cmd.count
                if tape_head < 0:
                    tape = [0] * -tape_head + tape
                    tape_head = 0
            elif cmd.cmd == '>':
                tape_head += cmd.count
                cells_to_add = tape_head - len(tape) + 1
                if cells_to_add > 0:
                    tape.extend(0 for _ in range(cells_to_add))

    def get_string(self, input=''):
        return ''.join(map(chr, self.get_ints(input)))


def get_bf_path(directory, name):
    bf_path = os.path.join(directory, f'{name}.bf')
    if os.path.isfile(bf_path):
        return bf_path


class BrainfuckLoader:
    def __init__(self, path):
        self._path = path

    @classmethod
    def find_module(cls, name, path=None):
        for d in sys.path:
            bf_path = get_bf_path(d, name)
            if bf_path is not None:
                return cls(bf_path)

        if path is not None:
            name = name.rsplit('.', 1)[-1]
            for d in path:
                bf_path = get_bf_path(d, name)
                if bf_path is not None:
                    return cls(bf_path)

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]

        try:
            with open(self._path) as f:
                mod = BrainfuckModule(f.read())
        except:
            raise ImportError(f"Could not open {self._path}")

        mod.__file__ = self._path
        mod.__loader__ = self
        sys.modules[name] = mod
        return mod
