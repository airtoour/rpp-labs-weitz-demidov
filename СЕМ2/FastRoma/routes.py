from config import app
from flask import render_template
from models import OperationsForm, Operations

@app.route('/find_descr', methods=['GET', 'POST'])
def find_descr():
    form = OperationsForm()

    if form.validate_on_submit():
        id = form.id.data
        oper = Operations.query.get(id)

        if oper:
            result = f'Результат: {oper.description}'
        else:
            result = f'Операция с ID {id} не найдена'

        return render_template('return_description.html', form=form, result=result)

    return render_template('return_description.html', form=form)