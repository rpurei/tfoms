#!python
#cython: language_level=3, always_allow_keywords=True
from app.config import LOCAL_DATABASE_URI

from flask import request, render_template, current_app, flash, Blueprint
from flask_login import login_required, current_user
from datetime import datetime
from calendar import monthrange
from sqlalchemy import create_engine, text

opt_handler = Blueprint('opt', __name__)


@login_required
@opt_handler.route('/reports', methods=['GET', 'POST'])
def show_report():
    login = ''
    result_list = []
    result_header = ['Статус', 'Количество']
    start_date = ''
    end_date = ''
    dt = datetime.now().strftime('%d.%m.%Y')
    dt_month = str(dt.split('.')[1])
    dt_year = dt.split('.')[2]
    dt_first_day = '01'
    dt_last_day = str(monthrange(int(dt_year), int(dt_month))[1])
    if current_user.is_authenticated:
        login = current_user.name
    try:
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            if start_date == '':
                start_date = f'{dt_year}-{dt_month}-{dt_first_day}'
            if end_date == '':
                end_date = f'{dt_year}-{dt_month}-{dt_last_day}'
        elif request.method == 'GET':
            start_date = f'{dt_year}-{dt_month}-{dt_first_day}'
            end_date = f'{dt_year}-{dt_month}-{dt_last_day}'
        database_engine = create_engine(LOCAL_DATABASE_URI, echo=False)
        with database_engine.connect() as conn:
            result = conn.execute(text(f"""SELECT trans_status,count(1) 
                                           FROM transactions 
                                           WHERE trans_date>="{start_date}" 
                                           AND trans_date<="{end_date}" 
                                           GROUP BY trans_status"""))
            for row in result:
                result_list.append((row[0], row[1]))
        return render_template('reports.html', login=login, result_report=result_list, result_header=result_header,
                               start_date=start_date, end_date=end_date)
    except Exception as err:
        current_app.logger.critical(str(err))
        flash(f'Ошибка: {str(err)}', 'danger')
        return render_template('500.html')
