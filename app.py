from flask import Flask
from view.user_view import user
from view.task_views import task_bp

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(task_bp)

if __name__ == '__main__' :
    app.run()