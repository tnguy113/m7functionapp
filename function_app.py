import azure.functions as func
import logging
import uuid
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_m7name_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_m7name_trigger(req: func.HttpRequest) -> func.HttpResponse:
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
        file_name = f'name-{str(uuid.uuid4()).split("-")[0]}'
        write_to_blob_storage(file_name, name)
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def write_to_blob_storage(file_name, content):
    try:
        blobServiceClient = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=blobstrgm5;AccountKey=qmbk2otAIGUo+URZYZTbFtD6ZbVWp5+5vsYv9bWDTlbIsFNMHYFHBedagCQexDG4xvX+bHE+MaJg+AStjmiAJw==;EndpointSuffix=core.windows.net')
        containerClient = blobServiceClient.get_container_client('output-data')
        blobClient = containerClient.get_blob_client(blob=file_name)
        blobClient.upload_blob(content)
        logging.info(f'Create new file {file_name} successfully.')
    except Exception as e:
        logging.error(f'An exception is found: {e}')
