
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from bankt.db import get_db
from bankt.auth import login_required


bp = Blueprint('logged', __name__, url_prefix='/logged')

@bp.route('/start', methods=('GET',))
@login_required
def start():
	id = session.get('user_id')
	user = get_db().execute(
		'SELECT username FROM user WHERE id = ?', (id,)
	).fetchone()
	return render_template('logged/start.html', user=user)
#	return '<h3> Wtiaj {} w swoim banku'.format(user['username'])


@bp.route('/transfer', methods=('GET', 'POST'))
@login_required
def transfer():
	if request.method == 'POST':
		reciever = request.form['reciever']
		account_no = request.form['account_no']
		amount = request.form['amount']
		title = request.form['title']
		error = None

		if not reciever:
			error = 'reciever name is required.'
		elif not account_no:
			error = 'account number is required.'
		elif not amount:
			error = 'amount is required.'
		elif not title:
			error = 'title is required.'

		if not account_no.isnumeric():
			error = 'Account number must contain only digits'
		elif len(account_no) != 4:
			error = 'Wrong account number'

		#add amount validation

		transfer_data = {
			'reciever': reciever,
			'account_no': account_no,
			'amount': amount,
			'title': title
		}
		session['transfer_data'] = transfer_data

		if error is None:
			return redirect(url_for('logged.accept'))

		flash(error)

	return render_template('logged/transfer.html')

@bp.route('/accept', methods=('GET', 'POST',))
@login_required
def accept():
	if request.method == 'POST':
		error = None

		sender_id = session.get('user_id')

		account_no = request.form['account_no']
		amount = request.form['amount']
		title = request.form['title']
		

		if error is None:
			db = get_db()
			db.execute(
				'INSERT INTO transfers (sender_id, account_no, amount, title) VALUES (?, ?, ?, ?)',
				(sender_id, account_no, amount, title) 
			)
			db.commit()
			session.pop('transfer_data', None)
			return redirect(url_for('logged.accepted'))

		flash(error)

	transfer_data = session.get('transfer_data')
	return render_template('logged/accept.html', data=transfer_data)

@bp.route('/accepted', methods=('GET',))
@login_required
def accepted():
	error = None
	user_id = session.get('user_id')
	db = get_db()
	transfer_data = db.execute('SELECT * FROM transfers WHERE sender_id == ? ORDER BY id DESC LIMIT 1', (user_id,) ).fetchone()

	return render_template('logged/accepted.html', data=transfer_data)


@bp.route('/history', methods=('GET',))
@login_required
def history():
	user_id = session.get('user_id')
	db = get_db()
	transfers = db.execute(
		'SELECT title, account_no, amount FROM transfers WHERE sender_id == ? ORDER BY id DESC',
		(user_id,)
	).fetchall()
	return render_template('logged/history.html', transfers=transfers)

