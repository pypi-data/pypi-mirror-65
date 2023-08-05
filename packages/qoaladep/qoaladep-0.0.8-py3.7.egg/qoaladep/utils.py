'''
    File name: utils.py.py
    Author: [Qoala Ds Team]
    Date created: / /2019
    Date last modified: //2020
    Python Version: >= 3.5
    Qoaladep version: v0.2
    Maintainer: [Qoala Ds Team]
'''
import cv2 
import numpy as np 


def nms(result_detection: [float], 
        confidence_threshold=0.75, 
        overlap_threshold=0.3) -> [float]:

    result_box = []
    result_conf = []
    result_class = []
    final_bbox = []
    
    for boxes in result_detection:
        mask = boxes[:, 4] > confidence_threshold
        boxes = boxes[mask, :] 
        classes = np.argmax(boxes[:, 5:], axis=-1)
        classes = classes.astype(np.float32).reshape((classes.shape[0], 1))
        boxes = np.concatenate((boxes[:, :5], classes), axis=-1)

        boxes_dict = dict()
        for cls in range(16):
            mask = (boxes[:, 5] == cls)
            mask_shape = mask.shape
                
            if np.sum(mask.astype(np.int)) != 0:
                class_boxes = boxes[mask, :]
                boxes_coords = class_boxes[:, :4]
                boxes_ = boxes_coords.copy()
                boxes_[:, 2] = (boxes_coords[:, 2] - boxes_coords[:, 0])
                boxes_[:, 3] = (boxes_coords[:, 3] - boxes_coords[:, 1])
                boxes_ = boxes_.astype(np.int)
                    
                boxes_conf_scores = class_boxes[:, 4:5]
                boxes_conf_scores = boxes_conf_scores.reshape((len(boxes_conf_scores)))
                the_class = class_boxes[:, 5:]

                result_box.extend(boxes_.tolist())
                result_conf.extend(boxes_conf_scores.tolist())
                result_class.extend(the_class.tolist())
        
    indices = cv2.dnn.NMSBoxes(result_box, result_conf, confidence_threshold, overlap_threshold)
    for i in indices:
        i = i[0]
        box = result_box[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        conf = result_conf[i]
        the_class = result_class[i][0]
        final_bbox.append([left, top, width, height, conf, the_class])
    return final_bbox
