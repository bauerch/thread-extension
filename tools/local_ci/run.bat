@echo off
rem Navigate to the project root folder
cd %cd%\..\..
rem TODO: Activate conda virtual environment

echo #### 1. RUN UNIT TESTS ####################################################
python -m coverage run --rcfile=.coveragerc -m unittest discover -s test -p "test_*.py" -b
python -m coverage report --rcfile=.coveragerc -m
del .coverage

echo #### 2. ANALYSE CODE QUALITY ##############################################
for /R src %%f in (*.py) do pylint --rcfile=.pylintrc "%%f"
for /R src %%f in (*.py) do mypy --config=mypy.ini "%%f"
pause
