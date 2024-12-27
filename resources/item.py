from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from schemas import ItemSchema,ItemUpdateSchema

from flask_jwt_extended import jwt_required,get_jwt

from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from models import ItemModel

from db import db

blp = Blueprint("items", __name__, description="Operation on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,item_id):
        # try:
        #     return items[item_id],200
        # except:
        #     abort(404,message="Item not found.")
        item = ItemModel.query.get_or_404(item_id)
        return item


    @jwt_required(fresh=True)
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="Admin previleges needed for this operation")
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error has occured while deleting item")
        return {"message": "Item Deleted successfuly"}
        # try:
        #     del items[item_id]
        #     return {"message": "Item deleted successfully"}
        # except KeyError:
        #     abort(404,message="Item not found.")

    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200,ItemSchema)
    def put(self,item_data,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="Admin previleges needed for this operation")
        
        item = ItemModel.query.get(item_id)

        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:
            item = ItemModel(id=item_id,**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while updating the item")
        return item
       

@blp.route("/item")
class Item(MethodView):
    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        # return items.values()
        return ItemModel.query.all()


    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401,message="Admin previleges needed for this operation")
            
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(500, message="Item with same name already exists")
        except SQLAlchemyError:
            abort(500, message="An error has occured while insterting Item")

        return item
    
    