from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key='secret_123'


from app import router
