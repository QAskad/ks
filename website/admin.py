from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User
from . import db

admin = Blueprint('admin', __name__)

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.email != 'admin@gmail.com':
            flash("Sorry, you cannot access this page", category='error')
            return redirect(url_for('views.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin')
@admin_required
def admin_panel():
    users = User.query.all()  
    return render_template('admin.html', users=users)

@admin.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted!', category='success')
    else:
        flash('User not found.', category='error')
        
    users = User.query.all()  
    return render_template('admin.html', users=users)
    
