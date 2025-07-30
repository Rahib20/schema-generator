FROM python

WORKDIR /schema-generator

COPY . /schema-generator

RUN pip install -r requirements.txt

#VOLUME ["/schema-generator/data"]

ENV FLASK_APP=Scema.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["python", "run_waitress.py"]
