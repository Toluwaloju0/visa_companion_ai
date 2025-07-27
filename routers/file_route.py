#!/usr/bin/python3
""" the router for the file processes """

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from utils.save_file import File
from utils.mistral_ai import Mistral_AI

async def file_checker(file: UploadFile):
    """ a function to check a file for validity """

    if file.filename[-4:] != ".pdf" and file.filename[-4:] != ".doc":
        raise HTTPException(status_code=405, detail="file must be a pdf of doc file")

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > 2:
        raise HTTPException(status_code=405, detail="file must not exceed 2MB")

    file.file.seek(0)
    return file


FileRouter = APIRouter(
    prefix="/file",
    tags=["FILES"],
    # description="Upload your files to check your eligibility for a USA visa"
)

@FileRouter.post("/pdf")
async def pdf_files(file: UploadFile = Depends(file_checker)):
    """ The function to process pdf files when they are passed into the API """

    system_file = File() # instantiate a class to handle file save and delete
    mistral = Mistral_AI()  # instantiate a class for AI calls

    # await saving the file into system and mistral bucket
    file_name = await system_file.save(file)
    await mistral.save_file(file_name)

    # process the file in mistral ai
    user_info = await mistral.prompt_for_json()

    result = await mistral.prompt_for_eligibility()

    # save the result to a file
    # filename = f"{user_info[PersonalBackground][GivenName]}{user_info[PersonalBackground][GivenName]}.docx"
    system_file.save_to_file(
        "filename",
        result
    )

    # remove the file
    system_file.remove_file()

    return FileResponse(
        path="filename"
    )


@FileRouter.post("/doc")
async def pdf_files(file: UploadFile = Depends(file_checker)):
    """ The function to process doc files when they are passed into the API """

    system_file = File() # instantiate a class to handle file save and delete
    mistral = Mistral_AI()  # instantiate a class for AI calls

    # await saving the file into system and mistral bucket
    file_name = await system_file.save(file)
    await mistral.save_file(file_name)

    # process the file in mistral ai
    user_info = await mistral.prompt_for_json()
    result = await mistral.prompt_for_eligibility()

    # save the result to a file
    # filename = f"{user_info[PersonalBackground][GivenName]}{user_info[PersonalBackground][GivenName]}.docx"
    system_file.save_to_file(
        "filename",
        result
    )

    # remove the file
    system_file.remove_file()

    return FileResponse(
        path="filename"
    )
    
