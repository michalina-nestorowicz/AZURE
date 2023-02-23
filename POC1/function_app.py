import azure.functions as func
from azure.storage.blob import BlobServiceClient,BlobClient
import logging
import requests
import json

app = func.FunctionApp()

# Learn more at aka.ms/pythonprogrammingmodel

# Get started by running the following code to create a function using a HTTP trigger.

@app.function_name(name="HttpTrigger1")
@app.route(route="hello")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
     logging.info('Python HTTP trigger function processed a request.')

     name = req.params.get('name')
     if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

     if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
     else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
     

@app.function_name(name="Upload")
@app.route(route="upload")
def test_function(req: func.HttpRequest) -> func.HttpResponse:
     logging.info('UPLOAD TRIGGER')
     r = requests.get('https://api.gios.gov.pl/pjp-api/rest/station/findAll')
     data = r.json()
     with open('data.json', 'w') as f:
        json.dump(data, f)
     return func.HttpResponse(f'Response: {r.status_code}')
     #return func.HttpResponse(f'Response x {r.text}')



@app.function_name(name="BlobOutput1")
@app.route(route="file")
@app.blob_input(arg_name="inputblob",
                 path="C:\\Users\\mnestoro\\test.txt",
                 connection="AzureWebJobsStorage")
@app.blob_output(arg_name="outputblob",
                path='https://nestorowiczstorageacc.blob.core.windows.net/input',
                connection="AzureWebJobsStorage")
def main(req: func.HttpRequest, inputblob: str, outputblob: func.Out[str]):
    logging.info(f'Python Queue trigger function processed {len(inputblob)} bytes')
    outputblob.set(inputblob)
    return "ok"