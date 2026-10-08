import os
import sys
import subprocess

current_dir = os.path.dirname(os.path.abspath(__file__))
sub_project_dir = os.path.join(current_dir, "RecruitFlow")
venv_python = os.path.join(sub_project_dir, ".venv", "Scripts", "python.exe")
inner_main = os.path.join(sub_project_dir, "main.py")

if os.path.exists(venv_python) and os.path.abspath(sys.executable) != os.path.abspath(venv_python):
    sys.exit(subprocess.call([venv_python, inner_main] + sys.argv[1:], cwd=sub_project_dir))
else:
    sys.path.insert(0, sub_project_dir)
    os.chdir(sub_project_dir)
    from dotenv import load_dotenv
    load_dotenv(os.path.join(sub_project_dir, ".env"))
    from app import create_app
    app = create_app()
    if __name__ == "__main__":
        app.run(debug=True)
