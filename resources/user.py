from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt,
    create_refresh_token,
    get_jwt_identity)
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from passlib.hash import pbkdf2_sha256

from db import db
from blocklist import BLOCKLIST
from models.user import UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operation on users")

@blp.route("/user")
class User(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    def post(self,user_data):
        # if(UserModel.query.filter(UserModel.username==user_data["username"]).first()):
        #     abort(409,message="Another User with same name already exist")
        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400,message="User already exist")
        except SQLAlchemyError:
            abort(500,message="An error has occured while creating the user")
        return {"message": "User created successfuly"},201

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @blp.response(200)
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error has occured while deleting the user")
        return {"message": "User deleted successfuly"}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(UserModel.username==user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {"access_token": access_token,
                    "refresh_token": refresh_token}
        
        return {"message": "Invalid Credentials"}
    
@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
    
@blp.route("/refresh")
class RefreshToken(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        # Here only one refresh token is allowed
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}


         
    


