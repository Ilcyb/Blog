from app import create_app
from flaskext.markdown import Markdown
from datetime import datetime
from flask import current_app

app = create_app()
Markdown(app)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_power():
    return {'power': current_app.config['POWERD']}

if __name__ == '__main__':
    app.run(debug=True)