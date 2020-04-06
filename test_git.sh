set -e

echo 'creating test conda env...'
conda remove --name test --all --yes
conda create --name test python=3 --yes
eval "$(conda shell.bash hook)"
conda activate test

rm -rf tmp/
BRANCH=$(git rev-parse --abbrev-ref HEAD)
git clone --branch=$BRANCH https://github.com/ploomber/template tmp/
cd tmp/
python install.py --name my_sample_package
rm -rf tmp/