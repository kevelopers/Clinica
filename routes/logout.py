from flask import Blueprint, redirect, url_for, session

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    # Redirect to the login page
    return redirect(url_for('auth.login'))
