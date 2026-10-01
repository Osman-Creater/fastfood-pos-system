from __future__ import annotations

from fastapi import FastAPI


def attach_api_metadata(app: FastAPI) -> None:
    app.title = "FastFood POS + Bookkeeping API"
    app.version = "0.1.0"
    app.description = "Multi-location fast-food POS, accounting, and reporting backend"
