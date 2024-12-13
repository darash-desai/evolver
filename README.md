# eVOLVER

Control software for the [eVOLVER](https://khalil-lab.gitbook.io/evolver) system.

# Development

## Environment

This project uses `venv` to manage the python environment. If you project directory does not already contain a `.venv` directory, create one by running the command:

```
python -m venv .venv
```

Then activate the environment and install the project dependecies by running the following:

```
source .venv/bin/activate
pip install -r requirements.txt
```

VSCode should automatically activate the your Python environment going forward.

## Starting eVOLVER

To start the eVOLVER system, run:

```
python main.py
```

## Code Formatting

This project uses Black as a code formatter. If you are using Visual Studio Code, install the [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) Python formatter extension.
