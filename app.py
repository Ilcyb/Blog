from app import create_app
from admin import create_admin_app
from flaskext.markdown import Markdown
from datetime import datetime
from flask import current_app

app = create_app()
admin_app = create_admin_app()
Markdown(app)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.context_processor
def inject_power():
    return {'power': current_app.config['POWERD']}

if __name__ == '__main__':
    app.run(debug=True)