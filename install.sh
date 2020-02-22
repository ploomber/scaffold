 #!/usr/bin/env bash
 

echo "Python packages should also have short, all-lowercase names,
although the use of underscores is discouraged."
echo -e '\nSource: https://www.python.org/dev/peps/pep-0008/\n'

read -p "Package name: " PROJECT_NAME

sed -i '' "s/{{package_name}}/$PROJECT_NAME/g" template/template/setup.py
mv "template/src/{{package_name}}" "template/src/$PROJECT_NAME"

mv template/* .

mv template/ "$PROJECT_NAME/"