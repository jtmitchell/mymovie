#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    import ptvsd
    ptvsd.enable_attach("my_secret", address = ('0.0.0.0', 3000))
