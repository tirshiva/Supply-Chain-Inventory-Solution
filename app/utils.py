"""
utils.py

Utility functions.
"""
def allowed_file(filename):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))
