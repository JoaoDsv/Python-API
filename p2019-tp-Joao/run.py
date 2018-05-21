from flask import Flask
from apps.user import app_user
from apps.token import app_token
from apps.login import app_login
from apps.transaction import app_transaction

app = Flask(__name__)

app.register_blueprint(app_user)
app.register_blueprint(app_token)
app.register_blueprint(app_login)
app.register_blueprint(app_transaction)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
