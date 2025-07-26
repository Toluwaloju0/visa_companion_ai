#!/usr/bin/python3
""" the router for the file processes """

from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
from utils.save_file import File
from utils.mistral_ai import Mistral_AI

FileRouter = APIRouter(
    prefix="/file",
    tags=["FILES"],
    # description="Upload your files to check your eligibility for a USA visa"
)

@FileRouter.post("/pdf")
async def pdf_files(file: UploadFile):
    """ The function to process pdf files when they are passed into the API """

    # if file.filename[:-4] != ".pdf":
        # return JSONResponse({
        #     "error": "This route only accepts pdf files",
        # })

    system_file = File() # instantiate a class to handle file save and delete
    mistral = Mistral_AI()  # instantiate a class for AI calls

    # await saving the file into system and mistral bucket
    file_name = await system_file.save_file(file)
    await mistral.save_file(file_name)

    # process the file in mistral ai
    result = await mistral.prompt()

    return PlainTextResponse(
        content=result
    )
    
