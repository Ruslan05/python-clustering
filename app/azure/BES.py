# How this works:
#
# 1. Assume the input is present in a local file (if the web service accepts input)
# 2. Upload the file to an Azure blob - you"d need an Azure storage account
# 3. Call BES to process the data in the blob.
# 4. The results get written to another Azure blob.
#
# Note: You may need to download/install the Azure SDK for Python.
# See: http://azure.microsoft.com/en-us/documentation/articles/python-how-to-install/

import urllib2
# If you are using Python 3+, import urllib instead of urllib2

import json
import time
from azure.storage.blob import *


def printHttpError(httpError):
    print("The request failed with status code!!!: " + str(httpError.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(httpError.info())

    print(json.loads(httpError.read()))
    return


def processResults(result):
    results = result["Results"]
    for outputName in results:
        result_blob_location = results[outputName]
        sas_token = result_blob_location["SasBlobToken"]
        base_url = result_blob_location["BaseLocation"]
        relative_url = result_blob_location["RelativeLocation"]

        print("The results for " + outputName + " are available at the following Azure Storage location:")
        print("BaseLocation: " + base_url)
        print("RelativeLocation: " + relative_url)
        print("SasBlobToken: " + sas_token)

    return

def invokeBatchExecutionService():
    storage_account_name = "szmedialead@gmail.com"  # Replace this with your Azure Storage Account name
    storage_account_key = "Zk3Ahs9ouVeiRC40IeVyoykPuriApQU5b5j4o0puzoLLFMSa/tB9y04BFBH1OAcaMYLKJ58yePJyAZSf/vEWEw=="  # Replace this with your Azure Storage Key
    storage_container_name = ""  # Replace this with your Azure Storage Container name
    connection_string = "DefaultEndpointsProtocol=https;AccountName=" + storage_account_name + ";AccountKey=" + storage_account_key
    api_key = "Zk3Ahs9ouVeiRC40IeVyoykPuriApQU5b5j4o0puzoLLFMSa/tB9y04BFBH1OAcaMYLKJ58yePJyAZSf/vEWEw=="  # Replace this with the API key for the web service
    url = "https://ussouthcentral.services.azureml.net/workspaces/ba24eec468a54ed89dc064c2b4345689/services/c69bf9b2a983465f9be98ed2d9bad454/jobs"

    payload = {

        "Outputs": {

            "RegressionParameters": {"ConnectionString": connection_string,
                                    "RelativeLocation": "/" + storage_container_name + "/RegressionParametrsresults.ilearner"},

            "ResultOfRegression": {"ConnectionString": connection_string,
                                   "RelativeLocation": "/" + storage_container_name + "/ResultOfRegressionresults.csv"},

            "Relevant": {"ConnectionString": connection_string,
                         "RelativeLocation": "/" + storage_container_name + "/Relevantresults.csv"},

            "ClustersParameters": {"ConnectionString": connection_string,
                                  "RelativeLocation": "/" + storage_container_name + "/ClustersParametrsresults.csv"},

            "Clusters": {"ConnectionString": connection_string,
                         "RelativeLocation": "/" + storage_container_name + "/Clustersresults.csv"},
        },
        "GlobalParameters": {
            "Append score columns to output": "True",
            "Check for Append or Uncheck for Result Only": "True",
            "Check for Append or Uncheck for Result Only1": "True",
            "Check for Append or Uncheck for Result Only2": "",
            "Database query": "SELECT * FROM SK",
        }
    }

    body = str.encode(json.dumps(payload))
    headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + api_key)}
    print("Submitting the job...")

    # If you are using Python 3+, replace urllib2 with urllib.request in the following code

    # submit the job
    req = urllib2.Request(url + "?api-version=2.0", body, headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        printHttpError(error)
        return

    result = response.read()
    job_id = result[1:-1]  # remove the enclosing double-quotes
    print("Job ID: " + job_id)

    # If you are using Python 3+, replace urllib2 with urllib.request in the following code
    # start the job
    print("Starting the job...")
    req = urllib2.Request(url + "/" + job_id + "/start?api-version=2.0", "", headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, error:
        printHttpError(error)
        return

    url2 = url + "/" + job_id + "?api-version=2.0"

    while True:
        print("Checking the job status...")
        # If you are using Python 3+, replace urllib2 with urllib.request in the follwing code
        req = urllib2.Request(url2, headers={"Authorization": ("Bearer " + api_key)})

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError, error:
            printHttpError(error)
            return

        result = json.loads(response.read())
        status = result["StatusCode"]
        if (status == 0 or status == "NotStarted"):
            print("Job " + job_id + " not yet started...")
        elif (status == 1 or status == "Running"):
            print("Job " + job_id + " running...")
        elif (status == 2 or status == "Failed"):
            print("Job " + job_id + " failed!")
            print("Error details: " + result["Details"])
            break
        elif (status == 3 or status == "Cancelled"):
            print("Job " + job_id + " cancelled!")
            break
        elif (status == 4 or status == "Finished"):
            print("Job " + job_id + " finished!")

            processResults(result)
            break
        time.sleep(1)  # wait one second
    return


invokeBatchExecutionService()