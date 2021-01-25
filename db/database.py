import os
import boto3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Define AWS const.
ENDPOINT = os.getenv('AWS_ENDPOINT')
USR = os.getenv('AWS_USER')
REGION = os.getenv('AWS_REGION')
PORT = "5432"
DBNAME = "newssites"


# gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = boto3.client('rds')


# Generates AWS RDS token.
def get_db_token():
    t = client.generate_db_auth_token(
        DBHostname=ENDPOINT,
        Port=PORT,
        DBUsername=USR,
        Region=REGION)
    return t


SQLALCHEMY_DB_URL = f"postgresql://{USR}:{get_db_token()}@{ENDPOINT}/{DBNAME}"

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
