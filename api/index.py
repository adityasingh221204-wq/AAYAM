"""
Vercel Serverless Function Entry Point for AAYAM
Directly connects Vercel WSGI invocation to Flask Web Server.
"""
import sys
from pathlib import Path

# Set up project root in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web.server import app

# Vercel looks for 'app' as the WSGI callable
