from flask import Flask, render_template, redirect, jsonify, abort, request
from clickhouse_driver import Client
import requests
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__, static_url_path="/static")
client = Client('194.55.245.41', user="default", password="!1234567Q")

token = '6250249084:AAF5swryY-Dqo360hKtN9cLms1OX1C8ONNw'
chat_id = "930423518"

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    # Здесь ты должен реализовать загрузку пользователя на основе его идентификатора
    # Возвращай объект пользователя или None, если пользователь не найден
    return User()

@login_manager.request_loader
def load_user_from_request(request):
    # Здесь ты должен реализовать загрузку пользователя на основе данных запроса
    # Возвращай объект пользователя или None, если пользователь не найден
    return User()

@app.route("/")
def root():
    return render_template("index.html")

@app.route("/postdata", methods=["POST"])
def postdata():
    username = request.form.get("username")
    password = request.form.get("password")
    request_data = client.execute(f"SELECT COUNT(*) AS count FROM lntech.name WHERE user = '{username}' AND password = '{password}';")
    if request_data == [(1,)]:
        data = {'chat_id': chat_id, 'text': f'{username} authenticated - ip {request.remote_addr}'}
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage?', data=data)
        print(r.json())
        return redirect("/login?username="+username+"&password="+password)
    else:
        abort(401)

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    user_list = ["IP", "GETAWAY", "NETMASK", "DNS1", "DNS2"]
    return render_template("login.html", user_list=user_list, username=username, password=password)

@app.route("/ip")
@login_required
def ip_login():
    return render_template("IP.html")  


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
