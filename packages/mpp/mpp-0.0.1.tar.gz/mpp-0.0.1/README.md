# MPP
My Python Project

## Description
A simple tool to create a project with Python.

## Usage

Start a project easily
```
$ mpp setup
What is your project name? Project
What is your author name? Name
Do you want to display the console (y/n)? [n] y
Are you using an icon (y/n)? [y]

$ python main.py
'Project' is ready to be used
```

Show your configuration
```
$ mpp config
 -→ name = Project
 -→ author = Name
 -→ console = True
 -→ icon = resources/images/icon.ico
```

Edit your configuration
```
$ mpp config name author
What is your project name? [Project] AmazingProject
What is your author name? [Name] John

Are you sure of your modifications (y/n)? y
```

Freeze your project with [PyInstaller](https://www.pyinstaller.org/)
```
$ mpp freeze
[PyInstaller stdout...]
$ target\AmazingProject\AmazingProject.exe
'AmazingProject' is ready to be used
```

Create an installer for your project with [NSIS](https://nsis.sourceforge.io/Main_Page)
```
$ mpp installer
[NSIS stdout...]
```
