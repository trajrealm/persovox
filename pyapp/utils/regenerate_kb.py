import os
import subprocess
import sys
import traceback


def run_regenerate_kb(username: str, files: list) -> bool:
    script_path = os.path.join("pyapp", "services", "resume_processor.py")
    root_path = os.path.abspath(".")
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{root_path}:{env.get('PYTHONPATH', '')}"
    try:
        result = subprocess.run(
            [
                sys.executable,
                script_path,
                username,
                str(files)
            ],
            env=env,
            check=True,
            capture_output=True,
            text=True
        )
        print("Subprocess Output:", result.stdout)
        print("Subprocess stderr:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        traceback.print_exc()
        print("Subprocess Error:", e.stderr)
        return False
