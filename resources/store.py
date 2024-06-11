from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

sblp = Blueprint("Stores", __name__, description="Store operation")


@sblp.route("/store/<int:id>")
class Store(MethodView):
    @jwt_required()
    @sblp.response(200, StoreSchema)
    def get(self, id):
        try:
            store = StoreModel.query.get_or_404(id)
            return store
        except KeyError:
            return {"message": "Store not found"}

    @jwt_required()
    @sblp.arguments(StoreUpdateSchema)
    @sblp.response(200, StoreSchema)
    def put(self, store_data, id):
        store = StoreModel.query.get(id)
        if store:
            if store_data.get("name"):
                store.name = store_data.get("name")
            if store_data.get("city"):
                store.city = store_data.get("city")
        else:
            store = StoreModel(id=id, **store_data)
        db.session.add(store)
        db.session.commit()
        return store

    @jwt_required()
    def delete(self, id):
        try:
            store = StoreModel.query.get(id)
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted."}
        except SQLAlchemyError:
            abort(500, message="Erro while deleting store")


@sblp.route("/store/")
class StoreListView(MethodView):
    @jwt_required()
    @sblp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @sblp.arguments(StoreSchema)
    @sblp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Erro while adding store")

        return store
