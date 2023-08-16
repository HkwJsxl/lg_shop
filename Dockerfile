FROM ubuntu:20.04
LABEL maintainer="lg_shop.Edu"

ENV PYTHONUNBUFFERED 1

COPY ./Miniconda3-py38_23.1.0-1-Linux-x86_64.sh /opt/
COPY ./sources.list /etc/apt/sources.list
COPY ./ /lg_shop

RUN apt-get update \
    && apt-get -y install wget \
    && mkdir /root/.conda \
    && bash /opt/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh -b \
    && rm -f /opt/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh

ENV PATH /root/miniconda3/bin:$PATH

RUN conda install pymysql -c conda-forge \
    && conda install uwsgi -c conda-forge \
    && pip install supervisor -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r /lg_shop/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && chmod -R 755 /lg_shop

WORKDIR /lg_shop

EXPOSE 8000

VOLUME /lg_shop
