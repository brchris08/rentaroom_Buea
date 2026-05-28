from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.routers import auth, listings, predict
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
import shutil, uuid, os

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