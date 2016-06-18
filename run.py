from werkzeug.serving import run_simple
from werkzeug.debug import DebuggedApplication
from app import app


app = DebuggedApplication(app, evalex=True)
run_simple('localhost', 5000, app, use_reloader=True)