import urllib2
# If you are using Python 3+, import urllib instead of urllib2
import json

class ServiceImport:

    def __init__(self):
        self.data = []
        self.__api_key = 'Zk3Ahs9ouVeiRC40IeVyoykPuriApQU5b5j4o0puzoLLFMSa/tB9y04BFBH1OAcaMYLKJ58yePJyAZSf/vEWEw=='
        self.__api_url = 'https://ussouthcentral.services.azureml.net/workspaces/ba24eec468a54ed89dc064c2b4345689/services/c69bf9b2a983465f9be98ed2d9bad454/execute?api-version=2.0&details=true'
        self.__api_data = {
            "GlobalParameters": {
                "Append score columns to output": "True",
                "Check for Append or Uncheck for Result Only": "True",
                "Check for Append or Uncheck for Result Only1": "True",
                "Check for Append or Uncheck for Result Only2": "",
                "Database query": "select * from SK",
            }
        }

    def importData(self):
        _body = str.encode(json.dumps(self.__api_data))
        _headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + self.__api_key)}
        _req = urllib2.Request(self.__api_url, _body, _headers)
        try:
            response = urllib2.urlopen(_req)
            # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
            # req = urllib.request.Request(url, body, headers)
            # response = urllib.request.urlopen(req)
            result = response.read()
            self.data = json.loads(result)
        except urllib2.HTTPError, error:
            print("The request failed with status code: " + str(error.code))
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read()))


    def getJsonGridData(self, serviceName):
        self.importData()
        data = self.data['Results'][serviceName]['value']
        columns = data['ColumnNames']
        values = data['Values']
        _columnsToTable = []
        _columnValuesToTable = []
        _rowValues = []

        for column in (columns):
            _columnsToTable.append({'field': column, 'title':column})

        for j, value in enumerate(values):
            for i, item in enumerate(value):
                if(len(_rowValues)):
                    _rowValues[0] = dict(dict({columns[i]: value[i]}).items() + rowValues[0].items())
                else:
                    _rowValues.append(dict({columns[i]: value[i]}))
            _columnValuesToTable.append(_rowValues)
            _rowValues = []

        response = [_columnsToTable, _columnValuesToTable]
        return json.dumps(response)
