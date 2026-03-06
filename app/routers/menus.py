from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from uuid import UUID
from models.menu import Menu
from schema.menu import MenuUpsertResponse, MenuCreate, MenuUpdate
from http import HTTPStatus

router = APIRouter()

@router.get('/{stall_id}')
def list_menu_by_stallid(
    stall_id: UUID,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    
    base_query = db.query(Menu).filter(Menu.stall_id == stall_id)
    menu_list = (
            base_query
            .filter(Menu.is_deleted==False)
            .order_by(Menu.updated_at)
            .limit(limit)
            .offset(offset)
        )
    
    total = base_query.count()
    menu_items = menu_list.all()
        
    return {
        "status_code": HTTPStatus.OK if len(menu_items) > 1 else HTTPStatus.NO_CONTENT,
        "message": 'Menu listsed successfully' if len(menu_items) > 1 else 'No records found',
        "data": menu_items,
        'next_offset': offset + limit if len(menu_items) == limit else None,
        "pagination":{
            "total": total,
            "limit": limit,
            "offset" : offset
        }
    }


@router.post("/")
def create_menu(
    menu_item:MenuCreate,
    db: Session = Depends(get_db)
)-> MenuUpsertResponse:
    
    new_menu_item = Menu(**menu_item.model_dump())
    db.add(new_menu_item)
    db.commit()
    db.refresh(new_menu_item)
    
    return MenuUpsertResponse(
        status_code=HTTPStatus.CREATED,
        message="Menu item created",
        data=new_menu_item
    )
    

@router.put('/{id}')
def update_menu_item(
    id: UUID,
    menu_item: MenuUpdate,
    db:Session = Depends(get_db)
) ->MenuUpsertResponse:
    
    existed_item = db.query(Menu).filter(Menu.id == id, Menu.is_deleted== False).first()
    
    if not existed_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    updated_item = menu_item.model_dump(exclude_unset=True)
    for col, val in updated_item.items():
        setattr(existed_item, col, val)
    
    db.commit()
    db.refresh(existed_item)
    
    return MenuUpsertResponse(
        status_code=HTTPStatus.OK,
        message="Menu item updated successfully",
        data=existed_item
    )
    
@router.delete('/{id}')
def menu_item_delete(
    id: UUID,
    db:Session = Depends(get_db)
):
    existed_item = db.query(Menu).filter(Menu.id == id).first()
    if not existed_item:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Menu item not found'
        )
    
    setattr(existed_item,'is_deleted',True)
    db.commit()
    db.refresh(existed_item)
    
    return {
        "status_code": HTTPStatus.OK,
        "message":"Menu Item deleted successfully!"
    }