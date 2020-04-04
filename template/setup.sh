# setup.sh is a bash script that sets up the environment from sratch:

# check conda
if [[ "$(command -v conda)" = "" ]]
then
    echo "Cannot setup environment: conda is not installed"
    exit
fi

# A script to setup the development environment
if [[ -z "$1" ]]
then
    echo "Did not pass a name for the environment, using default value: package_name"
    NAME=package_name
else
    NAME=$1
fi

if [[ "$1" == "-h" || "$1" == "--help" ]]
then
  printf "$(basename $0) ENV_NAME\n"
  printf "\tCreate (or replace) a conda environment named ENV_NAME. If no\n"
  printf "\targument is passed, an environment named 'package_name' will be\n"
  printf "\tcreated. After creation, packages from environment.yml are \n"
  printf "\tinstalled using conda install, then wheels are installed using\n"
  printf "\tpip, if there is a setup.py file, it is installed in editable mode.\n"
  exit 0
fi


G='\e[32m'
END='\e[0m\n'

print () {
    printf "$G$1$END"
}

# this will create a conda env called "package_name", will replace an existing one if any
print "Creating conda environment '$NAME'...\n"
conda env create --file environment.yml --force --name $NAME

# we need to initialize conda, see: https://github.com/conda/conda/issues/7980
eval "$(conda shell.bash hook)"

print "Activating $NAME environment: conda activate $NAME"
conda activate $NAME

print "$(type python)"
print "$(type pip)"

# install the package in editable mode to reflect source code changes
if [ -f "setup.py" ]; then
    print "Installing package from setup.py in editable mode (all dependencies)..."
    pip install --editable ".[all]"
fi

# also install any wheels
for f in *.whl; do
  [[ -f "$f" ]] || break
  print "Installing wheel: pip install $f'...\n"
  pip install $f
done


if [ -d "tests/" ]; then
    # test installation
    print "Testing installation..."
    pytest tests/test_import_pkg.py
fi

print "Remember to activate your environment using 'conda activate $NAME'"
