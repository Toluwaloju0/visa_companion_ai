#!/usr/bin/python3
""" a method to create a fastapi app to accept a file for visa companion authentication """

import dotenv

from fastapi import FastAPI
from routers.file_route import FileRouter

app = FastAPI(root_path="/api/v1/visaCompanion")

app.include_router(FileRouter)
