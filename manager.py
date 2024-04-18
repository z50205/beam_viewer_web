from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from beam_viewer import create_app, db



app = create_app()
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db)

cli=FlaskGroup(app)

if __name__ == "__main__":
     cli()
    # app.run(debug=True)

