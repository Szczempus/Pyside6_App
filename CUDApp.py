import sys
import os
import subprocess

if __name__ == "__main__":
    print(sys.platform)
    cwd = os.getcwd()
    env = cwd + r"\environment\env\python.exe"
    app = cwd + r"\app\main.py"
    subprocess.Popen([env, app])
