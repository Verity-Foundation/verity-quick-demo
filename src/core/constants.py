"""
Configs, Defaults
"""
from enum import Enum

STORAGEPORT = 8080
HOST = "http://127.0.0.1"
ADDHOST = "127.0.0.1"
VERIFYPORT = 8000

class ContentType(str, Enum):
    """Type of content being claimed."""
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
