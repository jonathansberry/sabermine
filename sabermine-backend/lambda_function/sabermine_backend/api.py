from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from mangum import Mangum
import string
from pydantic import BaseModel, HttpUrl
from . import logic
from starlette.responses import RedirectResponse


app = FastAPI()

BASE62_ALPHABET = string.digits + string.ascii_letters


class URLString(BaseModel):
    url: HttpUrl


@app.get("/api/")
def ready() -> dict[str, str]:
    """Check to confirm if the service is ready."""
    return {"message": "Sabermine api ready"}


@app.post("/api/shorten_url")
def shorten_url(input_url: URLString) -> dict[str, str]:
    """Generates a short URL, stores it in DynamoDB, and returns the short code."""
    try:
        short_url = logic.shorten_url(str(input_url.url))
        return {"short_url": short_url}
    # TODO Specific exceptions should be caught
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating short URL: {str(e)}")


@app.post("/api/upload")
def upload(file: UploadFile = File(...)) -> dict[str, str]:
    """Uploads a file to S3 and returns the URL."""
    try:
        file_url = logic.upload_file(file)
        short_url = logic.shorten_url(file_url)
        return {"short_url": short_url}
    # TODO Specific exceptions should be caught
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@app.get("/api/all")
def get_all_short_urls(
    limit: int = Query(10, ge=1, le=100),
    last_evaluated_key: str = None
):
    """
    Retrieve all short URLs from the DynamoDB table.
    """
    try:
        return logic.get_all_short_urls(limit, last_evaluated_key)
    # TODO Specific exceptions should be caught
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DynamoDB error: {str(e)}")


@app.get("/{short_code}")
def redirect(short_code: str, response_class=RedirectResponse):
    """API to resolve short code to the original URL."""
    try:
        original_url = logic.retrieve_url(short_code)
    # TODO Specific exceptions should be caught
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving short URL: {str(e)}")
    if not original_url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(original_url)


handler = Mangum(app)
