from flask import Flask
from views.user_view import user
from database.__init__ import database
from views.verb_view import verb


app = Flask(__name__)

app.register_blueprint(user)

app.register_blueprint(verb)

print("DATABASE CONNECTION -> ", database.dbConnection)

@app.route("/")
def index():
    return "This API is working."

if __name__ == "__main__":
    app.run()
