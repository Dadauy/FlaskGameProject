import datetime

from flask import Flask, render_template, session, jsonify
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.utils import redirect

from data import db_session
from data.games import Game
from data.users import User
from forms.createlobby import CreateLobby
from forms.login import LoginForm
from forms.move import MoveForm
from forms.user import RegisterForm

import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = "07658c9d-9db8-4bf8-9886-aaa6175d900e"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route("/")
def home():
    return render_template("home.html", title="Главная")


@app.route("/registration", methods=['GET', 'POST'])
def registration_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/authorization')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route("/authorization", methods=['GET', 'POST'])
def authorization_user():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session["name"] = form.username.data
            return redirect("/lobby")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route("/lobby", methods=['GET', 'POST'])
@login_required
def lobby():
    form = CreateLobby()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # создание новой игры(внесением её в БД)
        game = Game(
            uuid=str(uuid.uuid4()),
            first_name=session.get("name", None),
            second_name="",
            state=None,
            doska="lB,kB,cB,fB,gB,cB,kB,lB,pB,pB,pB,pB,pB,pB,pB,pB,_,_,_,_,_,_,"
                  "_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,pW,pW,pW,pW,pW,pW,pW,pW,lW,kW,cW,fW,gW,cW,kW,lW",
            move=True
        )

        db_sess.add(game)
        db_sess.commit()
        return redirect(f"/game/{game.uuid}")
    return render_template("lobby.html",
                           title="Лобби",
                           form=form,
                           name=session.get("name", None))


@app.route("/game/<gen_uuid>", methods=['GET', 'POST'])
@login_required
def game(gen_uuid):  # принимает форму хода
    form = MoveForm()

    db_sess = db_session.create_session()
    result = db_sess.query(Game).filter(Game.uuid == gen_uuid).first()
    if result.id != 0:
        if form.validate_on_submit() and result.state is None and result.doska.count("g") == 2 and \
                result.second_name != "":
            if len(form.here.data) == 2 and form.here.data[0] in "abcdefgh" and form.here.data[1] in "87654321" and \
                    len(form.there.data) == 2 and form.there.data[0] in "abcdefgh" and form.there.data[1] in "87654321":

                doska = result.doska.split(",")

                gorizont_here = "abcdefgh".index(form.here.data[0])
                vertical_here = "87654321".index(form.here.data[1])
                gorizont_there = "abcdefgh".index(form.there.data[0])
                vertical_there = "87654321".index(form.there.data[1])
                figure = doska[vertical_here * 8 + gorizont_here]

                if figure[0] == "l":  # ладья
                    if gorizont_here == gorizont_there or vertical_here == vertical_there:
                        doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                        doska[vertical_here * 8 + gorizont_here] = "_"

                elif figure[0] == "k":  # конь
                    move_variant = [(vertical_here - 2, gorizont_here + 1),
                                    (vertical_here - 2, gorizont_here - 1),
                                    (vertical_here - 1, gorizont_here + 2),
                                    (vertical_here - 1, gorizont_here - 2),
                                    (vertical_here + 1, gorizont_here + 2),
                                    (vertical_here + 1, gorizont_here - 2),
                                    (vertical_here + 2, gorizont_here + 1),
                                    (vertical_here + 2, gorizont_here - 1),
                                    ]
                    if (vertical_there, gorizont_there) in move_variant:
                        doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                        doska[vertical_here * 8 + gorizont_here] = "_"

                elif figure[0] == "c":  # слон
                    if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here):
                        doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                        doska[vertical_here * 8 + gorizont_here] = "_"

                elif figure[0] == "f":  # ферзь
                    if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here) or \
                            (gorizont_here == gorizont_there or vertical_here == vertical_there):
                        doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                        doska[vertical_here * 8 + gorizont_here] = "_"

                elif figure[0] == "g":  # король
                    if abs(vertical_there - vertical_here) == abs(gorizont_there - gorizont_here) == 1 or \
                            (gorizont_here == gorizont_there or vertical_here == vertical_there):
                        doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                        doska[vertical_here * 8 + gorizont_here] = "_"

                elif figure[0] == "p":  # пешка
                    if figure[1] == "W":
                        if vertical_there - vertical_here == 1:
                            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                            doska[vertical_here * 8 + gorizont_here] = "_"

                    elif figure[1] == "B":
                        if vertical_there - vertical_here == -1:
                            doska[vertical_there * 8 + gorizont_there] = doska[vertical_here * 8 + gorizont_here]
                            doska[vertical_here * 8 + gorizont_here] = "_"

                result.doska = ",".join(doska)

                if result.move is True:  # меняет чей сейчас ход
                    result.move = False
                else:
                    result.move = True

        if result.doska.count("g") == 1 and result.state is None:  # если кто то проиграл
            if result.doska.count("gW"):
                result.state = True
            else:
                result.state = False

        elif result.first_name != session.get("name", None) and result.second_name == "":  # присоединился второй игрок
            result.second_name = session.get("name", None)

        db_sess.commit()

        name = session.get("name", None)
        opponent = result.first_name
        if name == result.first_name:
            opponent = result.second_name

        return render_template("game.html",
                               form=form,
                               name=name,
                               hreff=f"/game/{result.uuid}",
                               opponent=opponent,
                               )
    return "Такой игры нет"


@app.route("/game/<gen_uuid>/reload_data", methods=['GET', 'POST'])
@login_required
def game_reload_data(gen_uuid):  # будет обновлять местоположение фигур. --> json
    db_sess = db_session.create_session()
    result = db_sess.query(Game).filter(Game.uuid == gen_uuid).first()

    msg_state = "Игра идет"
    if result.state is True:
        msg_state = "Белые выиграли"
    elif result.state is False:
        msg_state = "Черные выиграли"

    if result.move is True:
        msg_move = "Ход белых"
    else:
        msg_move = "Ход черных"

    print(result.doska.split(","))
    json_return = {"doska": result.doska.split(","),
                   "state": msg_state,
                   "move": msg_move}

    return jsonify(json_return)


@app.route("/statistics", methods=['GET', 'POST'])
@login_required
def statistics():
    username = session.get("name", None)

    count = 0
    count_win = 0

    db_sess = db_session.create_session()
    result = db_sess.query(Game).filter((Game.first_name == username) | (Game.second_name == username)).all()

    for res in result:
        count += 1
        if res.first_name == username and res.state is True:
            count_win += 1
        elif res.second_name == username and res.state is False:
            count_win += 1

    return render_template("statistic.html",
                           count=count,
                           count_win=count_win,
                           )


if __name__ == "__main__":
    main()
