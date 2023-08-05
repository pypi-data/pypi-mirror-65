import subprocess


class Command:

    @staticmethod
    def execute(params):
        command = subprocess.run(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return command.returncode, command.stdout or command.stderr
