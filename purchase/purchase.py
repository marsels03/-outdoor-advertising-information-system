import flask
from database.sql_provider import SQLProvider
from database.operations import select_from_DB, execute_sql, execute_transaction
from auth.login_required import login_required
from auth.role_required import role_required
from flask import request, url_for
from datetime import datetime

purchase_app = flask.Blueprint('purchase_app', __name__, template_folder='templates')
sql_provider = SQLProvider('purchase/sql')
# start_date = None
# final_date = None
# result = None
reserved_billboards = []
aso = []


def calculate_total(cart_items, start_date, final_date):
    total = 0
    date_format = '%Y-%m-%d'
    start_date = datetime.strptime(start_date, date_format)
    final_date = datetime.strptime(final_date, date_format)
    date_difference = (final_date - start_date).days

    for item in cart_items:
        total += item['price'] * date_difference

    return total


def check_dates(date1, date2):
    return date1 < date2


@purchase_app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@purchase_app.route('/', methods=['GET'])
@login_required(flask.session)
@role_required(flask.session)
def purchase_handler_index():
    return flask.render_template("rent_menu.html")


@purchase_app.route('/availability', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def availability_handler():
    if request.method == 'GET':
        return flask.render_template('rent.html', action='view')

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        final_date = request.form.get('final_date')
        if not check_dates(start_date, final_date):
            return flask.render_template('rent.html', action='view',
                                         error_message='Неправильно выбран диапазон дат')

        return flask.redirect(url_for('purchase_app.show_availability_handler', start=start_date, end=final_date))


@purchase_app.route('/availability/show', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def show_availability_handler():
    # global start_date, final_date, result, reserved_billboards
    global reserved_billboards

    if request.method == 'GET':
        start_date = request.args.get('start')
        final_date = request.args.get('end')
        flask.session['start_date'] = start_date
        flask.session['final_date'] = final_date

        sql_statement = sql_provider.get('date_view', {'start': start_date, 'end': final_date})
        result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
        flask.session['result'] = result
        return flask.render_template('choose_billboards.html', result=result, date_from=start_date,
                                     date_to=final_date, reserved_bilb=reserved_billboards)

    if request.method == 'POST':
        selected_billboard = {'bill_id': request.form.get('bill_id'), 'price': int(request.form.get('price')),
                              'install_address': request.form.get('install_address'), 'size': request.form.get('size'),
                              'quality': request.form.get('quality')}

        if 'basket' not in flask.session:
            flask.session['basket'] = []

        button_clicked = request.form.get('button_action')
        global aso

        if button_clicked == 'add':
            # добавляем в сессию
            flask.session['basket'].append(selected_billboard)
            aso.append(selected_billboard)

            if int(selected_billboard['bill_id']) not in reserved_billboards:
                reserved_billboards.append(int(selected_billboard['bill_id']))

        if button_clicked == 'remove':
            # убираем из сессии
            if selected_billboard in flask.session['basket']:
                flask.session['basket'].remove(selected_billboard)

            aso.remove(selected_billboard)
            reserved_billboards.remove(int(selected_billboard['bill_id']))

        return flask.render_template('choose_billboards.html', result=flask.session['result'],
                                     date_from=flask.session['start_date'],
                                     date_to=flask.session['final_date'], reserved_bilb=reserved_billboards)


@purchase_app.route('/basket', methods=['GET', 'POST'])
@login_required(flask.session)
@role_required(flask.session)
def basket_handler():
    if request.method == 'POST':
        button_clicked = request.form.get('button_action')
        if button_clicked == 'remove':
            selected_billboard = {'bill_id': request.form.get('bill_id'), 'price': int(request.form.get('price')),
                                  'install_address': request.form.get('install_address'),
                                  'size': request.form.get('size'),
                                  'quality': request.form.get('quality')}
            print(selected_billboard)
            global aso
            if selected_billboard in flask.session['basket']:
                flask.session['basket'].remove(selected_billboard)

            aso.remove(selected_billboard)
            reserved_billboards.remove(int(selected_billboard['bill_id']))
        if button_clicked == 'checkout':

            sql_statement = sql_provider.get('get_contract_id', {'login': flask.session['user']})
            res = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
            contract_id = res[0]['contract_id']
            transaction_sqls = []
            print(aso)

            # создаем запись в orders
            transaction_sqls.append(
                sql_provider.get(
                    'create_order',
                    {
                        'date_of_issue': datetime.now().strftime('%Y-%m-%d'),
                        'order_price': calculate_total(aso, flask.session['start_date'], flask.session['final_date']),
                        'contract_id': contract_id
                    }
                )
            )
            execute_transaction(flask.current_app.config['MYSQL_DB_CONFIG'], transaction_sqls)
            transaction_sqls = []

            # получаем его айди
            sql_statement = sql_provider.get('get_last_order_id', {})
            result = select_from_DB(flask.current_app.config['MYSQL_DB_CONFIG'], sql_statement)
            order_id = result[0]['order_id']

            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(flask.session['start_date'], date_format)
            final_date = datetime.strptime(flask.session['final_date'], date_format)
            date_difference = (final_date - start_date).days

            # формируем транзакцию в таблицу order_line
            for billboard in aso:
                transaction_sqls.append(
                    sql_provider.get(
                        'insert_order_line',
                        {
                            'start': flask.session['start_date'],
                            'end': flask.session['final_date'],
                            'bill_id': billboard['bill_id'],
                            'order_id': order_id,
                            'bill_rent_price': billboard['price'] * date_difference  # коррекция стоимости
                        }
                    )
                )

            # формируем транзакцию в таблицу schedule
            for billboard in aso:
                transaction_sqls.append(
                    sql_provider.get(
                        'add_schedule',
                        {
                            'start': flask.session['start_date'],
                            'end': flask.session['final_date'],
                            'bill_id': billboard['bill_id'],
                            'contract_id': contract_id,
                        }
                    )
                )

            # отправляем транзакцию
            execute_transaction(flask.current_app.config['MYSQL_DB_CONFIG'], transaction_sqls)
            aso.clear()
            reserved_billboards.clear()
            return flask.render_template('basket.html', cart_items=aso, order_id=order_id)

    basket_items = flask.session.get('basket', [])
    total = calculate_total(aso, flask.session['start_date'], flask.session['final_date'])
    return flask.render_template('basket.html', cart_items=aso, total=total, basket_items=basket_items)
