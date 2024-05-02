import flask
from database.sql_provider import SQLProvider
from database.operations import select_from_DB,execute_sql
from auth.login_required import login_required
from auth.role_required import role_required

selects_app = flask.Blueprint('selects_app', __name__, template_folder='templates')
sql_provider = SQLProvider('sql')


@selects_app.route('/')
@login_required(flask.session)
def selects_handler_index():
    return flask.render_template('selects_index.html', role=flask.session['role'])

@selects_app.route('/schedule')
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_schedule():
    sql_statement = sql_provider.get('select_schedule')
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    return flask.render_template('schedule.html', role=flask.session['role'],result=result)




@selects_app.route('/products', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_get():
    sql_statement = sql_provider.get('select_all', {})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    return flask.render_template('products.html', billboard=result,role=flask.session['role'])


@selects_app.route('/search/search-by-name', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_name_search_get():
    return flask.render_template('search_by_name.html')

@selects_app.route('/search/search-by-name', methods=['POST'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_name_search_post():
    data = flask.request.form.get('name').capitalize()

    if not data:
        return flask.render_template('search_by_name.html', error='13')

    sql_statement = sql_provider.get('select_by_name', {'quality': data})
    billboard = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if not billboard:
        return flask.render_template('search_by_name.html', error='14')

    return flask.render_template('search_by_name.html', billboard=billboard)

@selects_app.route('/search/search-by-price', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_price_search_get():
    return flask.render_template('search_by_price.html')

@selects_app.route('/search/search-by-price', methods=['POST'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_price_search_post():
    data1 = flask.request.form.get('from_price')
    data2 = flask.request.form.get('to_price')
    if not data1:
        return flask.render_template('search_by_price.html', error='13')

    sql_statement = sql_provider.get('select_by_price', {'fromprice':data1,'toprice':data2})
    billboard = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    print(billboard)
    if not billboard:
        return flask.render_template('search_by_price.html', error='14')

    return flask.render_template('search_by_price.html', billboard=billboard)


@selects_app.route('/search', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_search_get():
    return flask.render_template('search.html')



@selects_app.route('/employees')
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_employees():
    sql_statement = sql_provider.get('select_employee')
    employees = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    return flask.render_template('employees.html', internal_users=employees)


@selects_app.route('/employees/search-by-position', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_by_pos_handler_get():
    return flask.render_template('search_by_position.html')


@selects_app.route('/employees/search-by-position', methods=['POST'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_by_pos_handler_post():
    data = flask.request.form.get('name').capitalize()

    if not data:
        return flask.render_template('search_by_position.html', message='Empty input')

    sql_statement = sql_provider.get('select_by_pos', {'emplpos': data})
    products = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if not products:
        return flask.render_template('search_by_position.html', message='No results')

    return flask.render_template('search_by_position.html', employees=products)


@selects_app.route('/owners')
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_owners():
    sql_statement = sql_provider.get('select_owner')
    owners = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    return flask.render_template('owners.html', bill_owner=owners)

@selects_app.route('/search/search-by-date', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_date_search_post():
    if flask.request.method == 'GET':
        return flask.render_template('search_by_date.html', action='view')
    # else
    start_date = flask.request.form.get('start_date')
    final_date = flask.request.form.get('final_date')
    if not start_date:
        return flask.render_template('search_by_date.html', action='view', message='Пустой ввод')

    sql_statement = sql_provider.get('date_view', {'start': start_date, 'end': final_date})
    check_result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    if not check_result:
        return flask.render_template('search_by_date.html', action='view', message='Отчет не найден')

    sql_statement = sql_provider.get('date_view', {'start': start_date, 'end': final_date})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    return flask.render_template('search_by_date.html', action='view', result=result)

@selects_app.route('/search/search-by-date_2', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def selects_handler_date_search():
    if flask.request.method == 'GET':
        return flask.render_template('search_by_date_2.html', action='view')
    # else
    date = flask.request.form.get('start_date')
    if not date:
        return flask.render_template('search_by_date_2.html', action='view', message='Пустой ввод')

    sql_statement = sql_provider.get('hard', {'date': date})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    return flask.render_template('schedule.html', action='view', result=result)