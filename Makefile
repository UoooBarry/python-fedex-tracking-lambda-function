pack:
	python3 -m pip install --target ./packages xmltodict requests
	cd packages && 	zip -r ../pack.zip .
	cd ..
	zip -g pack.zip package_tracking.py

deploy:
	aws lambda update-function-code --function-name package_tracking --zip-file fileb://pack.zip