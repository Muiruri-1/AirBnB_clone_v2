#!/usr/bin/python3
"""
This module contains a Fabric script to create and distribute an archive
to web servers using the function deploy.
"""

from fabric.api import env
from os.path import exists
from datetime import datetime
from fabric.operations import local, put, run
from os import path

env.hosts = ['<IP web-01>', '<IP web-02>']


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


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        archive_name = archive_path.split('/')[-1]
        archive_filename = archive_name.split('.')[0]
        remote_path = "/data/web_static/releases/{}/".format(archive_filename)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(remote_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, remote_path))
        run('rm /tmp/{}'.format(archive_name))
        run('mv {}web_static/* {}'.format(remote_path, remote_path))
        run('rm -rf {}web_static'.format(remote_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(remote_path))

        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
