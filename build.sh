BASEDIR=$(dirname $0)
cd $BASEDIR
pip install -U -r requirements.txt -t dist/lambda
cp -R racepace/* dist/lambda
cd dist/lambda
zip -r ../lambda.zip .  # zip within dir to avoid parent folder
cd ..
rm -r lambda
