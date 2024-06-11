from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema

ublp = Blueprint("Users", __name__, description="User operation")


@ublp.route("/register")
class UserRegister(MethodView):
    @ublp.response(201, UserSchema)
    @ublp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data.get("username")
        ).first():
            abort(409, message="Username already exists")

        username = user_data.get("username")
        password = pbkdf2_sha256.hash(user_data.get("password"))

        user = UserModel(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while adding user")

        return user


@ublp.route("/user/<int:user_id>")
class UserList(MethodView):
    @ublp.response(201, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @ublp.response(200, UserSchema)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro while deleting user")
        return {"message": "User deleted"}


@ublp.route("/login")
class UserLogin(MethodView):
    @ublp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid creds")


@ublp.route("/logout")
class UserLogin(MethodView):
    @jwt_required()
    def post(self):
        jwt = get_jwt()["jti"]
        BLOCKLIST.add(jwt)
        return {"message": "Logout !"}


@ublp.route("/refresh")
class UserLogin(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        jwt = get_jwt()["jti"]
        BLOCKLIST.add(jwt)
        return {"access_token": access_token}
