FROM python:3.6

ADD backup.py /app/
ADD requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT [ "python", "backup.py", "-d", "repos" ]
