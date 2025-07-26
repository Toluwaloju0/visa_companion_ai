import os
from dotenv import load_dotenv
from mistralai import Mistral
from json import loads

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

    async def prompt_for_json(self):
        """ a method to prompt the AI and check the eligibility of the user
        """

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """this is a request for immigration for people with Extraordinary Ability, \
using USCIS rules volume 6 part f chapter 2 return a json encoded response with the following fields \
Personal background always containing the given name and family name along with other informations, Criteria-specific evidence (e.g., original contributions, critical role, authorship), \
Expert recommendation letters, Media coverage or proof of judging. If images are included use the heading of the \
image as the image"""
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
            model= "mistral-large-latest",
            messages=messages
        )

        # Print the content of the response
        user_info = str(chat_response.choices[0].message.content).replace("`", "")[4:]
        return loads(user_info)


    async def prompt_for_eligibility(self):
        """ a method to prompt the AI and check the eligibility of the user
        """

        # Define the messages for the chat
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
you are an USCIS officer in charge of examining request for immigration. as based on volume 6 part f chapter 2 of the USCIS policy would the owner of this pdf be granted a visa.
write a concise and well detailed reason why the applicant is granted or not granted an applcation for visa.
search for the following Heuristic patterns: Include logic for identifying:
Excessive generalizations or unquantified claims, Lack of independent third-party evidence, Template repetition across letters, Field of expertise inconsistencies
in your response
                        """
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
            model= "mistral-large-latest",
            messages=messages
        )

        # Print the content of the response
        return chat_response.choices[0].message.content