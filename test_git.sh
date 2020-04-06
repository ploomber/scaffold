set -e

if [[ -z "$1" ]]
then
    echo "Missing GIT_HASH argument, retrieving it from the current repo"
    GIT_HASH=$(git rev-parse HEAD)
else
    GIT_HASH="$1"
fi

echo "Testing git commit $GIT_HASH"

echo 'creating test conda env...'
conda remove --name test --all --yes
conda create --name test python=3 --yes
eval "$(conda shell.bash hook)"
conda activate test

rm -rf /tmp/git_clone
git clone https://github.com/ploomber/template /tmp/git_clone
git checkout $GIT_HASH
cd /tmp/git_clone
python install.py --name my_sample_package

# make sure .git is not deleted
test -d .git

cd ..
rm -rf /tmp/git_clone