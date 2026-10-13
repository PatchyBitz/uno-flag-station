import os

from SCons.Script import Import

Import("env")
env = globals()["env"]

FLAG_NAMES = ("FLAG1", "FLAG2", "FLAG3", "FLAG4")


def load_env(path):
    values = {}
    try:
        with open(path, encoding="utf-8") as handle:
            for raw in handle:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                line = line.removeprefix("export ")
                key, sep, value = line.partition("=")
                if not sep:
                    continue
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
                    value = value[1:-1]
                values[key.strip()] = value
    except OSError:
        return values
    return values


env_path = os.path.join(env.subst("$PROJECT_DIR"), ".env")
values = load_env(env_path)

defines = []
blinks = values.get("BLINKS")
if blinks:
    defines.append(("BLINKS", int(blinks)))

for name in FLAG_NAMES:
    value = values.get(name)
    if value:
        defines.append((name, env.StringifyMacro(value)))

if defines:
    env.Append(CPPDEFINES=defines)
