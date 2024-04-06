import json
import os
import subprocess


def install_package(package_name):
    package_dir = f"/packages/{package_name}"
    if not os.path.exists(package_dir):
        print(f"Package {package_name} not found.")
        return

    with open(f"{package_dir}/package.json") as f:
        package_info = json.load(f)

    for dependency in package_info['dependencies']:
        install_package(dependency)

    install_script = package_info['install_script']
    subprocess.run(f"{package_dir}/{install_script}", shell=True)



def main():
    package_name = input("Enter package name: ")
    install_package(package_name)

if __name__ == "__main__":
    main()