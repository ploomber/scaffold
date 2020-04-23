set -e
set -x

if [[ "$1" == "-h" || "$1" == "--help" ]]
then
  printf "$(basename $0)\n"
  printf "\tCreate a zip file for deployment. The compressed file includes\n"
  printf "\tthe wheel, Procfile, environment.yml and setup.sh files\n"
  exit 0
fi


G='\e[32m'
END='\e[0m\n'

print () {
    printf "$G$1$END"
}

get_version="
import re, ast
re_ = re.compile(r'__version__\s+=\s+(.*)')
with open('src/package_name/__init__.py', 'rb') as f:
    print(ast.literal_eval(re_.search(f.read().decode('utf-8')).group(1)))
"
VERSION=$(echo "$get_version" | python)
OUTDIR="dist-main-$VERSION"

print "Found version $VERSION in src/package_name/__init__.py..."
print "Output will be stored at $OUTDIR"
rm -rf $OUTDIR

print "Generating wheel..."
python setup.py bdist_wheel --dist-dir $OUTDIR

print "Adding Procfile..."
cp distribute/main/Procfile $OUTDIR

print "Adding environment.yml..."
cp environment.yml $OUTDIR

print "Adding setup.sh..."
cp setup.sh $OUTDIR

print "Zipping..."
zip -r $OUTDIR.zip $OUTDIR
rm -rf $OUTDIR

print "Done. Zip file: $OUTDIR.zip"