import flask

from database.sql_provider import SQLProvider
from database.operations import select_from_DB, execute_sql


auth_app = flask.Blueprint('auth_app', __name__, template_folder='templates')
sql_provider = SQLProvider('auth/sql')


@auth_app.route('/')
def auth_handler():
    return flask.render_template('auth.html')


@auth_app.route('/sign-up', methods=['GET'])
def sign_up_handler_get():
    return flask.render_template('sign-up.html')


@auth_app.route('/sign-up', methods=['POST'])
def sign_up_handler_post():
    login = flask.request.form['login']
    password = flask.request.form['password']
    password_repeat = flask.request.form['password_repeat']

    if password != password_repeat:
        return flask.render_template('sign-up.html', message='Password and password\'s repeat don\'t match')

    data = {'login': login, 'password': password}

    if not all(data.values()):
        return flask.render_template('sign-up.html', message='Login or password is empty')

    sql_statement = sql_provider.get('select_login', {'login': login})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if result:
        return flask.render_template('sign-up.html', message='User with this login already exists')
    sql_statement = sql_provider.get('add_buyer', data)
    execute_sql(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    flask.session['user'] = data['login']
    flask.session['password'] = data['password']
    flask.session['is_auth'] = True
    flask.session['role'] = 'buyer'
    return flask.redirect('/')


@auth_app.route('/sign-in', methods=['GET'])
def sign_in_handler_get():
    return flask.render_template('sign-in.html')


@auth_app.route('/sign-in', methods=['POST'])
def sign_in_handler_post():
    data = {'login': flask.request.form['login'], 'password': flask.request.form['password']}
    print(data)
    if not all(data.values()):
        return flask.render_template('auth.html', message='Login or password is empty')

    sql_statement = sql_provider.get('select_role', data)
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if result:
        flask.session['user'] = data['login']
        flask.session['password'] = data['password']
        flask.session['is_auth'] = True
        flask.session['role'] = result[0]['role']
        return flask.redirect('/')

    return flask.render_template('sign-in.html', message='Login or password is incorrect')


@auth_app.route('/logout')
def logout_handler():
    flask.session.clear()
    return flask.redirect('/')
