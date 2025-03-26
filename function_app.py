import azure.functions as func
import logging
import uuid
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="http_to_blob_trigger", auth_level=func.AuthLevel.ANONYMOUS)
def http_m7name_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP trigger function that responds to a GET request with a personalized message.

    This function processes an HTTP request, extracts the 'name' query parameter,
    and returns a personalized greeting. If the 'name' parameter is provided, it
    is used to create a text file with value of 'name' is the content and then
    upload to Azure Blob Storage.
    If the 'name' parameter is not provided, a default message is returned.

    Parameters:
    req (func.HttpRequest): The HTTP request object.

    Returns:
    func.HttpResponse: A response object containing the greeting message.
    """

    logging.info("Python HTTP trigger function processed a request.")

    # Parse query parameter name
    name = req.params.get("name")
    logging.info(f"Param name = {name}.")

    # If name is provided in the query string, use it as the file content, build the file name and upload to blob container
    if name:
        file_name = f'name-{str(uuid.uuid4()).split("-")[0]}.txt'
        write_to_blob_storage(file_name, name)
        return func.HttpResponse(
            f"Hello, {name}. This HTTP triggered function executed successfully."
        )

    # If name is not provided in the query string, send the response with a default message with status code 200
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200,
        )


def write_to_blob_storage(file_name, content):
    """
    Uploads a file to blob storage with the given file name and content.

    Parameters:
    file_name (str): The name of the file to be uploaded.
    content (str): The content of the file to be uploaded.

    Returns:
    None
    """
    try:
        blobServiceClient = BlobServiceClient.from_connection_string(
            "DefaultEndpointsProtocol=https;AccountName=blobstrgm5;AccountKey=qmbk2otAIGUo+URZYZTbFtD6ZbVWp5+5vsYv9bWDTlbIsFNMHYFHBedagCQexDG4xvX+bHE+MaJg+AStjmiAJw==;EndpointSuffix=core.windows.net"
        )
        containerClient = blobServiceClient.get_container_client("output-data")
        blobClient = containerClient.get_blob_client(blob=file_name)
        blobClient.upload_blob(content)
        logging.info(f'Created new file "{file_name}.txt" successfully.')
    except Exception as e:
        logging.error(f"An exception is found: {e}")
