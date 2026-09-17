# Add the imports
import random
import string

import logging


logger = logging.getLogger(__name__)

from fastapi import FastAPI, HTTPException, Request, status, APIRouter
from fastapi.responses import RedirectResponse

from db import get_connection
from models import URLCreate, ErrorResponse

from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI application:

app = FastAPI(
    title="URL Shortener API",
    description="A practice URL shortening API using FastAPI and PostgreSQL",
    version="1.0.0"
)

# Add the short_cod_generator
def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    code = ""

    for _ in range(length):
        code += random.choice(characters)

    return code

# Create a function to generate a unique short code

def generate_unique_short_code(cursor):
    while True:
        short_code = generate_short_code()

        cursor.execute(
            """
            SELECT id
            FROM urls
            WHERE short_code = %s;
            """,
            (short_code,)
        )

        existing_url = cursor.fetchone()

        if existing_url is None:
            return short_code

# Add a Root Endpoint
@app.get("/")
def home():
    return {
        "message": "URL Shortener API is running"
    }


# Create the POST /urls Endpoint

@app.post(
        "/urls",
        status_code=status.HTTP_201_CREATED,
        responses={
            500: {
                "description": "Internal server error"
        }
    }
)
def create_short_url(url_data: URLCreate):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        short_code = generate_unique_short_code(cursor)

        cursor.execute(
            """
            INSERT INTO urls (
                short_code,
                original_url,
                user_id
            )
            VALUES (%s, %s, %s)
            RETURNING id, short_code, original_url, user_id, created_at;
            """,
            (
                short_code,
                str(url_data.original_url),
                1
            )
        )

        created_url = cursor.fetchone()

        connection.commit()

        return {
            "id": created_url[0],
            "short_code": created_url[1],
            "original_url": created_url[2],
            "user_id": created_url[3],
            "created_at": created_url[4]
        }

    except Exception:
        connection.rollback()
        logger.exception("Failed to create short URL")

        raise HTTPException(
            status_code=500,
            detail="Unable to create short URL"
        )

    finally:
        cursor.close()
        connection.close()


# Add the redirect endpoint
@app.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    request: Request
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        # 1. Find the original URL using the short code
        cursor.execute(
            """
            SELECT id, original_url
            FROM urls
            WHERE short_code = %s;
            """,
            (short_code,)
        )

        result = cursor.fetchone()

        # 2. Return 404 if the short code does not exist
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Short URL not found"
            )

        url_id = result[0]
        original_url = result[1]

        # 3. Get the visitor's IP address
        visitor_ip = None

        if request.client is not None:
            visitor_ip = request.client.host

        # 4. Insert a click record
        cursor.execute(
            """
            INSERT INTO clicks (
                url_id,
                ip_address
            )
            VALUES (%s, %s);
            """,
            (url_id, visitor_ip)
        )

        # 5. Commit the click record
        connection.commit()

        # 6. Redirect to the original URL
        return RedirectResponse(
            url=original_url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    except HTTPException:
        connection.rollback()
        raise

    except Exception:
        connection.rollback()
        logger.exception("Failed to redirect short URL")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process short URL"
        )

    finally:
        cursor.close()
        connection.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)