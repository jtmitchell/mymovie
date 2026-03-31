"""
serve.py - launch the app with Granian (Rust-based ASGI server)
===============================================================

Usage
-----
    # development (auto-reload)
    python serve.py

    # or call granian directly:
    granian --interface asgi app.main:app --host 0.0.0.0 --port 8000 --workers 4

Granian docs: https://github.com/emmett-framework/granian
"""

import granian
from granian.constants import Interfaces

if __name__ == "__main__":
    server = granian.Granian(
        # Module path understood by granian's import machinery
        target="config.wsgi:application",
        address="0.0.0.0",  # nosec  # noqa: S104
        port=8000,
        interface=Interfaces.WSGI,
        loop="uvloop",
        process_name="granian [mymovie]",
        websockets=False,
        backpressure=10,
        # Number of worker processes (scale with CPU cores in production)
        workers=1,
        # Threads per worker (Granian uses Tokio under the hood)
        runtime_threads=1,
        # Enable HTTP/2 support
        http="auto",
        # Reload on source changes -  great for development
        reload=True,
    )
    server.serve()
