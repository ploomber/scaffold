set -e

if [[ "$1" == "-h" || "$1" == "--help" ]]
then
  printf "$(basename $0) {app-name}\n"
  printf "\tCreate a zip file for deployment. The compressed file includes\n"
  printf "\tthe wheel, Procfile, environment.yml and setup.sh files\n"
  exit 0
fi

if [[ ! -d "$1" ]]
then
    echo "App '$1' does not exist (can't find folder named $1)"
    exit 1
fi

G='\e[32m'
END='\e[0m\n'

print () {
    printf "$G$1$END"
}


APP=$1
APP_DIR=$(python -c "import os, sys; print(os.path.abspath(sys.argv[1]))" $1)
ROOT=$(python -c "import os, sys; print(os.path.abspath(sys.argv[1]))" $APP_DIR/../../)

print "Building distribution file for app '$APP' in: $APP_DIR"

cd $ROOT
get_version="
import re, ast
re_ = re.compile(r'__version__\s+=\s+(.*)')
with open('src/package_name/__init__.py', 'rb') as f:
    print(ast.literal_eval(re_.search(f.read().decode('utf-8')).group(1)))
"

VERSION=$(echo "$get_version" | python)
print "Found version $VERSION in src/package_name/__init__.py..."

OUT_NAME="package_name-$APP-$VERSION"
print "Output file: $OUT_NAME.zip"

OUT_DIR="$APP_DIR/$OUT_NAME"
print "Output will be stored at $OUT_DIR.zip"
rm -rf $OUT_DIR

print "Generating wheel..."
python setup.py bdist_wheel --dist-dir $OUT_DIR

print "Adding Procfile..."
cp "distribute/$APP/Procfile" $OUT_DIR

print "Adding environment.yml..."
cp environment.yml $OUT_DIR

print "Adding setup.sh..."
cp setup.sh $OUT_DIR

for l in $(cat "$APP_DIR/INCLUDE"); do
    if [[ $l == *","* ]]; then
        f=$(echo "$l" | cut -d "," -f 1)
        pre=$(echo "$l" | cut -d "," -f 2)
        print "Adding $f at $pre"
        mkdir -p "$OUT_DIR/$pre"
        cp $f "$OUT_DIR/$pre"
    else
        cp $l $OUT_DIR
    fi
done

cd $APP_DIR
print "Zipping..."
zip -r "$OUT_NAME.zip" "$OUT_NAME/"
rm -rf "$OUT_NAME/"

print "Done. Zip file: $OUT_DIR.zip"