from fastapi import APIRouter, Depends, HTTPException, Query, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.stall import Stall
from schema.stall import StallCreate, ListStallResponse, UpsertStallResponse, UpdateStall
from uuid import UUID
from http import HTTPStatus
# import os
# import boto3
# import io
router = APIRouter()

# S3_BUTCKET_NAME = os.getenv('S3_BUTCKET_NAME', 'food-bucket-12345')
# S3_REGION = os.getenv('S3_REGION', 'us-east-1')

# # Init S3 client
# s3_client = boto3.client("s3", region_name=S3_REGION)

# @router.get('/search?q={queryString}', response_model=ListStallResponse)
# def search_stall_by_name(
#     limit:int = Query(10, ge=1, le=100),
#     offset:int = Query(0, ge=0),
#     querystring:str = '',
#     db:Session = Depends(get_db)
# ):
    
#     return ''


@router.get('', response_model=ListStallResponse)
def list_stall(
    limit: int = Query(10, ge=1, le=100),
    offset:int = Query(0, ge=0),
    querystring:str = '',
    db:Session = Depends(get_db)
    ):
    base_query = db.query(Stall)
    total = base_query.filter(Stall.is_deleted == False).count()
    
    if querystring:
        querystring = f'%{querystring}%'
        base_query = (
            base_query
            .filter(
                or_(
                    Stall.stall_name.ilike(querystring),
                    Stall.stall_type.ilike(querystring)
                )
            )
        )
    
    stalls =(
        base_query
        .filter(Stall.is_deleted == False)
        .order_by(Stall.display_order)
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    return {
        "status_code": HTTPStatus.OK if len(stalls) > 1 else HTTPStatus.OK,
        "message": 'Stall fetched successfully' if len(stalls) > 1 else 'No records found',
        "data": stalls,
        "pagination":{
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }
    
@router.post('', response_model=UpsertStallResponse)
def create_stall(
    stall:StallCreate,
    db:Session = Depends(get_db)
)->UpsertStallResponse:
    
    # new_stall = Stall(                    # This will work too but below statement is more optimized
    #     stall_name = stall.stall_name,
    #     stall_type = stall.stall_type,
    #     status = stall.status,
    #     display_order = stall.display_order,
    #     stall_image = stall.stall_image,
    #     contact_name = stall.contact_name,
    #     stall_area = stall.stall_area,
    #     open_at = stall.open_at,
    #     close_at = stall.close_at,
    #     stall_number = stall.stall_number,
    #     discount = stall.discount
    # )
    new_stall = Stall(**stall.model_dump())   # Works only when - Schema fields == Model fields and No extra request-only fields
    db.add(new_stall)
    db.commit()
    db.refresh(new_stall)
    
    return UpsertStallResponse(
        status_code=HTTPStatus.CREATED,
        message="Stall created successfully",
        data=new_stall
    )


@router.get('/{stall_id}', response_model= UpsertStallResponse)
def get_stall_by_id(
    stall_id: UUID, 
    db:Session = Depends(get_db)
) -> UpsertStallResponse:
    
    response_stall = db.query(Stall).filter(Stall.id == stall_id, Stall.is_deleted== False).first()
    if not response_stall:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Stall not found"
        )
    
    return UpsertStallResponse(
        status_code=HTTPStatus.OK,
        message="Stall updated successfully",
        data=response_stall
    )


@router.put('/{stall_id}', response_model = UpsertStallResponse)
def update_stall_by_id(
    stall_id: UUID,
    stall: UpdateStall,
    db: Session = Depends(get_db)
) -> UpsertStallResponse:
    
    # Fetch existing stall
    existed_stall = db.query(Stall).filter(Stall.id == stall_id).first()
    
    if not existed_stall:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Stall not found")
    
    # Update only provided fields
    update_data = stall.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existed_stall, field, value)
        
    # Save changes
    db.commit()
    db.refresh(existed_stall)
    
    # Return Wrapped response
    return UpsertStallResponse(
        status_code=HTTPStatus.OK,
        message='Stall updated successfully',
        data = existed_stall
    )
    

@router.delete("/{stall_id}")
def delete_stall_by_id(
    stall_id: UUID,
    db:Session = Depends(get_db)
):
    existed_stall = db.query(Stall).filter(Stall.id == stall_id).first()
    
    if not existed_stall:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Stall not existed'
        )
    setattr(existed_stall, 'is_deleted', True)
    
    db.commit()
    db.refresh(existed_stall)
    
    return {
        "status_code": HTTPStatus.OK,
        "message": "Stall record deleted!"
    }
    
# @router.post('/upload') 
# async def upload_files(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
    
#     try:
#         contents  = await file.read()
#         temp_file = io.BytesIO(contents)
#         temp_file.seek(0)
        
#         s3_client.upload_fileObj(
#             temp_file,
#             S3_BUTCKET_NAME,
#             file.filename
#         )
#     except Exception as e:
#         print(e)
#         raise HTTPException(status_code=500, detail=f"An Error occured during upload into S3")
#     finally:
#         await file.close()
#         temp_file.close()
#     return {"filename": file.filename}