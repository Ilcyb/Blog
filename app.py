from app import create_app
from flaskext.markdown import Markdown

app = create_app()
Markdown(app)

if __name__ == '__main__':
    app.run(debug=True)