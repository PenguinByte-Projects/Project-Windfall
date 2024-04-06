import argparse
import json
import os
import subprocess
import shutil

def install_package(package_name):
    package_dir = f"/packages/{package_name}"
    if not os.path.exists(package_dir):
        print(f"Package {package_name} not found.")
        return

    with open(f"{package_dir}/package.json") as f:
        package_info = json.load(f)

    for dependency in package_info.get('dependencies', []):
        install_package(dependency)

    install_script = package_info['install_script']
    result = subprocess.run(f"{package_dir}/{install_script}", shell=True)

    if result.returncode == 0:
        installed_path = package_info.get('installed_path', '')
        if installed_path:
            os.environ['PATH'] += os.pathsep + installed_path
            print(f"Successfully added {installed_path} to PATH.")
        else:
            print("Installation successful, but 'installed_path' is not specified in package.json.")
    else:
        print(f"Installation of {package_name} failed.")

def uninstall_package(package_name):
    package_dir = f"/packages/{package_name}"
    if not os.path.exists(package_dir):
        print(f"Package {package_name} not found.")
        return

    with open(f"{package_dir}/package.json") as f:
        package_info = json.load(f)

    installed_path = package_info.get('installed_path', '')
    if installed_path:
        # Remove the installed_path from the PATH environment variable
        os.environ['PATH'] = os.pathsep.join(
            [path for path in os.environ['PATH'].split(os.pathsep) if path != installed_path]
        )
        print(f"Removed {installed_path} from PATH.")

        # Delete the installed_path directory
        shutil.rmtree(installed_path, ignore_errors=True)
        print(f"Successfully uninstalled {package_name}.")
    else:
        print("Uninstallation successful, but 'installed_path' is not specified in package.json.")

def main():
    parser = argparse.ArgumentParser(description='Manage packages.')
    parser.add_argument('command', choices=['install', 'uninstall'], help='The command to execute.')
    parser.add_argument('package_name', help='The name of the package to manage.')
    args = parser.parse_args()

    if args.command == 'install':
        install_package(args.package_name)
    elif args.command == 'uninstall':
        uninstall_package(args.package_name)

if __name__ == "__main__":
    main()
