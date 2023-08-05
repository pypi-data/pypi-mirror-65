FROM continuumio/miniconda3
# We need conda for geopandas installation

ENV PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=0
RUN conda install python=3.7
ENV PATH /opt/conda/envs/env/bin:$PATH

RUN apt-get update && apt-get install -y git
RUN python -m pip install --upgrade pip
RUN conda install geopandas
RUN pip install pytest ipdb

WORKDIR /app
COPY requirements.txt /requirements
RUN pip install -r /requirements
COPY . /app
RUN pip install -e .
