 #!/usr/bin/env bash
 

echo "Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."
echo -e '\nSource: https://www.python.org/dev/peps/pep-0008/\n'

read -p "Package name: " PROJECT_NAME

sed -i '' "s/{{package_name}}/$PROJECT_NAME/g" template-master/template/setup.py
sed -i '' "s/{{package_name}}/$PROJECT_NAME/g" template-master/template/README.md
mv "template-master/template/src/{{package_name}}" "template-master/template/src/$PROJECT_NAME"

mv template-master/template/* template-master/

rm -rf template-master/LICENSE template-master/test.sh template-master/install.sh template-master/template

mv template-master/ "$PROJECT_NAME/"

echo 'Done.'
