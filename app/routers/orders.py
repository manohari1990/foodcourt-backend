from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from models.order import Order
from models.order_item import OrderItem
from models.menu import Menu
from http import HTTPStatus
from schema.order import OrderCreate, UpsertOrderResponse, OrderUpdate, OrderResponse
from decimal import Decimal

router = APIRouter()

@router.get('/')
def list_orders(
    limit:int = Query(10, ge=1, le=100),
    offset:int = Query(0, ge=0),
    db:Session = Depends(get_db)
):
    
    base_query = db.query(Order)
        
    total = base_query.count()
    
    list_query = (
        base_query
        .order_by(Order.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    
    
    return {
        "status_code": HTTPStatus.OK,
        "message": "List successfully!",
        "data": list_query,
        "pagination":{
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }


@router.get('/{id}')
def get_order_by_id(
    id: UUID,
    db:Session = Depends(get_db)
) -> UpsertOrderResponse:
    existed_order = db.query(Order).filter(Order.id == id).first()
    if not existed_order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order could not be found!")
    
    return UpsertOrderResponse(
        status_code=HTTPStatus.OK,
        message="Order found!",
        data=existed_order
    )

@router.post("/")
def create_order(
    order: OrderCreate,
    db:Session = Depends(get_db)
) -> UpsertOrderResponse:
    
    new_order = Order(
        table_number = order.table_number,
        stall_id = order.stall_id,
        order_status = order.order_status,
        payment_status = order.payment_status,
        total_payment = order.total_payment,
        estimated_time = order.estimated_time
    )
    total_payment = 0
    order_items = []
    for row in order.items:
        
        menu_item = db.query(Menu).filter(Menu.id==row.item_id).first()
        if not menu_item:
            continue

        item_discount = menu_item.price * (menu_item.discount/Decimal(100))
        
        item_price_with_discount = menu_item.price-item_discount
        item_price = row.quantity * item_price_with_discount
        
        ordered_item_model = OrderItem(
            item_id = row.item_id,
            quantity = row.item_id,
            price_at_order_time = item_price
        )
        order_items.append(ordered_item_model)
        
        total_payment += item_price_with_discount
    
    setattr(new_order, 'total_payment', total_payment)
    
    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        for row in order_items:
            row.order_id = new_order.id
            print(row.order_id)
        db.bulk_save_objects(order_items)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to create order!"
        )
    
    return UpsertOrderResponse(
        status_code=HTTPStatus.CREATED,
        message="Order created successfully!",
        data=new_order
    )
    
    
@router.put('/{id}')
def update_order(
    id: UUID,
    update_order: OrderUpdate,
    db:Session = Depends(get_db)
) ->UpsertOrderResponse | dict:
    
    existed_order = db.query(Order).filter(Order.id == id).first()
    
    if not existed_order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order could not be found!")
    
    try:
        updated_order = update_order.model_dump(exclude_unset=True)
        for field, value in updated_order.items():
            setattr(existed_order, field, value)
            
        db.commit()
        db.refresh(existed_order)
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Failed to update the order!'
        )
    
    return UpsertOrderResponse(
        status_code=HTTPStatus.OK,
        message="Order updated Successfully",
        data= existed_order
    )
    
@router.delete("/{id}")
def delete_order(
    id: UUID,
    db:Session = Depends(get_db)
):
    
    exited_order = db.query(Order).filter(Order.id == id).first()
    
    if not exited_order:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Order could not be found!")
    
    try:
        db.delete(exited_order)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Failed to delete the order!"
        )
    return {
        "status_code": HTTPStatus.OK,
        "message": "Order deleted successfully!"
    }