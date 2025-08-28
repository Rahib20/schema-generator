FROM python

WORKDIR /schema-generator

COPY . /schema-generator
ENV PYTHONUNBUFFERED=1
RUN pip install --no-cache-dir -r requirements.txt

VOLUME [ "/schema-generator/data" ]

ENV FLASK_APP=Scema.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 80

CMD ["python", "run_waitress.py"]
