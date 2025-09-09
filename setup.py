"""
BOMB DEFUSER GAME - SETUP SCRIPT
================================

PURPOSE: Installation and packaging setup for the Bomb Defuser Game
AUTHOR: Coding Club Presentation Tool
VERSION: 1.0

DESCRIPTION:
Setup script for creating distributable packages and handling dependencies.
Supports both development installation and PyInstaller executable creation.
"""

from setuptools import setup, find_packages
import os
import sys

# Read the README file for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Bomb Defuser Game - Python Debugging Game for Educational Presentations"

# Game metadata
GAME_INFO = {
    'name': 'bomb-defuser-game',
    'version': '1.0.0',
    'description': 'Interactive Python debugging game with bomb defusing theme',
    'long_description': read_readme(),
    'long_description_content_type': 'text/markdown',
    'author': 'Coding Club',
    'author_email': 'your-email@example.com',
    'url': 'https://github.com/your-username/bomb-defuser-game',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Education :: Computer Aided Instruction (CAI)',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: Microsoft :: Windows',
        'Environment :: Win32 (MS Windows)',
    ],
    'keywords': 'game education python debugging programming learning',
    'python_requires': '>=3.8',
}

# Required dependencies
REQUIREMENTS = [
    'PyQt5>=5.15.0',
    'Pygments>=2.10.0',
]

# Optional dependencies for building executable
BUILD_REQUIREMENTS = [
    'PyInstaller>=6.0.0',
    'auto-py-to-exe>=2.0.0',
]

# Development dependencies
DEV_REQUIREMENTS = [
    'pytest>=7.0.0',
    'black>=22.0.0',
    'flake8>=5.0.0',
]

def install_requirements():
    """Install required packages"""
    import subprocess
    
    print("Installing required packages...")
    
    for package in REQUIREMENTS:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    print("✓ All requirements installed successfully!")
    return True

def create_executable():
    """Create standalone executable using PyInstaller"""
    import subprocess
    
    print("Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        'python', '-m', 'PyInstaller',
        '--onefile',
        '--windowed', 
        '--name', 'BombDefuserGame',
        '--add-data', 'levels;levels' if os.path.exists('levels') else '',
        'bomb_defuser.py'
    ]
    
    # Remove empty add-data if levels folder doesn't exist
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.check_call(cmd)
        print("✓ Executable created successfully!")
        print("  Check the 'dist' folder for BombDefuserGame.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create executable: {e}")
        return False

def setup_dev_environment():
    """Set up development environment"""
    print("Setting up development environment...")
    
    all_packages = REQUIREMENTS + BUILD_REQUIREMENTS + DEV_REQUIREMENTS
    
    for package in all_packages:
        try:
            __import__(package.split('>=')[0].split('==')[0])
        except ImportError:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    """Main setup function"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'install':
            install_requirements()
        elif command == 'build':
            if install_requirements():
                create_executable()
        elif command == 'dev':
            setup_dev_environment()
        elif command == 'test':
            # Run the test script
            try:
                import test_game
                test_game.main()
            except ImportError:
                print("test_game.py not found. Make sure you're in the correct directory.")
        else:
            print(f"Unknown command: {command}")
            print("Available commands: install, build, dev, test")
    else:
        # Standard setuptools setup
        setup(
            **GAME_INFO,
            packages=find_packages(),
            install_requires=REQUIREMENTS,
            extras_require={
                'build': BUILD_REQUIREMENTS,
                'dev': DEV_REQUIREMENTS,
            },
            entry_points={
                'console_scripts': [
                    'bomb-defuser=bomb_defuser:main',
                ],
            },
            include_package_data=True,
            package_data={
                '': ['levels/*.py', 'assets/*'],
            },
        )

if __name__ == '__main__':
    main()