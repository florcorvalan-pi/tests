from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class DocumentIntelligence:

    def __init__(self, key, endpoint):

        self.model = "prebuilt-layout"


        self.client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

    def get_text_from_file(self, file_object):

        poller = self.client.begin_analyze_document(self.model, file_object)
        result = poller.result()

        text_content = ""

        for page in result.pages:
            for line in page.lines:
                text_content += line.content + "\n"

        return text_content.strip()
    
def process_file(file_path):
    # Abrimos el archivo en modo binario (importante para Azure Document Intelligence)
    with open(file_path, "rb") as file:
        # Creamos una instancia de DocumentIntelligence
        document_processor = DocumentIntelligence(
            key="1dapUpI2GJRzLrwPznSs3olAUUmxtUjSBo4hIplCWEGZIZX01llfJQQJ99AKACYeBjFXJ3w3AAALACOGM2Zk",
            endpoint="https://snr-document-intelligence.cognitiveservices.azure.com/"
        )
        
        # Procesamos el archivo
        text_content = document_processor.get_text_from_file(file)

        with open('result.txt', "w", encoding="utf-8") as output_file:
            output_file.write(text_content)
        
        return text_content

# Ejemplo de uso
file_path = "IS1164-1.pdf"  # o cualquier otro documento
extracted_text = process_file(file_path)
print(extracted_text)

