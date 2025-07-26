This is an analyzer for the EB-1A Risk Analyser. It is a fastapi app which uses fastapi to get pdf file from the user and then upload it to mistral LLM  for checking the eligibiolity of the applicant. To use the AI application download a RFE form from the page https://www.uscis.gov/i-140

Fill all required fields such as your name and state of interest.

Open a linux terminal window in your system and run
`sudo apt update && upgrade -y`

`sudo apt install -y python3 python-pip`

`git clone https://github.com/Toluwaloju0/visa_companion_ai.git`

`cd visa_companion`

`pip3 install -r requirements.txt`

`fastapi dev main.py`

Go to your web browser and type

`http://localhost:8000/docs`

Under Files look for a POST command and try it out by uploading your document and running it