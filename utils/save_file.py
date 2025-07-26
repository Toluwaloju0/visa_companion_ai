#!/usr/bin/python3
""" The method to save the pdf file to the LLM bucket """

import os
import shutil

class File:
    """ a class to process all file uploaded """

    async def save_file(self, file):
        """ a method to save a file into the system memort """

        # make a directory to store files
        os.makedirs("./temp", exist_ok=True)

        self.file_name = f"./temp/{file.filename}"

        with open(self.file_name, "wb") as pdf_file:
            shutil.copyfileobj(file.file, pdf_file)

        return self.file_name
    

    def remove_file(self):
        """ a method to remove a file from the system memory """

        os.remove(self.file_name)