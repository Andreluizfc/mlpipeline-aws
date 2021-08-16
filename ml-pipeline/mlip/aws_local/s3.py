import os
import base64

# third imports
import boto3
import cv2
import numpy as np
from io import BytesIO
from PIL import Image


def write_image(img_array, bucket, key):
    """Write an image array into S3 bucket

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    file_stream = BytesIO()
    im = Image.fromarray(img_array)
    im.save(file_stream, format='jpeg')
    object.put(Body=file_stream.getvalue())


def get_np_image(bucket, image_name):
    """
    Get images from bucket in np format.

    Parameters
    ----------
    bucket: string
        Bucket name
    image_name : string
        name of the image in bucket

    Returns
    -------
    image: numpy array
        image from bucket
    """
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    image = None
    try:
        response = s3.get_object(Bucket=bucket, Key=image_name)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            file_content = response["Body"].read()
            np_array = np.frombuffer(file_content, np.uint8)
            image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error loading {image_name} from S3 bucket {bucket} - {e}")

    return image


def get_image(bucket, image_name):
    """
    Get images from bucket in bytes format.

    Parameters
    ----------
    bucket: string
        bucket name
    image_name : string
        name of the image in bucket

    Returns
    -------
    image: bytes
        image from bucket
    """
    s3 = boto3.client('s3', endpoint_url="http://localhost:4566")
    image = None
    try:
        response = s3.get_object(Bucket=bucket, Key=image_name)
        status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if status == 200:
            image = base64.b64encode(response["Body"].read())
    except Exception as e:
        print(f"Error loading {image_name} from S3 bucket {bucket} - {e}")

    return image


def load_data(dir, bucket_name):
    """
    Load data to a S3 bucket.

    Parameters
    ----------
    dir: string
        dir where to get the data
    bucket_name : string
        Bucket name

    Returns
    -------
    success: Bool
        True if load is successful.
    """
    success = False
    try:
        os.system(
            f"aws --endpoint-url=http://localhost:4566 s3 sync {dir} s3://{bucket_name}")
        success = True
    except Exception as e:
        print(f"Error loading data to S3 - {e}")
    return success
