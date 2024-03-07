#!/usr/bin/python3
"""
This module contains a Fabric script to generate a .tgz archive
from the contents of the web_static folder of the AirBnB Clone repo.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Path to the generated archive if successful, None otherwise.
    """
    try:
        now = datetime.now()
        time_format = now.strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_" + time_format + ".tgz"
        local("mkdir -p versions")
        local("tar -cvzf versions/{} web_static".format(archive_name))
        return "versions/{}".format(archive_name)
    except Exception:
        return None
