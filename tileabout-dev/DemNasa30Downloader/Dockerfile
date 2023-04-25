FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /config /app
WORKDIR /app
COPY ./.netrc /root
COPY ./requirements.txt /config/
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip install -r /config/requirements.txt
RUN chmod 0600 /root/.netrc
