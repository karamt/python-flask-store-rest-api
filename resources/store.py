
from flask.views import MethodView
from flask_smorest import Blueprint,abort

from models import StoreModel

from db import db

from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from schemas import StoreSchema,StoreUpdateSchema

blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="Error deleting store")
        return {"message": "Store Deleted successfuly"}


    @blp.arguments(StoreUpdateSchema)
    @blp.response(200,StoreSchema)
    def put(self,store_data,store_id):
        store = StoreModel.query.get(store_id)

        if store:
            store.name = store_data["name"]
        else:
            store = StoreModel(id=store_id,**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while updating the store")
        
        return store
        

@blp.route("/store")
class Store(MethodView):
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Another store already exists with same name")
        except SQLAlchemyError:
            abort(500, message="An error has occured while inserting store")

        return store
      
        