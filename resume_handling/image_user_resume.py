import os
import sys
import shutil
from PIL import Image
import pytesseract
def main(img_path):
	tess =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
	pytesseract.pytesseract.tesseract_cmd = tess
	text = pytesseract.image_to_string(Image.open(img_path))
	return text
