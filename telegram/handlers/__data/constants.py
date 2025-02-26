import json
import os


dir_path = os.path.dirname(__file__)

with open(os.path.join(dir_path, "templates.json")) as f:
    TEMPLATES: dict[str, str] = json.load(f)

commands_path = os.path.join(os.path.dirname(dir_path), "commands")
commands_accesses = os.listdir(commands_path)
COMMANDS = {}
for a in commands_accesses:
    p = os.path.join(commands_path, a)
    for c in os.listdir(p):
        if "." not in c and c != "__pycache__":
            with open(os.path.join(p, c, "description.txt")) as f:
                desc = f.read()
            COMMANDS.setdefault(c, {"access_level": int(a[-1]), "description": desc})
