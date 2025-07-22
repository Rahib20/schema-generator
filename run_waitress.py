from waitress import serve
import Scema

serve(Scema.Schema, host='0.0.0.0', port=80)

print("debug")