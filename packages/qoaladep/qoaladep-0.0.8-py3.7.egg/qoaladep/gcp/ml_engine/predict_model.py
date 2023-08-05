import base64
from googleapiclient import discovery
from googleapiclient import errors
from oauth2client.client import GoogleCredentials


def predict(project_id, model_name, json_data):
    """[Function for predict data to model in ML Engine]
    
    Arguments:
        project_id {[string]} -- [String of Project ID]
        model_name {[string]} -- [Name model in ML Engine]
        json_data {[type]} -- [ if scikit-learn model:
                                    json_data ([[float]]): List of input model, where each input json_data is a list of floats.
                                        example : json_data = [25, "Private", 226802, "11th", 7, "Never-married", "Machine-op-inspct", "Own-child", "Black", "Male", 0, 0, 40, "United-States"]
                                if tensorflow model:
                                    json_data (dict): List of input model, where each input json_data is a dict.
                                        example : json_data = {'input': {'b64': image_request}}]
    
    Returns:
        response[dict] -- [Response predicted data from ML Engine]
        status[Boolean] -- [Status request prediction model]
    """

    PROJECT_ID = 'projects/{}'.format(project_id)
    modelID = '{}/models/{}'.format(PROJECT_ID, model_name)
    credentials = GoogleCredentials.get_application_default()
    ml = discovery.build('ml', 'v1', credentials=credentials, cache_discovery=False)

    request_body = {"instances": [json_data]}
    request = ml.projects().predict(name=modelID, body=request_body)
    response = None
    status = False

    try:
        response = request.execute()
        status = True
    except errors.HttpError as err:
        response = str(err._get_reason())

    return response, status
