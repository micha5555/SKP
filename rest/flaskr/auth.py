import functools

from flask import (
    Blueprint,
    flash, 
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for
)
from flaskr.db import get_db, select_user_by_id, add_user


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = select_user_by_id(id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                add_user(db, username, password)
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("index"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))