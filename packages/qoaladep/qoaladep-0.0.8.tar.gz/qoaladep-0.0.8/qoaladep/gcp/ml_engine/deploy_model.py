import time
import requests
import google.auth
import google.auth.transport.requests


def deploy(project_id, model_name, version_name, model_path, runtime_version, framework_name, python_version):
    """[Function for model deployment to ml engine]
    
    Arguments:
        project_id {[string]} -- [Project ID of model]
        model_name {[string]} -- [Model name : must be unique within the AI Platform Prediction model.]
        version_name {[string]} -- [Version name of model]
        model_path {[string]} -- [Model path: the path to your model directory in Cloud Storage.
                                    If you're deploying a TensorFlow model, this is a SavedModel directory.
                                    If you're deploying a scikit-learn or XGBoost model, this is the directory containing your model.joblib, model.pkl, or model.bst file.
                                    If you're deploying a custom prediction routine, this is the directory containing all your model artifacts. The total size of this directory must be 500 MB or less.
                                 ]
        runtime_version {[string]} -- [Runtime version: a runtime version based on the dependencies your model needs. If you're deploying a scikit-learn model, an XGBoost model, or a custom prediction routine, this must be at least 1.4.]
        framework_name {[string]} -- [Framework model : TENSORFLOW, SCIKIT_LEARN, or XGBOOST. Omit this parameter if you're deploying a custom prediction routine.]
        python_version {[string]} -- [Python version : must be set to "3.5" (for runtime versions 1.14 through 1.14) or "3.7" (for runtime versions 1.15 and later) to be compatible with model files exported using Python 3. If not set, this defaults to "2.7".]
    """    """[summary]
    
    Arguments:
        model_path {str} -- model path, example: gs://ml_models/recommendation/a1/
        version_name {str} -- the new version name
        model_name {str} -- the model name
    """
    status = True

    try:
        credentials, projects = google.auth.default()
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)

        token = 'Bearer ' + credentials.token
        headers = {'Content-type': 'application/json', 'Authorization': token}

        url_model_deployment = "https://ml.googleapis.com/v1/projects/{}/models/{}/versions".format(project_id, model_name)

        json_model = {}
        json_model["name"] = version_name
        json_model["deploymentUri"] = model_path
        json_model["runtimeVersion"] = runtime_version
        json_model["framework"] = framework_name
        json_model["pythonVersion"] = python_version
        
        response = requests.post(url_model_deployment, json=json_model, headers=headers)
        
        time.sleep(60)
        
        url_set_default = "https://ml.googleapis.com/v1/projects/{}/models/{}/versions/{}:setDefault".format(project_id, model_name, version_name)
        response = requests.post(url_set_default, headers=headers)

    except errors.HttpError as err:
        status = False
        response = str(err._get_reason())

    return response, status

