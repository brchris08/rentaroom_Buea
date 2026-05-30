# RentARoom Buea 🏠

A smart room listing and rent price estimation web application for students in Buea, Cameroon.

> Built as a Software Construction project demonstrating all five SWEBOK Knowledge Areas — from modular architecture and CI/CD pipelines to machine learning integration and cloud deployment.

---

## 🌐 Live Demo

**[https://rentaroom-buea.onrender.com](https://rentaroom-buea.onrender.com)**

---

## 📌 What It Does

- 🏘️ Landlords post room listings with photos, location, price, and amenities
- 🔍 Students browse and filter listings by neighbourhood, room type, and price
- 🤖 A machine learning model flags every listing as **Fair**, **Good Deal**, or **Overpriced**
- 💬 Students contact landlords directly via WhatsApp — no agency fees
- 🔐 Separate accounts for Students and Landlords
- 🛡️ Super admin dashboard to manage all users and listings

---

## 🗂️ Project Structure

```
rentaroom-buea/
│
├── backend/                        # FastAPI backend
│   ├── main.py                     # App entry point, all routes
│   ├── database.py                 # SQLAlchemy engine & session
│   ├── models/
│   │   └── schemas.py              # User, Listing, ListingImage models
│   └── routers/
│       ├── auth.py                 # POST /auth/register, /auth/login
│       ├── listings.py             # CRUD /listings/
│       └── predict.py              # POST /predict/ — ML price prediction
│
├── frontend/
│   ├── templates/
│   │   ├── welcome.html            # Landing page (/)
│   │   ├── index.html              # Browse listings (/home)
│   │   ├── login.html              # Login & Register (/login)
│   │   ├── post-listing.html       # Post a room (/post-listing)
│   │   ├── listing-detail.html     # Single listing (/listing-detail)
│   │   └── admin.html              # Admin dashboard (/admin) — local only
│   └── static/
│       ├── css/                    # Stylesheets
│       ├── js/                     # Scripts
│       ├── uploads/                # Uploaded room photos
│       └── Slides/                 # Hero slideshow images
│
├── ml/                             # Machine learning
│   ├── rent_model.pkl              # Trained Random Forest model
│   ├── encoder.pkl                 # OneHotEncoder for neighbourhoods
│   └── dataset.csv                 # Manually collected Buea housing data
│
├── tests/
│   └── test_main.py                # pytest test suite (5 tests)
│
├── .circleci/
│   └── config.yml                  # CircleCI CI/CD pipeline
│
├── Dockerfile                      # Docker container configuration
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in repo)
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register a new user |
| `POST` | `/auth/login` | Login and get user info |
| `GET` | `/listings/` | Get all listings (with filters) |
| `GET` | `/listings/{id}` | Get a single listing |
| `POST` | `/listings/` | Create a new listing |
| `PUT` | `/listings/{id}` | Update a listing |
| `DELETE` | `/listings/{id}` | Delete a listing |
| `POST` | `/predict/` | Predict rent price + fairness label |
| `POST` | `/upload-image` | Upload a room/hostel photo |
| `POST` | `/admin/login` | Admin authentication |
| `GET` | `/admin/data` | Get all users and listings (admin only) |
| `DELETE` | `/admin/remove-user/{id}` | Delete a user (admin only) |
| `DELETE` | `/admin/remove-listing/{id}` | Delete a listing (admin only) |

---

## 🧠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| ML Model | scikit-learn — Random Forest Regression |
| Frontend | HTML, CSS, JavaScript, Bootstrap 5 |
| Auth | passlib + bcrypt password hashing |
| Containerization | Docker |
| CI/CD | CircleCI — runs pytest on every push |
| Deployment | Render.com |
| Cloud DB | Supabase (PostgreSQL) |

---

## 🤖 Machine Learning

The ML model predicts fair rental prices for rooms in Buea based on:

| Feature | Type |
|---------|------|
| Neighbourhood | Categorical (One-Hot Encoded) |
| Room Type | Categorical (Single / Room & Toilet / Self Contain) |
| Water Supply | Binary (0 or 1) |
| Stable Electricity | Binary (0 or 1) |
| WiFi | Binary (0 or 1) |

**Model:** Random Forest Regression  
**Training data:** 500+ data points collected from field surveys, Facebook groups, WhatsApp broadcasts, and a Google Form peer survey  
**Output:** Predicted price in FCFA/year + fairness label (`Fair` / `Good Deal` / `Overpriced`)

---

## ⚙️ Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/brchris08/rentaroom_Buea.git
cd rentaroom_Buea
```

**2. Create and activate virtual environment**
```bash
python -m venv room_env
room_env\Scripts\activate        # Windows
source room_env/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file**
```
ADMIN_EMAIL=your_admin_email@gmail.com
ADMIN_PASSWORD=your_admin_password
ADMIN_SECRET=your_secret_token
```

**5. Run the app**
```bash
uvicorn backend.main:app --reload
```

**6. Open in browser**
```
http://127.0.0.1:8000
```

---

## ✅ Running Tests

```bash
pytest tests/test_main.py -v
```

Expected output:
```
tests/test_main.py::test_register          PASSED
tests/test_main.py::test_login             PASSED
tests/test_main.py::test_create_listing    PASSED
tests/test_main.py::test_get_listings      PASSED
tests/test_main.py::test_predict_price     PASSED

5 passed
```

---

## 🚀 DevOps Pipeline

```
Push to GitHub
      │
      ▼
CircleCI — runs pytest automatically
      │
      ▼
Docker — app containerized via Dockerfile
      │
      ▼
Render.com — deploys live to production
      │
      ▼
Supabase PostgreSQL — persistent cloud database
```

---

## 📊 System Architecture

![RentARoom Buea Architecture](rentaroom_buea_architecture.svg)

---

## 🛡️ Admin Dashboard

The admin dashboard is only accessible from `localhost` — it is completely hidden from the public internet. It allows the creator to:

- View all registered users and listings
- Delete users and listings
- Monitor platform growth in real time

---

## 📁 Dataset

The ML training dataset (`ml/dataset.csv`) was manually constructed using:

- **Field surveys** in Molyko, Bonduma, Great Soppo, Clerks Quarter, and Mile 16
- **Facebook groups** and WhatsApp student housing broadcasts  
- **Google Form peer survey** distributed to University of Buea students

**Total rows:** 500+ (after data augmentation from 42 real collected points)

---

## 👨‍💻 Author

**Bake Brian-Chris Nkongho**  
Department of Computer Engineering  
University of Buea  
Matricule: CT25A429

---

## 📄 License

This project was built for academic purposes as part of a Software Construction course at the University of Buea.