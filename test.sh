# stop if any command fails
set -e

if [[ -z "$1" ]]
then
    echo "Missing argument"
    exit 1
fi

CD_ARG=$1

echo 'creating test conda env...'
conda remove --name test --all --yes
conda create --name test python=3 --yes

# we need to initialize conda, see: https://github.com/conda/conda/issues/7980
eval "$(conda shell.bash hook)"

conda activate test

# list currently tracked files and zip them, this will keep the tree structure
echo 'zipping files...'
rm -f master.zip
git ls-tree -r --name-only HEAD | zip -@ master.zip

echo 'Moving files to tmp/'
rm -rf tmp/
mkdir -p tmp/template-master
mv master.zip tmp/template-master
cd tmp/template-master/
unzip master.zip
rm -rf master.zip
cd $CD_ARG

echo 'Running install.py...'
if [[ "$CD_ARG" = ".." ]]; then
    python template-master/install.py --name my_sample_package
elif [[ "$CD_ARG" = "." ]]; then
    python install.py --name my_sample_package
else
    echo "Invalid argument '$CD_ARG'"
    exit 1
fi

echo 'Installing package...'
pip install ".[test]"

echo 'Running tests...'
pytest

echo 'Done.'
