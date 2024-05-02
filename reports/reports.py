import flask
from database.sql_provider import SQLProvider
from database.operations import select_from_DB, execute_sql, call_proc
from auth.login_required import login_required
from auth.role_required import role_required

reports_app = flask.Blueprint('reports_app', __name__, template_folder='templates')
sql_provider = SQLProvider('reports/sql')


@reports_app.route('/')
@login_required(flask.session)
@role_required(flask.session)
def reports_index_handler():
    return flask.render_template('reports_index.html', role=flask.session['role'], reports=flask.current_app.config['reports_list'])

@reports_app.route('/create-rating', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def reports_create_rating_report():
    if flask.request.method == 'GET':
        return flask.render_template('rating_report.html', action='create')

    date = flask.request.form.get('date')
    if not date:
        return flask.render_template('rating_report.html', action='create', message='Пустой ввод')

    year, month = map(lambda x: int(x), date.split('-'))

    sql_statement = sql_provider.get('check_created_rating_report', {'year': year, 'month': month})
    check_result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if check_result:
        return flask.render_template('rating_report.html', action='create', message='Отчет уже существует')

    call_proc(flask.current_app.config['MYSQL_DB_CONFIG'], 'create_profit_rating_report', [month, year])

    return flask.render_template('rating_report.html', action='create', create_flag=True)



@reports_app.route('/create-sales', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def reports_create_sales_report():
    if flask.request.method == 'GET':
        return flask.render_template('sales_report.html', action='create')
    # else
    date = flask.request.form.get('date')
    if not date:
        return flask.render_template('sales_report.html', action='create', message='Пустой ввод')

    year, month = map(lambda x: int(x), date.split('-'))

    sql_statement = sql_provider.get('check_created_sales_report', {'year': year, 'month': month})
    check_result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    if check_result:
        return flask.render_template('sales_report.html', action='create', message='Отчет уже существует')

    call_proc(flask.current_app.config['MYSQL_DB_CONFIG'], 'create_sales_report', [month, year])

    return flask.render_template('sales_report.html', action='create', create_flag=True)


@reports_app.route('/view-sales', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def reports_view_sales_report():
    if flask.request.method == 'GET':
        return flask.render_template('sales_report.html', action='view')
    # else
    date = flask.request.form.get('date')
    if not date:
        return flask.render_template('sales_report.html', action='view', message='Пустой ввод')

    year, month = map(lambda x: int(x), date.split('-'))

    sql_statement = sql_provider.get('check_created_sales_report', {'year': year, 'month': month})
    check_result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
    if not check_result:
        return flask.render_template('sales_report.html', action='view', message='Отчет не найден')

    sql_statement = sql_provider.get('get_sales_report', {'year': year, 'month': month})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)

    count = 0
    income = 0
    for item in result:
        count += int(item['srs_count'])
        income += int(item['srs_income'])

    return flask.render_template('sales_report.html', action='view', result=result,
                                 total_count=count, total_income=income, month=month, year=year)

@reports_app.route('/view-rating', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def reports_view_rating_report():
    if flask.request.method == 'GET':
        return flask.render_template('rating_report.html', action='view')

    # else
    date = flask.request.form.get('date')
    if not date:
        return flask.render_template('rating_report.html', action='view', message='Пустой ввод')

    year, month = map(lambda x: int(x), date.split('-'))

    sql_statement1 = sql_provider.get('check_created_rating_report', {'year': year, 'month': month})
    check_result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement1)
    if not check_result:
        return flask.render_template('rating_report.html', action='view', message='Отчет не найден')

    sql_statement2 = sql_provider.get('get_rating_report', {'year': year, 'month': month})
    result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement2)
    print(result)
    return flask.render_template('rating_report.html', action='view', result=result, month=month, year=year)
