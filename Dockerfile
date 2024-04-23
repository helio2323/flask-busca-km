FROM python:3.11.6

RUN pip install --upgrade pip

WORKDIR /FLASK-BUSCA-KM

ADD . /FLASK-BUSCA-KM

RUN pip install -r requirements.txt

CMD ["python3", "index.py"]
