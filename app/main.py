"""FastAPI module to serve the backend API and all frontend sites."""

from contextlib import asynccontextmanager
from datetime import datetime
from os import getenv
from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi import Path as FasAPIPath
from fastapi import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from modules.config_handler import ConfigHandler
from pydantic import BaseModel, EmailStr, Field
from watchdog.observers import Observer

API_PREFIX: str = getenv("API_PREFIX", "/api")
DATA_PATH: Path = Path(getenv("DATA_PATH", "./data"))
CSV_HEADER: str = "email,timestamp\n"
ADMIN_SECRET: str = getenv("ADMIN_SECRET", "admin")
STATIC_PAGES_DIR: Path = Path(getenv("STATIC_PAGES_DIR", "./static_pages"))

CONF_PATH: Path = Path("./conf/config.yaml")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Function to run at startup and shutdown."""
    # create data directory if it doesn't exist
    DATA_PATH.mkdir(exist_ok=True)
    yield


app = FastAPI(
    title="Landing generator backend API",
    description="API to save email addresses for landing pages.",
    version="0.1.0",
    lifespan=lifespan,
)


class SiteEmail(BaseModel):
    email: EmailStr = Field(..., title="Email", description="Email address to save.")
    site: str = Field(
        ...,
        title="Site",
        description="Site name to save email for.",
        pattern="^[a-zA-Z0-9_]+$",
    )


@app.post(f"{API_PREFIX}/email", status_code=201)
async def post_email(
    site_email: SiteEmail,
) -> None:
    """Save an email address for a site."""
    site: str = site_email.site
    email: str = site_email.email

    SITE_DATA_PATH: Path = DATA_PATH / f"{site}.csv"

    # if file doesn't exist, create it with csv header
    if not SITE_DATA_PATH.exists():
        with open(SITE_DATA_PATH, "w") as f:
            f.write(CSV_HEADER)
    # append email and timestamp to file
    with open(SITE_DATA_PATH, "a") as f:
        f.write(f"{email},{datetime.utcnow().isoformat()}\n")


def check_secret(
    request: Request,
) -> None:
    """Check if the authorization token is correct."""
    if request.headers.get("Authorization") == ADMIN_SECRET:
        return Response(status_code=401, content="Wrong secret.")


@app.get(f"{API_PREFIX}/sites", dependencies=[Depends(check_secret)])
async def get_sites() -> list[str]:
    """Get all sites with emails."""
    # get all csv files in data directory
    return [site.stem for site in DATA_PATH.glob("*.csv")]


@app.get(API_PREFIX + "/emails/{site}", dependencies=[Depends(check_secret)])
async def get_emails(
    site: str = FasAPIPath(
        ...,
        title="Site",
        description="Site name to get emails for.",
        pattern="^[a-zA-Z0-9_]+$",
    ),
) -> list[dict[str, str]]:
    """Get all emails for a site."""
    SITE_DATA_PATH: Path = DATA_PATH / f"{site}.csv"
    # if file doesn't exist, return empty string
    if not SITE_DATA_PATH.exists():
        return Response(status_code=404)
    # read and return file contents
    with open(SITE_DATA_PATH, "r") as f:
        return [
            {"email": line.split(",")[0], "timestamp": line.split(",")[1][:-1]}
            for line in f.readlines()[1:]
        ]


app.mount("/", StaticFiles(directory=STATIC_PAGES_DIR, html=True), name="static")

observer = Observer()
config_handler = ConfigHandler()
observer.schedule(config_handler, path=CONF_PATH, recursive=False)
observer.start()
