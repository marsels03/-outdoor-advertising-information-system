import flask
import json

from selects.selects import selects_app
from auth.auth import auth_app
from reports.reports import reports_app
from purchase.purchase import purchase_app


app = flask.Flask(__name__)
app.secret_key = 'xnjpfabuyzdjj,ot'
app.config['MYSQL_DB_CONFIG'] = json.load(open('configs/db_config.json'))
app.config['reports_list'] = json.load(open('configs/reports.json'))

app.register_blueprint(selects_app, url_prefix='/selects')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(reports_app, url_prefix='/reports')
app.register_blueprint(purchase_app, url_prefix='/purchase')


@app.route('/')
def handler_index():
    message = None
    if flask.request.args:
        message = flask.request.args.get('error')

    role = flask.session['role'] if flask.session else None
    return flask.render_template('index.html',  role=role, message=message)


if __name__ == '__main__':
    settings = {'host': '127.0.0.1', 'port': 5000}
    app.run(host=settings['host'], port=settings['port'], debug=True)