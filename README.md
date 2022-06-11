# Fivetran Lambda Function with Serverless Framework

## Settings AWS IAM for Fivetran:

To connect [AWS Lambda](https://aws.amazon.com/lambda/) functions to Fivetran, you need:

- An AWS Lambda function
- An AWS account with Administrator privileges
- Make a note of the **External ID**. You will need it to configure AWS to connect with Fivetran. The automatically-generated External ID is tied to your fivetran account. If you close and re-open the setup form, the ID will remain the same.

​	**Fivetran** **External ID is** : Example `viscous_diersionss`

1. Create **policy** in JSON tab:

   ```json
      {
          "Version": "2012-10-17",
          "Statement": [
              {
                  "Sid": "InvokePermission",
                  "Effect": "Allow",
                  "Action": [
                      "lambda:InvokeFunction"
                  ],
                  "Resource": "*"
              }
          ]
      }
   ```

   Policy Name: `Fivetran-Lambda-Invoke`

2. Create a **unique role** for all Fivetran's invoke functions.

   * Select type of trusted entity - Another AWS account - We need the `Account ID` 

   * In **Options**, check the **Require external ID** checkbox.

   * Click **Next: Permissions**.

   * Select the `Fivetran-Lambda-Invoke` policy. 

   * Click **Next: Tags**. Entering tags is optional, but you must click through the step.

   * Click **Next: Review**.

   * Name your new role `Fivetran-Lambda` and then click **Create role**.

   * Select the Fivetran role that you just created. In the **Summary** section, make a note of the **Role ARN** value. 

   * This **Role ARN** we used for all Lambda Functions related with Fivetran. 

   * Select the designated Fivetran role.

   * In the **Summary** section, click the **Trust Relationships** tab, and then click **Edit trust relationships**.

     ```json
     {
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Principal": {
             "AWS": "arn:aws:iam::834469178297:root"
           },
           "Action": "sts:AssumeRole",
           "Condition": {
             "StringEquals": {
               "sts:ExternalId": "your_fivetran_externalID"
             }
           }
         },
         {
           "Effect": "Allow",
           "Principal": {
             "Service": "lambda.amazonaws.com"
           },
           "Action": "sts:AssumeRole"
         }
       ]
     }
     
     ```

     Note: Replace the `"your_fivetran_externalID"` with the Fivetran External ID

     * Click **Update Trust Policy**.

       

   ## Setting up AWS user for Serverless Framework:

   Setting up AWS user `serverles-admin` 

   - Acces key - Programmatic access
   - Note: We can to  `Attach existing policies directly` - `AdministratorAccess` this is no recommend, the DevOps need to check what is the best policy for this user. 
   - Save the credentials

   

   ## Setting local Serverless Framework:

   - [Serverless Framework](https://www.serverless.com/) aims to ease the pain of creating, deploying, managing, and debugging lambda functions

   - It integrates well with CI/CD tools - [Github Actions](https://github.com/serverless/github-action)

   - It has **[CloudFormation](https://aws.amazon.com/es/cloudformation/)** support so your entire stack can be deployed using this framework

   - For this framework you need to have [NodeJS](https://nodejs.org/en/)

     	-  Node v16.13.0
     	-  NPM v8.7.0

   - We need to install [AWS CLI](https://aws.amazon.com/cli/)

     `aws-cli/1.22.55 Python/3.8.10 Linux/5.13.0-44-generic botocore/1.24.0`

   - Install the Serverless Framework.

     ```bash
     sudo npm install -g serverless

   - Download credentials user on your machine. 

   - Set the Serverless credentials.

     ```bash
     serverless config credentials --provider aws --key xx --secret xx --profile serverless-admin
     ```

##  Create a lambda function with Serverless Framework

Note: 	`serverless` and `sls`  are the same commands.

```bash
➜  fivetran_lambda_connector_serverless git:(main) sls  
? What do you want to make? (Use arrow keys)
❯ AWS - Node.js - Starter 
  AWS - Node.js - HTTP API 
  AWS - Node.js - Scheduled Task 
  AWS - Node.js - SQS Worker 
  AWS - Node.js - Express API 
  AWS - Node.js - Express API with DynamoDB 
  AWS - Python - Starter 
  AWS - Python - HTTP API 
  AWS - Python - Scheduled Task 
  AWS - Python - SQS Worker 
  AWS - Python - Flask API 
  AWS - Python - Flask API with DynamoDB 
  Other 
```

Select AWS - Python - Starter and set the proyect name :

```bash
➜  fivetran_lambda_connector_serverless git:(main) ✗ sls                           

Creating a new serverless project

? What do you want to make? AWS - Python - Starter
? What do you want to call this project? aws-fivetran-connector-template

✔ Project successfully created in aws-fivetran-connector-template folder

? Do you want to login/register to Serverless Dashboard? No

```

Note: you can create a project for each Fivetran connector

```bash
fivetran_lambda_connector_serverless
├── aws-fivetran-connector-template
│   ├── handler.py
│   ├── README.md
│   └── serverless.yml
└── README.md
```

Move to  `aws-fivetran-connector-template`, set a `venv` and activate it.

Update you `.gitignore` file:

```
# Distribution / packaging
.Python
venv/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Serverless directories
.serverless

# NPM directories
package-lock.json
node_modules/
```



Run `npm init` for create `package.json` file for install new plugins in Serverless.

```json
{
  "name": "aws-fivetran-connector-template",
  "version": "1.0.0",
  "description": "Template for Fivetran AWS connector using Serverless Framework",
  "main": "handler.py",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [
    "Fivetran",
    "AWS",
    "Serverless",
    "Connector"
  ],
  "author": "MCTEKK",
  "license": "ISC"
}

```

 Install `serverless-python-requirements` plugin for deploy Python lambda functions with `requirements.txt`

```bash
serverless plugin install -n serverless-python-requirements
```

Automatic update `package.json`:

```json
{
  "name": "aws-fivetran-connector-template",
  "version": "1.0.0",
  "description": "Template for Fivetran AWS connector using Serverless Framework",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [
    "Fivetran",
    "AWS",
    "Serverless",
    "Connector"
  ],
  "author": "MCTEKK",
  "license": "ISC",
  "devDependencies": {
    "serverless-python-requirements": "^5.4.0"
  }
}
```

Configuration  in `serverless.yml` : 

```yaml
service: aws-fivetran-connector-template

frameworkVersion: '3'

provider:
  name: aws
  runtime: python3.8

functions:
  aws-fivetran-connector:
    handler: handler.lambda_handler

plugins:
  - serverless-python-requirements

```

The `functions` you can set the name of AWS lambda  `aws-fivetran-connector` and the handler with `handler.lambda_handler`  ( `handler.py`  and function `lambda_handler`)

### Deploy project with Serverless

```bash
serverless deploy --aws-profile serverless-admin --region us-west-2
```

```bash 
Deploying aws-fivetran-connector-template to stage dev (us-west-2)

✔ Service deployed to stack aws-fivetran-connector-template-dev (155s)

functions:
  aws-fivetran-connector: aws-fivetran-connector-template-dev-aws-fivetran-connector (11 MB)

Toggle on monitoring with the Serverless Dashboard: run "serverless"
```

This is the function name in aws : `aws-fivetran-connector-template-dev-aws-fivetran-connector`

**Note**: In the `.serverless/` directory you can see the `aws-fivetran-connector-template.zip` deployment file.



## Fivetran handler.py

### Fivetran Event:

```json
{
    "secrets": {
        "consumerKey": "",
        "consumerSecret": "",
        "apiKey": "yourApiKey"
    },
    "state": { }
}
```

The first event `state` is empty.  The `secrets` only accept the specify fields names `consumeKey, consumerSecret and apiKey`.

### Fivetran Response:

```json
{
    "state": {"count": "0" },  
    "insert":  {"table_name": [ {"items": "objects"} ] },
    'schema':  {'primary_key': ['asin', 'date'] } ,
    'hasMore': "False"
}
```

You can add `update and delete` with the same format that `insert`

### Fivetran Error Response:

```json
{
    "state": {"count": "1" }, 
    "errorMessage": "Custom error handling"
}
```

### Fivetran connector `handler.py` template

```python

from datetime import datetime

def lambda_handler(request, context):

    # Read event data - get secret and state object from event
    secrets = request['secrets']
	state = request['state']
    data = []
    table_name = "table_name"
    
    
    # API call - get data from API try catch block
    try:
        # Authenticate API call - use secret to authenticate API call
        consumer_key = secrets["consumerKey"]
        consumer_secret = secrets["consumerSecret"]
        api_key = secrets["apiKey"]
        
        api_client = get_client(consumer_key, consumer_secret, api_key)
        
    	# Process data - process data from API call and use state object to process data
        # Always confirm the state object is not empty
		count = 0 if not 'count' in request["state"] else int(request["state"]["count"])
        
        
        # Extract API data
        raw_data = get_data_from_api(api_client)
        
        # Transform API data
        data = transform_data(raw_data)
        
    except Exception as e:
    	# Error handling - if error, return error message for Fivetran
        return {'state': {'count': count }, 'errorMessage': f"Error {str(e)}"}

    # Load API data - return data to Fivetran
    return {
        "state": {"count": count + 1 },  
        "insert":  { f"{table_name}": data },
        'schema':  {'primary_key': ['id', 'date'] } ,
        'hasMore': False
	 }
  

def get_client(consumer_key, consumer_secret, api_key):
    """
    Get client API
    """
    pass

def get_data_from_api(api_client):
    """
    Get data API
    """
    pass

def transform_data(raw_data):
    """
    Transform data API
    """
    pass
```






​      