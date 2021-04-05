FROM python:3.8.5

WORKDIR /app

ADD requirements.txt .
ADD app.py .

RUN pip install -r requirements.txt

CMD ["python","app.py"]
