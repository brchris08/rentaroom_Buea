# RentARoom Buea 🏠

A smart room listing and rent price estimation web application for students in Buea, Cameroon.

## What It Does
- Landlords can post room listings with photos, location, price, and amenities
- Students can browse and filter listings by neighbourhood and price range
- A machine learning model predicts a fair rental price and flags listings as **Fair**, **Good Deal**, or **Overpriced**

## System Architecture
![RentARoom Buea Architecture](rentaroom_buea_architecture.svg)

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python + FastAPI |
| Database | SQLite |
| ML Model | scikit-learn (Random Forest Regression) |
| Frontend | HTML, CSS, JavaScript, Bootstrap 5 |
| Containerization | Docker |
| CI/CD | CircleCI |
| Deployment | Render.com |

## Features
- 🔐 User registration and login (Student and Landlord roles)
- 🏘️ Room listings with hostel and room interior photo upload
- 🔍 Browse and filter by neighbourhood, room type, and max price
- 🤖 AI-powered `/predict` endpoint for rent price estimation
- 🏷️ Price fairness label shown on every listing (Fair / Good Deal / Overpriced)
- ✅ Automated pytest test suite with 5 tests covering all core endpoints

## Project Structure
rentaroom-buea/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLite database setup
│   ├── models/              # Database models
│   ├── routers/
│   │   ├── auth.py          # Register & login endpoints
│   │   ├── listings.py      # Listings CRUD endpoints
│   │   └── predict.py       # ML price prediction endpoint
│   └── ml/                  # Trained model (.pkl files)
├── frontend/
│   ├── templates/
│   │   ├── index.html       # Browse listings page
│   │   ├── post-listing.html # Post a room page
│   │   ├── listing-detail.html # Single listing page
│   │   └── login.html       # Login / Register page
│   └── static/
│       ├── css/
│       ├── js/
│       └── uploads/         # Uploaded room photos
├── tests/
│   └── test_main.py         # pytest test suite
├── Dockerfile
├── .circleci/config.yml
└── requirements.txt

## Getting Started (Local Setup)

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/rentaroom-buea.git
cd rentaroom-buea
```

**2. Create and activate virtual environment**
```bash
python -m venv room_env
room_env\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
uvicorn backend.main:app --reload
```

**5. Open in browser**
http://127.0.0.1:8000

## Running Tests
```bash
pytest tests/test_main.py -v
```

## Dataset
The ML model was trained on a manually constructed dataset of 100–150+ rows collected via:
- Direct field surveys in Molyko, Bonduma, Great Soppo, Clerks Quarter, and Mile 16
- Facebook groups and WhatsApp student housing broadcasts
- Google Form peer survey distributed to UB students

## Status
🚧 Week 5 in progress — DevOps (Docker, CircleCI, Render.com)

## Author
**Bake Brian-Chris Nkongho** — Computer Engineering, University of Buea  
Matricule: CT25A429
