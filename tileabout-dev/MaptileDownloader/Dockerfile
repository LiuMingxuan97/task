FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirements.txt /root/
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ \
    && pip install -r /root/requirements.txt \
    && rm -rf ~/.cache/pip
