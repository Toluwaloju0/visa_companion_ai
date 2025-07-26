import os
from dotenv import load_dotenv
from mistralai import Mistral

class Mistral_AI:
    """ the class for the mistral ai usage for a file upload and processing """

    async def save_file(self, saved_file):
        """ a method to saave a pdf file and a document to mistral ai for processing
        Args:
            saved_file(str): a string pointing to the saved file
        """

        load_dotenv()  # load the env values in .env file

        api_key = os.environ["MISTRAL_API_KEY"]
        model = "mistral-large-latest"

        self.mistral = Mistral(api_key=api_key)

        # upload the pdf and return the signed url in strings
        uploaded_pdf = self.mistral.files.upload(
            file={
                "file_name": saved_file,
                "content": open(saved_file, "rb"),
            },
            purpose="ocr"
        )
        signed_url = self.mistral.files.get_signed_url(file_id=uploaded_pdf.id)

        self.signed_url = str(signed_url)[5:-1]

    async def prompt(self):
        """ a method to prompt the AI and check the eligibility of the user
        """

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "using uscis rules volume 6 part f chapter 2 would the owner of this pdf be granted a visa"
                    },
                    {
                        "type": "document_url",
                        "document_url": self.signed_url
                    }
                ]
            }
        ]

        # Get the chat response
        chat_response = self.mistral.chat.complete(
            model= "mistral-large-latest"
,
            messages=messages
        )

        # Print the content of the response
        print(chat_response.choices[0].message.content)
        return chat_response.choices[0].message.content