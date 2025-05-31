"""
inventory.py

Handles inventory operations like add/update.
"""
import csv
import os

inventory_file = "data/inventory.csv"

def update_inventory(items: list, bill_type: str):
    """
    Updates inventory based on parsed items.

    Args:
        items (list): List of items from the bill.
        bill_type (str): 'purchase' or 'sale'.
    """
    inventory = {}

    # Load existing inventory
    if os.path.exists(inventory_file):
        with open(inventory_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                inventory[row["item"]] = {"quantity": int(row["quantity"]), "price": float(row["price"])}

    # Update inventory
    for item in items:
        name = item["item"]
        if name in inventory:
            if bill_type == "purchase":
                inventory[name]["quantity"] += item["quantity"]
            elif bill_type == "sale":
                inventory[name]["quantity"] -= item["quantity"]
        else:
            inventory[name] = {"quantity": item["quantity"], "price": item["price"]}

    # Save inventory
    with open(inventory_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["item", "quantity", "price"])
        writer.writeheader()
        for item, data in inventory.items():
            writer.writerow({"item": item, "quantity": data["quantity"], "price": data["price"]})
