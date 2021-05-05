FROM python:3

WORKDIR /app
COPY requirements.txt influx.py /app/
RUN pip install -r /app/requirements.txt \
 && chmod 755 influx.py

 ENV LYRIC_CLIENT_ID=
ENV LYRIC_CLIENT_SECRET=
ENV LYRIC_APP_NAME=
ENV LYRIC_REDIRECT_UI=
ENV LYRIC_TOKEN=
ENV INFLUX_HOST=
ENV INFLUX_DB=

CMD ["python3", "-u", "/app/influx.py"]