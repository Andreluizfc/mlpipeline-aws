# python imports
import io
import os
import base64

# third imports
import pandas as pd
import pandasql as ps
import cv2
import albumentations as A
import torch
import numpy as np
from PIL import Image
from torchvision import transforms

# local imports
from main import APP_BASE_DIR
from aws_local import s3
from deep_fashion import deepfashion


def query(query):
    """
    Perform a SQL query in a dataframe.

    Parameters
    ----------
    query : string
        SQL query
    """
    dir_ = os.path.join(APP_BASE_DIR, 'data', 'db.pkl')
    database = pd.read_pickle(dir_)
    return ps.sqldf(f"{query}")


def _augment(images):
    """
    Augment Imagens using Albumentations.

    Parameters
    ----------
    images : dict
        dict containing images
    """

    images_copy = images.copy()

    for id in images.keys():
        image = images[id]
        h, w, _ = image.shape
        transform = A.Compose([
            A.RandomCrop(width=int(w-(w*0.2)), height=int(h-(h*0.2)))
        ])
        cropped = transform(image=image)['image']
        resized = cv2.resize(cropped, (256, 256), interpolation=cv2.INTER_AREA)
        _, im_arr = cv2.imencode('.jpg', resized)
        im_bytes = im_arr.tobytes()
        images_copy[id] = base64.b64encode(im_bytes).decode('utf-8')

    return images_copy


def load_images(df, bucket, augment=False):
    """
    Perform S3 request to load images
    from a df along with metadata.

    Parameters
    ----------
    df : dataframe
        Pandas dataframe containing images references.
    bucket : string
        S3 bucket name.
    """
    load = s3.get_image
    if augment:
        load = s3.get_np_image
    images = {}

    for id in df['id']:
        img_name = f'{id}.jpg'
        image = load(bucket, img_name)
        if not augment:
            image = image.decode('utf-8')
        images[id] = image
    if augment:
        images = _augment(images)
    return images


def predict(image):
    imgdata = base64.b64decode(image)

    fn = deepfashion.FashionNetVgg16NoBn()

    for k in fn.state_dict().keys():
        if 'conv5_pose' in k and 'weight' in k:
            torch.nn.init.xavier_normal_(fn.state_dict()[k])
            print('filling xavier {}'.format(k))

    for k in fn.state_dict().keys():
        if 'conv5_global' in k and 'weight' in k:
            torch.nn.init.xavier_normal_(fn.state_dict()[k])
            print('filling xavier {}'.format(k))

    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

    input_tensor = preprocess(Image.open(io.BytesIO(imgdata)))
    prediction = fn(input_tensor.unsqueeze(0))
    _, category_predicted = torch.max(prediction[1], 1)
    return category_predicted.item()
