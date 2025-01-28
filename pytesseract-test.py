import os
import pytesseract
from PIL import Image

def extract_text_from_images(image_folder):
    """
    Extrae texto de todas las imágenes en una carpeta usando Tesseract.

    Args:
        image_folder (str): Ruta a la carpeta donde se encuentran las imágenes.

    Returns:
        dict: Diccionario con los textos extraídos por imagen.
    """
    extracted_text = {}

 
    for filename in sorted(os.listdir(image_folder)):  
        print('bucle')
        if filename.endswith((".png", ".jpg", ".jpeg")):  
            image_path = os.path.join(image_folder, filename)
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang="spa")  # 'spa' para español
            extracted_text[filename] = text  

    return extracted_text


image_folder = "./images"  

texts = extract_text_from_images(image_folder)

with open("output_text.txt", "w", encoding="utf-8") as output_file:
    for image_name, text in texts.items():
        print('docs')
        output_file.write(f"--- Texto de {image_name} ---\n")
        output_file.write(text + "\n\n")

print("Extracción completa. Texto guardado en 'output_text.txt'.")
