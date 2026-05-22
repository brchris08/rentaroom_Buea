from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from backend.database import get_db
from backend.models.schemas import Listing, ListingImage
from pydantic import BaseModel, ConfigDict

router = APIRouter()


class ImageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    image_url: str
    is_cover: bool

class ListingCreate(BaseModel):
    title: str
    neighborhood: str
    room_type: str
    water: bool
    electricity: bool
    wifi: bool
    price: float
    description: Optional[str] = None
    owner_id: int
    image_urls: Optional[List[str]] = []

class ListingUpdate(BaseModel):
    title: Optional[str] = None
    neighborhood: Optional[str] = None
    room_type: Optional[str] = None
    water: Optional[bool] = None
    electricity: Optional[bool] = None
    wifi: Optional[bool] = None
    price: Optional[float] = None
    description: Optional[str] = None

# --- Helper to serialize listing ---
def serialize_listing(listing):
    images = [{"id": img.id, "image_url": img.image_url, "is_cover": img.is_cover} for img in listing.images]
    cover = next((img["image_url"] for img in images if img["is_cover"]), None)
    if not cover and images:
        cover = images[0]["image_url"]
    return {
        "id": listing.id,
        "title": listing.title,
        "neighborhood": listing.neighborhood,
        "room_type": listing.room_type,
        "water": listing.water,
        "electricity": listing.electricity,
        "wifi": listing.wifi,
        "price": listing.price,
        "description": listing.description,
        "owner_id": listing.owner_id,
        "image_url": cover,
        "images": images
    }

# --- Endpoints ---
@router.post("/")
def create_listing(listing: ListingCreate, db: Session = Depends(get_db)):
    new_listing = Listing(
        title=listing.title,
        neighborhood=listing.neighborhood,
        room_type=listing.room_type,
        water=listing.water,
        electricity=listing.electricity,
        wifi=listing.wifi,
        price=listing.price,
        description=listing.description,
        owner_id=listing.owner_id
    )
    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    # Save images
    for i, url in enumerate(listing.image_urls):
        img = ListingImage(
            listing_id=new_listing.id,
            image_url=url,
            is_cover=(i == 0)
        )
        db.add(img)
    db.commit()

    return {"message": "Listing created successfully", "listing_id": new_listing.id}

@router.get("/")
def get_all_listings(
    neighborhood: Optional[str] = None,
    room_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Listing)
    if neighborhood:
        query = query.filter(Listing.neighborhood == neighborhood)
    if room_type:
        query = query.filter(Listing.room_type == room_type)
    if min_price:
        query = query.filter(Listing.price >= min_price)
    if max_price:
        query = query.filter(Listing.price <= max_price)
    return [serialize_listing(l) for l in query.all()]

@router.get("/{listing_id}")
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return serialize_listing(listing)

@router.put("/{listing_id}")
def update_listing(listing_id: int, listing: ListingUpdate, db: Session = Depends(get_db)):
    db_listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    for key, value in listing.dict(exclude_unset=True).items():
        setattr(db_listing, key, value)
    db.commit()
    db.refresh(db_listing)
    return {"message": "Listing updated successfully"}

@router.delete("/{listing_id}")
def delete_listing(listing_id: int, db: Session = Depends(get_db)):
    db_listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    db.delete(db_listing)
    db.commit()
    return {"message": "Listing deleted successfully"}

@router.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    img = db.query(ListingImage).filter(ListingImage.id == image_id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(img)
    db.commit()
    return {"message": "Image deleted successfully"}