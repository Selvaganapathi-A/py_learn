#!/usr/bin env:zsh

clear

# echo '←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→'
# uv run ruff format . --line-length 240

# echo '←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→'
# uv run yapf -ir -vv --style google .
# # uv run yapf -ir -vv --style pep8 .

# echo '←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→'
# uv run isort . -vv

# echo '←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→'
# # pytest --cov -vvv -s .
# # pytest --cov -vvv .
# pytest -s -q .
# # pytest --cov .

# echo '←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→↘↓↙←↖↑↗→'
# git status


DIRECTORY="$(dirname "$(readlink -f "$0" )")"



echo
echo --------------------------------------------------------------------------
echo 1] *.pyc files
echo --------------------------------------------------------------------------
# * Remove *.pyc files
find $DIRECTORY -type f ! -path "**/.git/*" -path "**/*.pyc"
echo ==========================================================================
echo
echo --------------------------------------------------------------------------
echo 2] empty files
echo --------------------------------------------------------------------------
# * Remove empty files
find $DIRECTORY -type f ! -path "**/.git/*" ! -path "**/__init__.py" -empty
echo ==========================================================================
echo
echo --------------------------------------------------------------------------
echo 3] __pycache__ folders
echo --------------------------------------------------------------------------
# * Remove __pycache__ directories
find $DIRECTORY -type d ! -path "**/.git/*" -path "**/__pycache__"
echo ==========================================================================
echo
echo --------------------------------------------------------------------------
echo 4] Empty Directories
echo --------------------------------------------------------------------------
# * Remove empty directories
find $DIRECTORY -type d ! -path "**/.git/*" -empty
echo ==========================================================================
echo
echo
read -t 5 -r -p "Want to Actually Delete? Y/N:" userinput

userinput=${userinput:-N}

if [[ $userinput == "Y" ]] ; then
    echo
    echo Files Will be deleted.
    #
    find $DIRECTORY -type f ! -path "**/.git/*" -path "**/*.pyc" -delete
    find $DIRECTORY -type f ! -path "**/.git/*" ! -path "**/__init__.py" -empty -delete
    find $DIRECTORY -type d ! -path "**/.git/*" -path "**/__pycache__" -exec rm -dfr {} +
    find $DIRECTORY -type d ! -path "**/.git/*" -empty -delete
else
    echo
    echo No Files deleted.
fi

echo Check for Code Violations
uv run ruff check .
echo

echo Format with RUFF
uv run ruff format . --line-length 79
echo

# echo Format with yapf
# uv run yapf -ir --style google .
# echo

echo Format imports
uv run isort .
echo
