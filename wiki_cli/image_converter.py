from PIL import Image
import requests
from io import BytesIO
import numpy as np

class ASCIIConverter:
    ASCII_CHARS = '@%#*+=-:. '
    
    @classmethod
    def image_to_ascii(cls, image_url, width=80):
        """Convert image to ASCII art"""
        try:
            # Download image
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            
            # Convert to grayscale
            img = img.convert('L')
            
            # Resize image
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio * 0.5)  # Multiply by 0.5 to account for terminal character aspect ratio
            img = img.resize((width, height))
            
            # Convert pixels to ASCII
            pixels = np.array(img)
            ascii_img = ''
            
            for row in pixels:
                for pixel in row:
                    ascii_img += cls.ASCII_CHARS[pixel * (len(cls.ASCII_CHARS) - 1) // 255]
                ascii_img += '\n'
            
            return ascii_img
            
        except Exception as e:
            return f"Error converting image: {str(e)}"
