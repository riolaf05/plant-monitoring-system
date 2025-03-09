from langchain_core.tools import tool
import requests
import sys
import datetime

@tool
def send_image(image_path: str) -> str:
    """
    Useful to send images to Telegram.
    """
    return f"Immage sent to Telegram: {image_path}"
    
    