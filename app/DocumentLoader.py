# app/document_loader.py

import os

class DocumentLoader:
    def __init__(self, folder_path: str):
        """
        Initialize the loader with the folder path where documents are stored.

        Parameters:
        - folder_path (str): Directory containing documents (e.g., .txt files).
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")
        self.folder_path = folder_path

    def load_documents(self, file_extensions=(".txt",)):
        """
        Load and return contents of documents with supported extensions.

        Parameters:
        - file_extensions (tuple): File extensions to load (default: .txt)

        Returns:
        - List[dict]: Each dict contains 'filename' and 'content'
        """
        documents = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith(file_extensions):
                filepath = os.path.join(self.folder_path, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append({
                        "filename": filename,
                        "content": content
                    })
        return documents
