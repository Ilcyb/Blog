from admin import create_admin_app
from flask import current_app

admin_app = create_admin_app()

if __name__ == '__main__':
    admin_app.run(debug=True)