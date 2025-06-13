import os
import shutil
from werkzeug.utils import secure_filename

def save_uploaded_files(files, upload_dir):
    """
    Save uploaded file objects to the specified directory.
    Cleans up old files before saving new ones.

    Args:
        files (list): A list of FileStorage objects.
        upload_dir (str): Path to the directory where files will be saved.
    """
    # Clear previous uploads
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir)
    os.makedirs(upload_dir, exist_ok=True)

    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)
