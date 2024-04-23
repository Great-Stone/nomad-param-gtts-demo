from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import logging
import os
import shutil

app = FastAPI()
logging.basicConfig(level=logging.DEBUG)

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float

def copy_file_to_static(file_path: str, destination: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    shutil.copy(file_path, destination)

alloc_directory = "../alloc"
output_file = "output.mp3"
output_file_path = os.path.join(alloc_directory, output_file)
static_directory = "static"

try:
    copy_file_to_static(output_file_path, static_directory)
    logging.info(f"File '{output_file}' copied successfully to '{static_directory}'")
except HTTPException as e:
    logging.error(e.detail)

app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="static",
)

@app.get("/")
async def index() -> FileResponse:
    return FileResponse("index.html", media_type="html")

if __name__ == "__main__":
    my_port = int(os.environ.get("MY_PORT", 8080))

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=my_port)