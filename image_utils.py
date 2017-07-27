# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image

def delete_white_back(img):
    img = img.convert('RGBA')
    arr = np.array(img)
    
    # set white part transparent entirely
    arr[:, :, -1] = np.where(np.all(arr[:, :, :3] == 255, axis=-1), 0, 255)
    return Image.fromarray(arr)
    
if __name__ == '__main__':
    img = Image.open('稻城亚丁标志.jpg')
    img = delete_white_back(img)
    img.save('稻城亚丁标志-transp.png')
    