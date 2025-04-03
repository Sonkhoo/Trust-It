from PIL import Image, ImageEnhance
import pytesseract

def preprocess_image(image_path):
    """Enhance image for better OCR results"""
    img = Image.open(image_path)
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)
    
    return img

def extract_text(image_path):
    """Extract text from image using Tesseract"""
    try:
        processed_img = preprocess_image(image_path)
        text = pytesseract.image_to_string(
            processed_img,
            config='--psm 6 --oem 3'  # Single uniform text block
        )
        return text.strip()
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return None