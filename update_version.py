import re
import subprocess

def get_current_version():
    with open("setup.py", "r") as f:
        content = f.read()
        version_match = re.search(r"version=['\"]([^'\"]*)['\"]", content)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Não foi possível encontrar a versão no setup.py")

def increment_version(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{patch}"

def update_version_in_setup(new_version):
    with open("setup.py", "r") as f:
        content = f.read()
    new_content = re.sub(r"version=['\"]([^'\"]*)['\"]", f"version='{new_version}'", content)
    with open("setup.py", "w") as f:
        f.write(new_content)

def main():
    current_version = get_current_version()
    new_version = increment_version(current_version)
    update_version_in_setup(new_version)
    subprocess.run(["git", "add", "setup.py"])
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"])
    subprocess.run(["git", "tag", f"v{new_version}"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", f"v{new_version}"])

if __name__ == "__main__":
    main()
