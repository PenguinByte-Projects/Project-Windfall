import argparse
import json
import os
import subprocess
import shutil
import tempfile
import argparse
import json
import os
import subprocess
import shutil
import tempfile

def install_package(package_name):
    package_dir = f"/packages/{package_name}"
    if not os.path.exists(package_dir):
        print(f"Package {package_name} not found.")
        return

    with open(f"{package_dir}/package.json") as f:
        package_info = json.load(f)

    for dependency in package_info.get('dependencies', []):
        install_package(dependency)

    # Check if 'install_script' key exists in package_info
    if 'install_script' not in package_info:
        print(f"No install script specified for package {package_name}.")
        return

    install_script = package_info['install_script']
    # Create a temporary file and open it in nano for editing
    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as temp_file:
        temp_file.write(open(f"{package_dir}/{install_script}", 'r').read())
        temp_file.flush()
        subprocess.call(['nano', temp_file.name])
        # Ask the user if they are happy with their changes
        user_confirmation = input("Are you happy with your changes? (yes/no): ")
        if user_confirmation.lower() == 'yes':
            # Proceed with the installation, passing the path to package.json and package directory
            result = subprocess.run(f"{package_dir}/{install_script} {package_dir}/package.json {package_dir}", shell=True)
        else:
            print("Installation cancelled by the user.")
            return

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
