from pathlib import Path
from flask import Blueprint, current_app, send_from_directory

uploads = Blueprint('uploads', __name__)


@uploads.route('/uploads/<path:filename>', methods=['GET'])
def serve(filename):
    uploads_path = Path(current_app.config.get('CORNERSTONE_UPLOADS', current_app.root_path + '/uploads/')).resolve()
    return send_from_directory(uploads_path, filename, conditional=True)
