![logo](/logo.png)

## Overview

Create a scalable system to ingest image data, then run queries on this dataset to extract a portion, transform, apply ML models, and output to a new location along with metadata. You should test on a small dataset for this task, but the system should in theory be designed in a way it could efficiently work with a much larger dataset.

### Timeline

You shouldn't spend **more than 8 hours** on this, so it will be intentionally sparse. This helps us understand your ability to prioritize what is important.

Please provide your solution **within 72 hours** of reading this, or on the time line we agree on email.

### Submission

Create a Pull Request for this repo when ready with your result, which we'll use to ask questions and review with you.

## Expectations

Treat this as you would a real-world project that would be used and modified by others in the future, i.e., documentation, tests, etc. There is some flexibility in the requirements, bonus tasks etc - please be creative, but also judicious with a concise solution. Make sure that we are able to validate your solution. It's good to double check this by cloning your solution and trying to run a clean installation yourself before submitting.

Ask as many questions as you want to ensure that we're on the same page in terms of what is required.

The methodology you choose should be efficient; measure and plot the query/processing time for queries limiting results to different numbers of images. Do you expect your system to be able to scale to process 1M images?

### Focus On

- Code Legibility
- Clear Documentation
- Test Coverage - Unit
- Fully Functional

### Tips

We advise you to use docker-compose. That enables you to create a setup that is easy for us to run as well. Also external services like AWS can be mocked. For example to mock AWS you can use https://github.com/localstack/localstack.

## Tasks

Pipeline setup:

- Load images to S3
- Setup a database, of your choice, that will store references to the original images in S3 and metadata.

- Create a Rest API to query, transform and output results into a separate area that contains both the adjusted image(s) and the corresponding metadata.

In a Jupyter Notebook, run a query showcasing each task listed below. Show a basic data analysis of histogram counts for each class, year, etc. of the results. Display a sample of 10 random images from the query results along with their details.

- Obtain some subset of images according to a set of at least 3 different example queries (e.g. all types of Male shoes from years after 2012).
- Add a step to apply a set of augmentations on the results using e.g. the albumentations library to produce randomly cropped versions of the images (up to 20% smaller in each dimension), resized to fit in a common 256x256 square. Again show a sample query including this transformation step, displaying the output images.
- Add a step to run the [DeepFashion](https://github.com/i008/pytorch-deepfashion) model on the query results. You don’t need to train the model, just show that you can run the inference on the model.

!! Remember to write a clear READNE that contains all the details needed to run and understand the solution. !!

## Datasets

Use the following Dataset: [Fashion Products](https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset/version/1) from Kaggle.
> You may need to create a login; also the .zip files may appear corrupt on Linux, try decompressing first on Mac/Win or ask for help.

Use the smaller version [here](https://www.kaggle.com/paramaggarwal/fashion-product-images-small). This dataset contains ~44k images from an online product catalog.

### Sample: styles.csv

![](https://lh4.googleusercontent.com/_blZu-gCTCX2yxD-NZKmkSCJLjKSAP63M-5jBGP6kgdGpxpHMmmhm5IMP-td9pGCGb6urAFhhKNHokbMWM7iFC2a8bHslZHNg_aAsRltLRt_NPexJH14uFjFiW6H2-PcvPG2RrUO)

There are 58,600 entries, although only 44,447 have a corresponding image listed in the images.csv file (the IDs should correspond to the filename); so you should limit to using the entries with available images.

If you have any questions please let us know! Good luck!

## Bonus Points

- Upload the results to an AWS S3 storage bucket instead of a local folder.
- Consider using a task queue based system (e.g. Celery, Kubeflow or another framework of your choice) to make the system extensible and parallelizable.
- Discuss, and/or implement a proof of concept how you would scale your solution to millions or billions of images in a short time frame (<1day, <1hour) assuming infinite resources
- Add a simple API to allow for users to run one-off image processing, and batch processing
