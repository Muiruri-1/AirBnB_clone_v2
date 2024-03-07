#!/usr/bin/python3
"""
This module contains a Fabric script to delete out-of-date archives
using the function do_clean.
"""

from fabric.api import env, local, run
from datetime import datetime
from os import path
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_clean(number=0):
    """
    Deletes out-of-date archives.

    Args:
        number (int): Number of archives to keep (including the most recent).

    Returns:
        bool: True if cleaning is successful, False otherwise.
    """
    try:
        number = int(number)
        if number < 0:
            return False
        if number == 0 or number == 1:
            number = 1
        else:
            number += 1

        local("cd versions; ls -t | tail -n +{} | xargs -I {} rm -- {}"
              .format(number, number - 1))
        run("cd /data/web_static/releases; ls -t | tail -n +{} | xargs -I {} rm -rf -- {}"
            .format(number, number - 1))
        return True
    except Exception:
        return False
