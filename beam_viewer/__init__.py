from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from beam_viewer.config import Config
from flask_migrate import Migrate

db=SQLAlchemy()
migrate=Migrate()

from beam_viewer.route import index,delete,show,download,explore

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app,db)
    app.add_url_rule('/','index',index,methods=['GET','POST'])
    app.add_url_rule('/explore','explore',explore,methods=['GET','POST'])
    app.add_url_rule('/delete/<path:case_id>/<path:id>','delete',delete,methods=['GET','POST'])
    app.add_url_rule('/show/<case_id>/<id>/<filename>','show',show,methods=['GET','POST'])
    app.add_url_rule('/download/<case_id>/<id>/<filename>','download',download,methods=['GET','POST'])
    return app