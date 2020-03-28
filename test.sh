conda remove --name test --all --yes

conda create --name test python=3 --yes

conda activate test

# list currently tracked files and zip them, this will keep the tree
# structure
git ls-tree -r --name-only HEAD | zip -@ master.zip

mkdir -p tmp/template-master
mv master.zip tmp/template-master
cd tmp/template-master/
unzip master.zip
rm -rf master.zip
cd ..

python template-master/install.py

pip install ".[test]"

pytest



