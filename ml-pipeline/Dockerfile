FROM continuumio/anaconda3
COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip wheel setuptools
RUN python -m pip install --upgrade -r requirements.txt
ADD /mlip /mlip
WORKDIR /mlip
EXPOSE 5050
COPY . .