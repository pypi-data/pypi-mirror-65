import os
import tempfile
import subprocess

"""
Bundle all the dependencies in requirements.txt into a tar.bz2 by downloading and 
building wheels for all the dependencies in requirements.txt

See https://pip.pypa.io/en/stable/user_guide/#installation-bundles for details 
"""


def main():
    with tempfile.TemporaryDirectory() as tmpdir:
        if not os.path.exists("requirements.txt"):
            print("Run in a directory with requirements.txt")
            exit(1)
        subprocess.run(
            [
                "pip",
                "wheel",
                "-r",
                "requirements.txt",
                "--build-option",
                "--python-tag=py3",
                "--wheel-dir",
                tmpdir,
            ]
        )
        subprocess.run(["cp", "requirements.txt", tmpdir])
        cwd = os.getcwd()
        os.chdir(tmpdir)
        subprocess.run(["tar", "-cjvf", f"{cwd}/bundle.tar.bz2", *os.listdir(tmpdir)])
        os.chdir(cwd)
