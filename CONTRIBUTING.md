## Contributing - Raising an Issue

1. Issues > New issue

2. Give lots of details in the description and include screenshots wherever possible. If you would like to work on the issue, please mention this.

3. Please wait to be assigned to the issue before starting work on it.

## Contributing - Fixing an Existing Issue

1. Comment in the issue to ask to be assigned.

2. Download and install the latest version of [python](https://www.python.org/downloads/). Open a terminal and check that it is installed.

   `python --version`

3. Once you have been assigned, follow [these steps](https://docs.github.com/en/get-started/quickstart/contributing-to-projects) for forking and cloning the repo and creating a branch.

4. Install packages.

   ```
   python -m pip install --upgrade pip
   pip install tomlkit
   pip install python-frontmatter
   pip install pycodestyle
   pip install autopep8
   pip install pylint
   pip install pytest
   pip install coverage
   ```

5. Make your code additions or changes.

6. Run unit tests and make sure they all pass.

   `pytest`

   To run one specific unit test file:

   `pytest tests/<unit test file>.py`

7. Run autopep8 to format the code.

   `autopep8 --in-place --recursive --exclude='_version.py' --ignore=E501 .`

   If running into issues, try adding `python -m` in front of the command.

8. Run Pylint to evaluate the code. Please ensure the evaluation rating is at or above 9.0/10.

   `pylint src/ tests/ conftest.py`

   If running into issues, try adding `python -m` in front of the command.

   If you use VS Code, you can install the Pylint VSCode extension, and linting will automatically run when a Python file is opened. Read [here](https://code.visualstudio.com/docs/python/linting#_run-linting) for more details. This can help with identifying and locating issues, but you must run the above command line code to reveal the evaluation score.

9. Commit your changes to your branch and submit a pull request. See [steps in this guide](https://docs.github.com/en/get-started/quickstart/contributing-to-projects). In the pull request description, please link it to the issue by writing Closes #11, where 11 is replaced with your issue number. Please also include screenshots to show results of testing.

## Contributing - Writing Unit Tests

 - Create unit test files in tests/
 - Naming convention: `<source file name>_test.py`
 - Refactor test code by establishing global variables, global fixtures, helper functions in `conftest.py`
 - Run autopep8 and Pylint on test code prior to commit
 - Please remove print statements from tests prior to commit

## Contributing - Running Unit Tests

 - Run all tests: `pytest` or `python -m pytest`
 - Run with detailed view: `pytest -vv`
 - Run one specific test file: `pytest tests/<test file>.py`
 - Run while showing print statements in tests: `pytest -s`
 - Check code coverage (optional): `coverage report -m`
