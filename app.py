import logic
import os
from flask import Flask, render_template, request, send_from_directory, Response, abort, stream_with_context

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yXR~Xqw!jm[]Lkeq&wxX/,?RT'

BASE_DIRS = [logic.PseudoDirEntry(path) for path in logic.get_drives_letters()]

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def browse(req_path):
    try:
        requested_path = logic.PseudoDirEntry(req_path)

        if not req_path:
            return render_template('browse.html', current_path=requested_path, item_list=BASE_DIRS)

        if not os.path.exists(requested_path.path):
            return abort(404)

        if requested_path.is_file:
            return render_template('file.html', current_path=requested_path)
        else:
            new_files = logic.my_scan_dir(requested_path.path)
            return render_template('browse.html', current_path=requested_path, item_list=new_files)

    except PermissionError:
        return abort(403)

@app.route("/search", methods=['GET'])
def search():
    file_name = request.args.get("q")
    path = request.args.get("p")
    requested_path = logic.PseudoDirEntry(path)

    if request.args.get("r"):
        path = ''

    return stream_template("search.html", current_path=requested_path,  item_list=logic.search_in_dir(file_name, path))

@app.route("/download/<path:path>")
def download(path):
    dirname, fname = os.path.split(path.rstrip('/'))
    return send_from_directory(dirname, fname, as_attachment=True)

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return Response(stream_with_context(rv))

@app.errorhandler(403)
def access_denied(e):
    return render_template("403.html"), 403