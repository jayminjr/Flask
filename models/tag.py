from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(88), unique=True, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.Relationship("StoreModel", back_populates="tags")
    items = db.Relationship("ItemModel", back_populates="tags", secondary="items_tags")
