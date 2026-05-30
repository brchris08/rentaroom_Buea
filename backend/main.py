from dotenv import load_dotenv
load_dotenv()
import secrets
from fastapi import FastAPI,UploadFile, File, Depends, HTTPException, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base, get_db
from backend.routers import auth, listings, predict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil, uuid, os
from sqlalchemy.orm import Session
from backend.models.schemas import User, Listing

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="RentARoom Buea API",
    description="A smart room listing and rent price estimation API for students in Buea",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = os.getenv("ADMIN_SECRET")
    if credentials.credentials != token:
        raise HTTPException(status_code=403, detail="Forbidden")
    
@app.post("/admin/login")
def admin_login(credentials: dict, db: Session = Depends(get_db)):
    email = credentials.get("email")
    password = credentials.get("password")
    if (email == os.getenv("ADMIN_EMAIL") and
        password == os.getenv("ADMIN_PASSWORD")):
        token = os.getenv("ADMIN_SECRET")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/admin/data")
def get_admin_data(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_admin(credentials)
    users = db.query(User).all()
    listings = db.query(Listing).all()
    return {
        "users": [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role} for u in users],
        "listings": [{"id": l.id, "title": l.title, "neighborhood": l.neighborhood, "price": l.price, "owner_id": l.owner_id} for l in listings]
    }

@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_admin(credentials)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@app.delete("/admin/listings/{listing_id}")
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_admin(credentials)
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted"}
@app.get("/admin")
def serve_admin(request: Request):
    client_host = request.client.host
    allowed = ["127.0.0.1", "::1", "localhost"]
    if client_host not in allowed:
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse("frontend/templates/admin.html")

@app.get("/admin/data")
def get_admin_data(
    authorization: str = None,
    db: Session = Depends(get_db)
):
    verify_admin(authorization)
    users = db.query(User).all()
    listings = db.query(Listing).all()
    return {
        "users": [{"id": u.id, "full_name": u.full_name, "email": u.email, "role": u.role} for u in users],
        "listings": [{"id": l.id, "title": l.title, "neighborhood": l.neighborhood, "price": l.price, "owner_id": l.owner_id} for l in listings]
    }

@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    verify_admin(authorization)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}

@app.delete("/admin/listings/{listing_id}")
def delete_listing(
    listing_id: int,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    verify_admin(authorization)
    listing = db.query(Listing).filter(Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted"}
@app.get("/")
def serve_welcome():
    return FileResponse("frontend/templates/welcome.html")
@app.get("/home")
def serve_home():
    return FileResponse("frontend/templates/index.html")
@app.get("/login")
def serve_login():
    return FileResponse("frontend/templates/login.html")
@app.get("/post-listing")
def serve_post_listing():
    return FileResponse("frontend/templates/post-listing.html")
@app.get("/listing-detail")
def serve_listing_detail():
    return FileResponse("frontend/templates/listing-detail.html")

# Upload image
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs("frontend/static/uploads", exist_ok=True)
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = f"frontend/static/uploads/{filename}"
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"image_url": f"/static/uploads/{filename}"}

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(listings.router, prefix="/listings", tags=["Listings"])
app.include_router(predict.router, prefix="/predict", tags=["Prediction"])

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to RentARoom Buea API"}