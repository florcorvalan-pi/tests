from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
import json

class DocumentIntelligence:
    def __init__(self, key, endpoint):
        self.model = "prebuilt-document"  # Cambiar al modelo prebuilt-document
        self.client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    def get_text_and_tables(self, file_object):
        poller = self.client.begin_analyze_document(self.model, file_object)
        result = poller.result()

        structured_data = []  
        for page_number, page in enumerate(result.pages, start=1):
            page_content = {"page_number": page_number, "text": "", "tables": []}

            
            for line in page.lines:
                page_content["text"] += line.content + "\n"

            
            for table_index, table in enumerate(result.tables, start=1):
                table_data = {"table_number": table_index, "rows": []}
                for cell in table.cells:
                    
                    while len(table_data["rows"]) <= cell.row_index:
                        table_data["rows"].append([])
                    
                    table_data["rows"][cell.row_index].append(cell.content)
                page_content["tables"].append(table_data)

            structured_data.append(page_content) 

        return structured_data

def save_to_json(structured_data, output_path):
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

def save_to_txt(structured_data, output_path):
    with open(output_path, "w", encoding="utf-8") as txt_file:
        for page in structured_data:
            txt_file.write(f"=== Página {page['page_number']} ===\n\n")
            txt_file.write(page["text"] + "\n")
            for table in page["tables"]:
                txt_file.write(f"--- Tabla {table['table_number']} ---\n")
                for row in table["rows"]:
                    txt_file.write("\t".join(row) + "\n")
                txt_file.write("\n")

key=""
endpoint=""
file_path = "IS1164-1.pdf"

with open(file_path, "rb") as file:
    document_processor = DocumentIntelligence(key, endpoint)
    structured_data = document_processor.get_text_and_tables(file)

#  JSON y TXT
save_to_json(structured_data, "output.json")
save_to_txt(structured_data, "output-con-tablas.txt")
