conda remove --name test --all --yes

conda create --name test python=3 --yes

conda activate test

mkdir tmp
cd tmp

curl -O -L https://github.com/ploomber/template/archive/master.zip
unzip master.zip
rm -f master.zip