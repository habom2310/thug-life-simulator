import numpy as np
import cv2
import base64
import io
from PIL import Image

def calculate_bright_intensity_of_environment(image, percentage = 0.1):
    image = np.array(image).reshape(-1)
    pixels = np.random.choices(image, int(image.shape[0]*percentage, replace=False))
    return np.average(pixels)

def read_dlib_rect(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y

    return x,y,w,h

def read_dlib_shape(shape):
    np_shape = []
    for i in range(shape.num_parts):
        x = shape.part(i).x
        y = shape.part(i).y
        np_shape.append([x,y])

    return np_shape

def select_ROI(face, shape):
    roi1 = face[shape[29][1]:shape[33][1], #right cheek
            shape[54][0]:shape[12][0]]
            
    roi2 =  face[shape[29][1]:shape[33][1], #left cheek
            shape[4][0]:shape[48][0]]

    return roi1, roi2

def extract_mean_val(rois):
    g = []
    for roi in rois:
        g.append(np.mean(roi[:,:,1]))
    #b = np.mean(ROI[:,:,2])
    #return r, g, b
    mean_val = np.mean(g)
    return mean_val

def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

    
def base64_to_img(base64_string):
    # print(base64_string)
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(io.BytesIO(imgdata))
    image = np.array(cv2.cvtColor(np.array(image),cv2.COLOR_BGR2RGB))
    return image

def img_to_base64(img):
    base64_string = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    return base64_string