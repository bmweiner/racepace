pip install -U -r requirements.txt -t dist/lambda
cp -R racepace/* dist/lambda
cd dist/lambda
zip -r ../lambda.zip ./*
cd ..
rm -r lambda
