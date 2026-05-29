from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

# User table
class User(Base):
    __tablename__ = "users"

    is_admin = Column(Boolean, default=False)
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    listings = relationship("Listing", back_populates="owner")


# Listing table
class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    room_type = Column(String, nullable=False)
    water = Column(Boolean, nullable=False)
    electricity = Column(Boolean, nullable=False)
    wifi = Column(Boolean, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")


# Listing images table
class ListingImage(Base):
    __tablename__ = "listing_images"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    image_url = Column(String, nullable=False)
    whatsapp_number = Column(String, nullable=True)
    is_cover = Column(Boolean, default=False)

    listing = relationship("Listing", back_populates="images")