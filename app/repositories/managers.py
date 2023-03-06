from ast import Tuple
from collections import Counter
from typing import Any, List, Optional, Sequence
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text, column

from .models import (
    Ingredient,
    Order,
    OrderDetail,
    Size,
    Beverage,
    BeverageOrderDetail,
    db,
)
from .serializers import (
    IngredientSerializer,
    OrderSerializer,
    SizeSerializer,
    BeverageSerializer,
    ma,
)

from sqlalchemy import func, desc

class BaseManager:
    model: Optional[db.Model] = None
    serializer: Optional[ma.SQLAlchemyAutoSchema] = None
    session = db.session

    @classmethod
    def get_all(cls):
        serializer = cls.serializer(many=True)
        _objects = cls.model.query.all()
        result = serializer.dump(_objects)
        return result 

    @classmethod
    def get_by_id(cls, _id: Any):
        entry = cls.model.query.get(_id)
        return cls.serializer().dump(entry)

    @classmethod
    def create(cls, entry: dict):
        serializer = cls.serializer()
        new_entry = serializer.load(entry)
        cls.session.add(new_entry)
        cls.session.commit()
        return serializer.dump(new_entry)

    @classmethod
    def update(cls, _id: Any, new_values: dict):
        cls.session.query(cls.model).filter_by(_id=_id).update(new_values)
        cls.session.commit()
        return cls.get_by_id(_id)


class SizeManager(BaseManager):
    model = Size
    serializer = SizeSerializer


class IngredientManager(BaseManager):
    model = Ingredient
    serializer = IngredientSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class BeverageManager(BaseManager):
    model = Beverage
    serializer = BeverageSerializer

    @classmethod
    def get_by_id_list(cls, ids: Sequence):
        return (
            cls.session.query(cls.model).filter(cls.model._id.in_(set(ids))).all() or []
        )


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(
        cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]
    ):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all(
            (
                OrderDetail(
                    order_id=new_order._id,
                    ingredient_id=ingredient._id,
                    ingredient_price=ingredient.price,
                )
                for ingredient in ingredients
            )
        )
        cls.session.add_all(
            (
                BeverageOrderDetail(
                    order_id=new_order._id,
                    beverage_id=beverage._id,
                    beverage_price=beverage.price,
                )
                for beverage in beverages
            )
        )
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f"Method not suported for {cls.__name__}")


class IndexManager(BaseManager):
    @classmethod
    def test_connection(cls):
        cls.session.query(column("1")).from_statement(text("SELECT 1")).all()

class ReportManager(BaseManager):
    order_model = Order
    ingredient_model = OrderDetail
    session = db.session

    @classmethod
    def get_most_requested_ingredient(cls) -> dict:

        count_ingredients_in_order = aliased(cls.session.query(func.count(Ingredient._id).label('ingredient_id'), OrderDetail, Ingredient).\
                                        filter(Ingredient._id == OrderDetail.ingredient_id).\
                                        group_by(Ingredient._id).subquery())
        
        most_requested_ingredient = cls.session.query(func.max(count_ingredients_in_order.c.ingredient_id), count_ingredients_in_order.c.name).first()
        
        if most_requested_ingredient is None:
            return {"name": None, "times": None}
        
        response: list = [{
                'name': most_requested_ingredient[1],
                'times': most_requested_ingredient[0]
        } ]

        return response


    @classmethod
    def get_month_with_more_revenue(cls):
        month_with_more_revenue = cls.session.query(func.sum(Order.total_price).label('total_price'), func.strftime("%m", Order.date).label('month')).\
                                                    group_by(func.strftime("%m", Order.date)).\
                                                    order_by(desc('total_price')).first()
        if month_with_more_revenue is None:
            return {"revenue": None, "month": None}
        return {
                "month": month_with_more_revenue.month,
                "revenue": round(month_with_more_revenue.total_price, 2)                
            }
    

    @classmethod
    def get_best_customers(cls):
        best_customers = [row for row in cls.session.query(func.sum(Order.total_price).label('total_price'), Order.client_name,  Order.client_dni).\
                                                    group_by(Order.client_name).\
                                                    order_by(desc('total_price')).limit(3).offset(0).all()]
        response: list = [{
                'total_purchase': round(customer[0], 2),
                'name': customer[1],
                'dni': customer[2]
        } for customer in best_customers ]

        return response
    