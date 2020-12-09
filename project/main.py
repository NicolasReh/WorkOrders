from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import Workorder, Part
from datetime import datetime
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/wo', methods=['POST', 'GET'])
@login_required
def wo():
    if request.method == 'POST':
        wo_date = datetime.strptime(request.form['date_required'], '%Y-%m-%d')
        wo_client = request.form['client']
        wo_title = request.form['title']
        new_wo = Workorder(date_required=wo_date, user=current_user.name, client=wo_client, title=wo_title)

        try:
            db.session.add(new_wo)
            db.session.commit()
            return redirect('/wo')
        except Exception as e:
            print(e)
            return "Error al agregar orden de trabajo."

    else:
        wos = Workorder.query.order_by(Workorder.id).all()
        return render_template('workorders.html', wos=wos, today=datetime.utcnow())

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    wo_to_delete = Workorder.query.get_or_404(id)

    try:
        db.session.delete(wo_to_delete)
        db.session.commit()
        return redirect('/wo')
    except Exception as e:
        print(e)
        return "Error al borrar la orden de trabajo"

@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    wo_to_update = Workorder.query.get_or_404(id)
    if request.method == 'POST':
        date = request.form['date_required']
        if date:
            wo_to_update.date_required = datetime.strptime(date, '%Y-%m-%d')
        wo_to_update.user = current_user.name

        try:
            db.session.commit()
            return redirect('/wo')
        except Exception as e:
            print(e)
            return "Error al actualizar la orden de trabajo"
    else:
        return render_template('update.html', wo=wo_to_update)

@main.route('/wo/<int:id>/parts', methods=['POST', 'GET'])
@login_required
def part(id):
    wo = Workorder.query.get_or_404(id)
    if request.method == 'POST':
        new_part = Part()
        new_part.name = request.form['name']
        new_part.code = request.form['code']
        new_part.qty = request.form['qty']
        new_part.user = current_user.name
        new_part.wo_id = wo.id

        try:
            db.session.add(new_part)
            db.session.commit()
            return redirect(f'/wo/{wo.id}/parts')
        except Exception as e:
            print(e)
            return "Error al agregar parte."

    else:
        parts = wo.parts
        return render_template('parts.html', parts=parts, wo=wo)

@main.route('/delete_part/<int:id>')
@login_required
def delete_part(id):
    part_to_delete = Part.query.get_or_404(id)

    try:
        db.session.delete(part_to_delete)
        db.session.commit()
        return redirect(f'/wo/{part_to_delete.wo_id}/parts')
    except Exception as e:
        print(e)
        return "Error al borrar la orden de trabajo"

@main.route('/update_part/<int:id>', methods=['GET', 'POST'])
@login_required
def update_part(id):
    part_to_update = Part.query.get_or_404(id)
    if request.method == 'POST':
        part_to_update.name = request.form['name']
        part_to_update.code = request.form['code']
        part_to_update.qty = request.form['qty']
        part_to_update.finished = True if request.form.get('finished') == "finished" else False
        print(request.form.get('finished'))
        part_to_update.user = current_user.name

        try:
            db.session.commit()
            return redirect(f'/wo/{part_to_update.wo_id}/parts')
        except Exception as e:
            print(e)
            return "Error al actualizar la pieza"
    else:
        return render_template('update_part.html', part=part_to_update)