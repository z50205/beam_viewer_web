import os

from dotenv import load_dotenv
load_dotenv()

config_path=os.path.abspath(os.path.dirname(__file__))


class Config:    
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL","sqlite:///"+os.path.join(config_path,"beam.db"))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '0')
    MAX_CONTENT_LENGTH= 16 * 1024 * 1024

 
