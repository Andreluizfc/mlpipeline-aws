# python imports
import os
import base64

# third imports
import pandas as pd
import pandasql as ps
import cv2
import albumentations as A

# local imports
from main import APP_BASE_DIR
from aws_local import s3


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


def predict(final_features):
    pass
