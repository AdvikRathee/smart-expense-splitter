from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.GroupResponse, summary="Create a new group")
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    new_group = models.Group(name=group.name, description=group.description)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("/", response_model=list[schemas.GroupResponse], summary="List all groups")
def list_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()


@router.get("/{group_id}", response_model=schemas.GroupResponse, summary="Get group by ID")
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.post("/{group_id}/members", response_model=schemas.MemberResponse, summary="Add member to group")
def add_member(group_id: int, member: schemas.MemberCreate, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    new_member = models.Member(name=member.name, group_id=group_id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@router.get("/{group_id}/members", response_model=list[schemas.MemberResponse], summary="List members of a group")
def list_members(group_id: int, db: Session = Depends(get_db)):
    return db.query(models.Member).filter(models.Member.group_id == group_id).all()


@router.delete("/{group_id}", summary="Delete a group")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"message": f"Group '{group.name}' deleted successfully"}
