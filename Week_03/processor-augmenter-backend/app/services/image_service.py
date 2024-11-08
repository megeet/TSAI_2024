from PIL import Image, ImageEnhance, ImageOps
import io
import numpy as np
import cv2
from typing import Dict, List

class ImageService:
    def __init__(self):
        pass

    def process_image(self, image_data: bytes) -> bytes:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Apply multiple noise reduction techniques
        bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
        denoised = cv2.fastNlMeansDenoisingColored(
            bilateral,
            None,
            h=15,
            hColor=15,
            templateWindowSize=7,
            searchWindowSize=21
        )
        median = cv2.medianBlur(denoised, 3)
        final = cv2.GaussianBlur(median, (3, 3), 0)
        
        # Convert back to PIL Image
        final_rgb = cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
        processed_image = Image.fromarray(final_rgb)
        
        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def augment_image(self, image_data: bytes) -> Dict[str, bytes]:
        # Convert bytes to numpy array for OpenCV processing
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # 1. Brightness and Contrast adjustments
        adjusted = cv2.convertScaleAbs(img, alpha=1.3, beta=30)  # alpha for contrast, beta for brightness
        
        # Convert adjusted image to bytes
        adjusted_bytes = cv2.imencode('.png', adjusted)[1].tobytes()
        
        # 2. Horizontal flip
        flipped = cv2.flip(img, 1)  # 1 for horizontal flip
        flipped_bytes = cv2.imencode('.png', flipped)[1].tobytes()
        
        return {
            "adjusted": adjusted_bytes,
            "flipped": flipped_bytes
        }