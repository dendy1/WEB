import logic
from flask import Flask, render_template, request, send_from_directory, Response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    file_name = request.args.get("q")
    return Response(stream_template("search.html", pathes = logic.search_all_drives(file_name)))

@app.route("/download/<path>", methods=['POST'])
def download(path):
    return send_from_directory(path.directory, path.name)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(2)
    return rv