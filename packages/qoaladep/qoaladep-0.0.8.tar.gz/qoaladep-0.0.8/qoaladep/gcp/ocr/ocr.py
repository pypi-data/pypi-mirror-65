import json
import requests

def google_ocr(image_b64, ocr_key):
    """[Function for extract text from image using google OCR]
    
    Arguments:
        image_b64 {[string]} -- [String of base64 image]
    
    Returns:
        text_annotation[string] -- [Extracted text from image]
    """

    uri = "https://vision.googleapis.com/v1/images:annotate?key="+ocr_key
    header = {
        'Content-type': 'application/json'
    }
    
    payload = {}
    
    image = {}
    image['image'] = {}
    image['image']['content'] = image_b64
    image['features'] = []
    
    feature = {}
    feature['type'] = "TEXT_DETECTION"
    image['features'].append(feature)
    
    request_image = []
    request_image.append(image)
    payload['requests'] = request_image
    
    response = requests.request("POST", uri, data=json.dumps(payload), headers=header)

    response_json = json.loads(response.text)
    response = response_json['responses'][0]

    return response