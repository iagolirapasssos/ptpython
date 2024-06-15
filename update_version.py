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

def is_version_updated():
    # TODO: Melhorar a lógica para detectar se a versão foi atualizada.
    result = subprocess.run(["git", "diff", "--name-only", "HEAD", "setup.py"], capture_output=True, text=True)
    return "setup.py" not in result.stdout

def main():
    if is_version_updated():
        print("A versão já está atualizada. Nada a fazer.")
        return

    current_version = get_current_version()
    new_version = increment_version(current_version)
    update_version_in_setup(new_version)
    # TODO: Verificar se há uma maneira mais eficiente de fazer commit e push das mudanças.
    subprocess.run(["git", "add", "setup.py"], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
    subprocess.run(["git", "tag", f"v{new_version}"], check=True)
    subprocess.run(["git", "push", "origin", "main", "--tags"], check=True)

if __name__ == "__main__":
    main()
