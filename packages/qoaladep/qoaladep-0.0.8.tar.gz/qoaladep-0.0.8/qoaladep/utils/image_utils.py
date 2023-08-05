import io
import cv2
import base64
import numpy as np
from io import BytesIO
from PIL import Image as im
from scipy.ndimage import interpolation as inter


def skew_correction(image_input):
    # convert to binary
    img = im.open(BytesIO(base64.b64decode(image_input)))
    wd, ht = img.size
    pix = np.array(img)
    bin_img = 1 - (pix / 255.0)
    delta = 1
    limit = 45
    angles = np.arange(-limit, limit+delta, delta)
    scores = []
    for angle in angles:
        hist, score = find_score(bin_img, angle)
        scores.append(score)

    best_score = max(scores)
    best_angle = angles[scores.index(best_score)]

    # correct skew
    data = inter.rotate(bin_img, best_angle, reshape=False, order=0)
    data = 255 - data
    img = im.fromarray((255 * data).astype(np.uint8), "RGB")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score

def decode_b64_to_image(base64string):
    try:
        image_decoded = base64.b64decode(base64string)
        image_decoded = im.open(io.BytesIO(image_decoded))
        image_decoded = cv2.cvtColor(np.array(image_decoded), cv2.COLOR_BGR2RGB)
        status_decoded = True
    except:
        image_decoded = ''
        status_decoded = False
    return image_decoded , status_decoded


def encode_image_to_b64(image_array):
    try:
        _ , buffer_image = cv2.imencode('.jpg', image_array)
        image_encoded = base64.b64encode(buffer_image).decode('utf-8')
        status_encoded = True
    except:
        image_encoded = ''
        status_encoded = False
    return image_encoded , status_encoded


def encode_image_to_bytes(image_array):
    try:
        _ , buffer_cropped_image = cv2.imencode('.jpg', image_array)
        image_encoded = buffer_cropped_image.tobytes()
        status_encoded = True
    except:
        image_encoded = ''
        status_encoded = False
    return image_encoded , status_encoded