__version__ = '0.1.0'
import uuid
import random
from subprocess import Popen, PIPE, STDOUT
from plumbum import local
from IPython import embed
import pathlib

class Brish:

    # MARKER = str(uuid.uuid4())
    MARKER = '\x00'
    MLEN = len(MARKER)

    def __init__(self, defaultShell=None):
        self.defaultShell = defaultShell or pathlib.Path(__file__).parent / 'brish.zsh'
        self.p = None

    def init(shell=defaultShell):
        self.p = Popen(shell, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                universal_newlines=True) # decode output as utf-8, newline is '\n'

    def send_cmd(cmd):
        if self.p is None:
            init()
        print(cmd + MARKER, file=self.p.stdin, flush=True)
        stdout = ""
        for line in iter(self.p.stdout.readline, MARKER+'\n'):
            if line.endswith(MARKER+'\n'):
                line = line[:-MLEN-1]
            stdout += line
        return_code = int(self.p.stdout.readline())
        stderr = ""
        for line in iter(self.p.stderr.readline, MARKER+'\n'):
            if line.endswith(MARKER+'\n'):
                line = line[:-MLEN-1]
            stderr += line

        return (return_code, stdout, stderr)

    def cleanup():
        if self.p is None:
            return
        self.p.stdout.close()
        if self.p.stderr:
            self.p.stderr.close()
        self.p.stdin.close()
        self.p.wait()
        self.p = None
