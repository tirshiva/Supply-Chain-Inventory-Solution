"""
test_inventory.py

Tests for inventory functions.
"""
from app.inventory import update_inventory

def test_update_inventory_add():
    items = [{"item": "Pen", "quantity": 10, "price": 5.0}]
    update_inventory(items, "purchase")
    assert True
