"""
Image processing and OCR module.
"""
import os
from typing import Optional, Tuple
from pathlib import Path

# Optional imports - app works without these
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    Image = None

try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    pytesseract = None

from app.core.config import settings


class ImageProcessor:
    """Image processing and OCR utilities."""
    
    @staticmethod
    def preprocess_image(image_path: str):
        """Preprocess image for better OCR results."""
        if not CV2_AVAILABLE or not NUMPY_AVAILABLE:
            raise ImportError("OpenCV and NumPy are required for image processing. Install with: pip install opencv-python numpy")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Optional: denoise
        denoised = cv2.fastNlMeansDenoising(thresh, None, 10, 7, 21)
        
        return denoised
    
    @staticmethod
    def resize_image(image, max_size: Tuple[int, int] = (2000, 2000)):
        """Resize image if too large."""
        if not CV2_AVAILABLE or not NUMPY_AVAILABLE:
            raise ImportError("OpenCV and NumPy are required for image processing.")
        
        height, width = image.shape[:2]
        max_height, max_width = max_size
        
        if height > max_height or width > max_width:
            scale = min(max_height / height, max_width / width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        return image
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> Tuple[str, str]:
        """
        Extract text from image using OCR.
        Returns tuple of (extracted_text, processing_status).
        """
        if not TESSERACT_AVAILABLE:
            return "", "tesseract_not_available"
        
        if not CV2_AVAILABLE or not NUMPY_AVAILABLE or not PILLOW_AVAILABLE:
            return "", "image_processing_libraries_not_available"
        
        try:
            # Preprocess image
            processed_img = ImageProcessor.preprocess_image(image_path)
            processed_img = ImageProcessor.resize_image(processed_img)
            
            # Convert to PIL Image for pytesseract
            pil_image = Image.fromarray(processed_img)
            
            # Configure tesseract if path is provided
            if settings.TESSERACT_CMD:
                pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
            
            # Extract text
            extracted_text = pytesseract.image_to_string(pil_image, lang='eng')
            
            # Clean up text
            extracted_text = extracted_text.strip()
            
            if not extracted_text:
                return "", "no_text_detected"
            
            return extracted_text, "processed"
        
        except Exception as e:
            return "", f"error: {str(e)}"
    
    @staticmethod
    def is_image_file(filename: str) -> bool:
        """Check if file is an image based on extension."""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
        return Path(filename).suffix.lower() in image_extensions
    
    @staticmethod
    def process_image_upload(image_path: str) -> dict:
        """
        Process an uploaded image and extract text.
        Returns dict with extracted_text and processing_status.
        """
        if not ImageProcessor.is_image_file(image_path):
            return {
                "extracted_text": "",
                "processing_status": "not_an_image"
            }
        
        extracted_text, status = ImageProcessor.extract_text_from_image(image_path)
        
        return {
            "extracted_text": extracted_text,
            "processing_status": status
        }


