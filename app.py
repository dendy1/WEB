import logic
import os
import sys
import logging
from flask import Flask, render_template, request, send_from_directory, Response

app = Flask(__name__)

DRIVES = logic.get_drives_letters()

@app.route('/', defaults={'path': ''})
def browse():
    itemList = DRIVES
    return render_template('browse.html', itemList=itemList)

@app.route('/<path:path>')
def browser(path):
    if os.path.isdir(path):
        itemList = os.listdir(path)
        return render_template('browse.html', currentPath=path, itemList=itemList)

    elif os.path.isfile(path):
        return render_template('file.html', currentFile=path)

    else:
        return 'something bad happened'

@app.route("/search/<path:path>")
def search(path):
    file_name = request.args.get("q")
    return Response(stream_template("search.html", pathes=logic.search_file_in_dir(file_name, path)))

@app.route("/download/<path:path>")
def download(path):
    path = path.lstrip("/")
    path = path.lstrip("\\")
    print(path, file=sys.stderr)
    dirname, fname = os.path.split(path)
    return send_from_directory(dirname, fname)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(2)
    return rv