# run.py
import sys, logging
from waitress import serve
from paste.translogger import TransLogger
import Scema


logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)], format="%(message)s")

app = TransLogger(Scema.Schema)
serve(app, host="0.0.0.0", port=80)
