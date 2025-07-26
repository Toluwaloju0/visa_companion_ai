#!/usr/bin/python3

import asyncio
from utils.mistral_ai import Mistral_AI

async def main():
        
    mistral_test = Mistral_AI()
    await mistral_test.save_file("./temp/tolu_format.pdf")
    print(await mistral_test.prompt_for_json())


asyncio.run(main())