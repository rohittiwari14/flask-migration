from flask import request, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import User

routes_bp = Blueprint("routes", __name__)


@routes_bp.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    try:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            if not email or not password:
                return jsonify({"error": "Email and Password are required"}), 400
            user = User.query.filter_by(email=email).first()
            if user is None:
                return jsonify({"error": "Invalid email ID."}), 400
            elif not check_password_hash(user.password, password):
                return jsonify({"error": "Incorrect Password"}), 400
            else:
                return jsonify({"message": "Sign-In Successful."}), 200
        return jsonify({"message": "Welcome to Sign-In."})

    except Exception as e:
        return jsonify({"error": "An error occurred during Sign-In", "details": str(e)})


@routes_bp.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        try:
            new_user = User(
                name=request.form.get('name'),
                mobile_no=request.form.get('mobile'),
                email=request.form.get('email'),
                password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8),
                age=request.form.get('age'),
                address=request.form.get('address')
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User Created Successfully"}), 200

        except Exception as e:
            return jsonify({"error": "An error occurred during Sign-In", "details": str(e)})
    return jsonify({"message": "Welcome to Sign-Up"})
