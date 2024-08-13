import os
from app.utils import bcolors


class FolderSetup:
    """Set up templates and static folders"""

    def __init__(self, app=None):
        """Set static and templates folder"""
        ...

    def init_app(self, app):
        if app is not None:
            FolderSetup.root_path = os.path.dirname(app.instance_path)

        # app.static_folder = os.path.join(FolderSetup.root_path, "static")
        # app.template_folder = os.path.join(FolderSetup.root_path, "templates")

        # Create uploads directory if it does not exist
        try:
            upload_path = os.path.join(FolderSetup.root_path, "uploads")
            app.config.update(UPLOADS_DIR=upload_path)
            os.mkdir(upload_path)
        except FileExistsError:
            print(bcolors.WARNING + "[*] - Uploads Folder exists skipping this step!")



