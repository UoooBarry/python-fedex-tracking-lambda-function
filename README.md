# FedEx package tracking AWS lambda function
A simple python lambda function that could track a FedEx package with a tracking number

# Deploy
Configure your AWS credentials by following this tutorial: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html <br>
To create your own lambda function, go to https://aws.amazon.com/lambda/, sign in and create a lambda call `package_tracking` (You can modify it in the Makefile)<br>
Full guide of python lambda function: https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html<br>
A makfile script is made for convenience of the deployment, Steps:<br>
Install and pack the dependencies to a zip: <br>
`make pack` <br>
Deploy to your aws lambda function: <br>
`make deploy`

# AWS Lambda Configuration
You need to configure your FedEx credentials in your lambda function's environment variables. <br>
For sandbox credentials, you can easily apply it in https://www.fedex.com/en-us/developer/web-services.html <br>
You need the following environment variables: <br>
`ACCOUNT_NUMBER
KEY
PASSWORD
METER_NUMBER`

# Call the function
Request body: <br>
`{
  "track_no": "123456789012",
  "lang": "en" | "fr",
  "sandbox": true | false
}`