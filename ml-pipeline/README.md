# ML-pipeline

**Current stable version**: 0.0.1

This is an Machine Learning data pipeline implementation to upload raw data to a local S3 Bucket, run data segmentation, augmentation, model inference and upload the processed data to a local S3 Bucket.

1. [Libs](#libs)

2. [Installation](#installation)

    2.1 [Local](#local)

    2.2 [Docker](#docker)

3. [CLI](#cli)

4. [Tutorials](#tutorials)


<a name=libs />

## Libs

ml-pipeline uses the following libraries:

- [Localstack](https://github.com/localstack/localstack): Responsible for mocking the AWS development environment.
- [Docker API](https://docker-py.readthedocs.io/en/stable/): Responsible for manipulating docker images.
- [Flask](https://flask.palletsprojects.com/en/2.0.x/): Responsible for serving the Aplication in a REST API.
- [OpenCV](https://opencv.org/): Responsible for manipulating images as arrays.

<a name=installation />

## Installation

<a name=local />

### Local

#### Introduction
Install ML-pipeline in your local machine using anaconda and a virtual environment.
#### Installation
1. Configure Github ssh keys as described [here](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key).

2. Clone the [ml-pipeline](https://github.com/IMI-challenges/ml-pipeline.andre-castro) repository.

3. Download and Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
    * Navigate to ml-pipeline folder.
    * Create a virtual environment with `conda create -n myenv python=3.7` (loacated in the root of this project)
    * Activate your env with `conda activate myenv`
    * Install requiriments with `pip install --upgrade pip wheel setuptools` and `pip install --upgrade -r requirements.txt`
    

4. Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
    * Open terminal and create credentials with `aws configure`.
    * You can enter [real credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html), or dummy ones. 

6. Download, Install and Open [Docker](https://docs.docker.com/engine/install/)

7. Start Localstack by navigating to ml-pipeline/app/localstack and running `docker-compose up`.
    * To check all the services type the following URL on your browser `http://localhost:4566/health`. You should see a list of AWS services if correctly started.
    * Create a local S3 bucket to store raw data with `aws --endpoint-url=http://localhost:4566 s3 mb s3://default-bucket`.
    * Create a local S3 bucket to store processed data with `aws --endpoint-url=http://localhost:4566 s3 mb s3://processed-bucket`.
    * Check if both buckets were created with `aws --endpoint-url=http://localhost:4566 s3 ls`. You should see something similar to:
    ```
    year-month-day hour:min:sec default-bucket
    year-month-day hour:min:sec processed-bucket
    ```

<a name=docker />

### Docker (TODO)

#### Introduction
Install ML-pipeline in your local machine using Docker.

#### Installation
1. Navigate to the folder where the Dockerfile is located.
2. run command `docker build -t ml_pipeline:1.0 .`
3. Then run the docker image on port 5050 `docker run -p 5050:5050 ml_pipeline:1.0`

<a name=cli />

## CLI
The CLI helps the user to use the ML-pipeline package running commands on the terminal. For more information about CLI commands go to the app folder, and run the following command:
```
./main.py -h
```

## Tutorials

### Loading data to local S3 bucket
Use the following CLI command to load your local data to a Localstack S3 bucket.
`./main.py load -p "local_data_path" -b "name_of_the_s3_bucket"`

Example:
```
./main.py load -p "C:\\Users\\johndoe\\files\\data" -b "default-bucket"
```
### Creating a pandas DF from data
This step helps the user to create a pandas dataframe which has the references and metatada from the data at Localstack S3 bucket. The metadata file has the format of a CSV which contains *id, gender, category, subcategory, type, colour, season, year, usage, displayName*.

Use the following CLI command to load random images from Localstack S3 bucket to memory.
`./main.py database -m "path_to_styles.csv"`

Example:
```
./main.py database -m "C:\\Users\\johndoe\\files\\data\\styles.csv" 
```
### Starting local Flask Server
This step is responsible for running the Flask server to make requests. The Serves is responsible for getting SQL queries and searching in the DF created in the previous step.
Use the following CLI command to load random images from Localstack S3 bucket to memory.
`./main.py server start"`

### Making SQL queries to the server
Open the Jupyter notebook located at examples.
There you can view how to make some requests to the server.
