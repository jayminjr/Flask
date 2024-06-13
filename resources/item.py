from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel, StoreModel, TagModel
from schemas import (
    ItemSchema,
    ItemUpdateSchema,
    PlainItemSchema,
    PlainStoreSchema,
    PlainTagSchema,
    StoreSchema,
)

iblp = Blueprint("Items", __name__, description="Item operation")


@iblp.route("/item/<int:id>")
class Item(MethodView):
    @jwt_required()
    @iblp.response(200, ItemSchema)
    def get(self, id):
        try:
            item = ItemModel.query.get_or_404(id)
            return item
        except KeyError:
            return {"message": "item not found"}

    @jwt_required()
    @iblp.arguments(ItemUpdateSchema)
    @iblp.response(200, ItemSchema)
    def put(self, item_data, id):
        item = ItemModel.query.get(id)
        if item:
            item.name = item_data.get("name")
            item.price = item_data.get("price")
        else:
            item = ItemModel(id=id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item

    @jwt_required()
    def delete(self, id):
        try:
            item = ItemModel.query.get_or_404(id)
            db.session.delete(item)
            db.session.commit()
            return {"message": "Item deleted."}
        except SQLAlchemyError:
            abort(500, message="Error while deleting item")


@iblp.route("/item/")
class ItemListView(MethodView):
    @jwt_required()
    @iblp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @iblp.arguments(ItemSchema)
    @iblp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error while storing item data")
        return item


@iblp.route("/all")
@jwt_required()
def return_all_data():
    stores = StoreModel.query.all()
    store_schema = PlainStoreSchema()
    stores_json = store_schema.dump(obj=stores, many=True)

    items = ItemModel.query.all()
    item_schema = PlainItemSchema()
    items_json = item_schema.dump(obj=items, many=True)

    tags = TagModel.query.all()
    tags_schema = PlainTagSchema()
    tagss_json = tags_schema.dump(obj=tags, many=True)

    return {"stores": stores_json, "items": items_json, "tags": tagss_json}
