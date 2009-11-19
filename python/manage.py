#!/usr/bin/env python2.5
from common.appenginepatch.aecmd import setup_env
setup_env(manage_py_env=True)
import settings
from django.core.management import execute_manager
if __name__ == '__main__': execute_manager(settings)
