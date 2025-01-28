import fitz  # PyMuPDF
import os

def pdf_to_images_pymupdf(pdf_path, output_folder="images"):
    """
    Convierte las páginas de un PDF a imágenes utilizando PyMuPDF.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        output_folder (str): Carpeta donde se guardarán las imágenes generadas.

    Returns:
        list: Lista de rutas a las imágenes generadas.
    """
   

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    image_paths = []

    for page_number in range(len(doc)):
        page = doc[page_number]
        pix = page.get_pixmap(dpi=300)  
        image_path = os.path.join(output_folder, f"page_{page_number + 1}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths


pdf_path = "IS1164-1.pdf"  
image_paths = pdf_to_images_pymupdf(pdf_path)

print("Imágenes generadas:")
for img in image_paths:
    print(img)
