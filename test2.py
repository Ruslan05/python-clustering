import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json


data =  {
        "GlobalParameters": {
        "Append score columns to output": "True",
        "Check for Append or Uncheck for Result Only": "True",
        "Check for Append or Uncheck for Result Only1": "True",
        "Check for Append or Uncheck for Result Only2": "",
        "Database query": "select * from SK",
}
    }

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/ba24eec468a54ed89dc064c2b4345689/services/c69bf9b2a983465f9be98ed2d9bad454/execute?api-version=2.0&details=true'
api_key = 'Zk3Ahs9ouVeiRC40IeVyoykPuriApQU5b5j4o0puzoLLFMSa/tB9y04BFBH1OAcaMYLKJ58yePJyAZSf/vEWEw==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib2.Request(url, body, headers)

try:
    response = urllib2.urlopen(req)

    # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
    # req = urllib.request.Request(url, body, headers)
    # response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib2.HTTPError, error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())

    print(json.loads(error.read()))