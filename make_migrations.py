#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_backend.settings")
    from django.core.management import execute_from_command_line
    from auth_backend import settings 
    settings.SECRET_KEY = 'fake key'

    args = sys.argv + ["makemigrations"]
    execute_from_command_line(args)
