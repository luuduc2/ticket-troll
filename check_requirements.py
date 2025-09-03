import subprocess
import sys
import importlib

def check_and_install_requirements():
    # Read requirements from requirements.txt
    with open('requirements.txt', 'r') as file:
        requirements = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    
    # Filter out built-in modules
    built_in_modules = ['tkinter', 'datetime', 'threading']
    pip_requirements = [req for req in requirements if req.split('>=')[0] not in built_in_modules]
    
    print("Checking required packages...")
    
    # Check each requirement
    missing_packages = []
    for requirement in pip_requirements:
        package_name = requirement.split('>=')[0]
        try:
            importlib.import_module(package_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            missing_packages.append(requirement)
            print(f"✗ {package_name} needs to be installed")
    
    # Install missing packages
    if missing_packages:
        print("\nInstalling missing packages...")
        for package in missing_packages:
            print(f"Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install {package}. Error: {e}")
                sys.exit(1)
    
    print("\nAll required packages are installed!")

if __name__ == "__main__":
    check_and_install_requirements() 