"""
main.py

Entrypoint for the FastAPI backend server.
"""
from fastapi import FastAPI
from api.routes import inventory

app = FastAPI(
    title="Smart Inventory Scanner API",
    description="API to scan bills, parse items, and update inventory.",
    version="1.0.0"
)

app.include_router(inventory.router)
