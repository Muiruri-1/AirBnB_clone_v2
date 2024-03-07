#!/usr/bin/python3
"""
This module contains a Fabric script to distribute an archive
to web servers using the function do_deploy.
"""

from fabric.api import env, put, run, sudo
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']


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
