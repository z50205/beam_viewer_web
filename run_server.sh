#!/bin/sh



gunicorn --bind=0.0.0.0:8001 --log-level info --workers 4 beam_viewer.wsgi:application