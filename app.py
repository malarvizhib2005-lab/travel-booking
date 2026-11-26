from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Wanderly Travel Booking", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

DESTINATIONS = [
    {
        "id": "santorini",
        "name": "Santorini",
        "country": "Greece",
        "tag": "Aegean escape",
        "description": "Whitewashed villages, volcanic beaches, and the kind of sunset that slows the whole evening down.",
        "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=1200&q=85",
        "rating": 4.9,
        "reviews": 384,
        "days": "5 days",
        "price": 1290,
        "accent": "#ff7c6d",
    },
    {
        "id": "kyoto",
        "name": "Kyoto",
        "country": "Japan",
        "tag": "Quietly iconic",
        "description": "Temple gardens, lantern-lit lanes, and timeless neighborhoods where every turn feels cinematic.",
        "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1200&q=85",
        "rating": 4.8,
        "reviews": 267,
        "days": "7 days",
        "price": 1640,
        "accent": "#efb158",
    },
    {
        "id": "capetown",
        "name": "Cape Town",
        "country": "South Africa",
        "tag": "Wildly beautiful",
        "description": "Table Mountain mornings, ocean road afternoons, and a food scene worth crossing oceans for.",
        "image": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=1200&q=85",
        "rating": 4.9,
        "reviews": 198,
        "days": "6 days",
        "price": 1480,
        "accent": "#6eae8d",
    },
    {
        "id": "amalfi",
        "name": "Amalfi Coast",
        "country": "Italy",
        "tag": "Dolce vita",
        "description": "Cliffside villages, lemon-scented air, and slow lunches overlooking the Tyrrhenian Sea.",
        "image": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=85",
        "rating": 4.7,
        "reviews": 312,
        "days": "5 days",
        "price": 1570,
        "accent": "#79a9c5",
    },
]

HOTELS = {
    "santorini": [
        {"id": "caldera-house", "name": "Caldera House", "type": "Cliffside suite", "rating": 4.9, "price": 248, "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?auto=format&fit=crop&w=900&q=80", "amenities": ["Breakfast", "Infinity pool", "Airport transfer"]},
        {"id": "aether-villas", "name": "Aether Villas", "type": "Private villa", "rating": 4.8, "price": 310, "image": "https://images.unsplash.com/photo-1601918774946-25832a4be0d6?auto=format&fit=crop&w=900&q=80", "amenities": ["Sea view", "Private pool", "Concierge"]},
        {"id": "milos-stay", "name": "Milos Stay", "type": "Design hotel", "rating": 4.7, "price": 185, "image": "https://images.unsplash.com/photo-1540541338287-41700207dee6?auto=format&fit=crop&w=900&q=80", "amenities": ["Breakfast", "Spa", "Beach shuttle"]},
    ],
    "kyoto": [
        {"id": "higashiyama-house", "name": "Higashiyama House", "type": "Machiya retreat", "rating": 4.9, "price": 220, "image": "https://images.unsplash.com/photo-1528360983277-13d401cdc186?auto=format&fit=crop&w=900&q=80", "amenities": ["Tea ceremony", "Garden", "Breakfast"]},
        {"id": "sora-kyoto", "name": "Sora Kyoto", "type": "Boutique hotel", "rating": 4.8, "price": 196, "image": "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?auto=format&fit=crop&w=900&q=80", "amenities": ["Onsen", "Bike hire", "Restaurant"]},
    ],
    "capetown": [
        {"id": "signal-house", "name": "Signal House", "type": "Ocean-view hotel", "rating": 4.8, "price": 174, "image": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99?auto=format&fit=crop&w=900&q=80", "amenities": ["Breakfast", "Rooftop", "Car hire"]},
        {"id": "fynbos-lodge", "name": "Fynbos Lodge", "type": "Nature lodge", "rating": 4.9, "price": 205, "image": "https://images.unsplash.com/photo-1534430480872-3498386e7856?auto=format&fit=crop&w=900&q=80", "amenities": ["Hiking access", "Fireplace", "Spa"]},
    ],
    "amalfi": [
        {"id": "casa-luce", "name": "Casa Luce", "type": "Lemon grove hotel", "rating": 4.8, "price": 265, "image": "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=900&q=80", "amenities": ["Sea terrace", "Breakfast", "Boat trips"]},
        {"id": "palazzo-mare", "name": "Palazzo Mare", "type": "Historic palazzo", "rating": 4.7, "price": 298, "image": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=900&q=80", "amenities": ["Pool", "Valet parking", "Restaurant"]},
    ],
}

PACKAGES = {
    destination["id"]: [
        {"id": f'{destination["id"]}-slow-explorer', "name": "The Slow Explorer", "duration": destination["days"], "price": destination["price"], "summary": "The considered way to see it: signature sights, neighborhood secrets, and room to wander.", "includes": ["Handpicked hotel", "Daily breakfast", "Local host", "Airport transfers", "Flexible cancellation"]},
        {"id": f'{destination["id"]}-full-colour', "name": "Full Colour Weekend", "duration": "4 days", "price": destination["price"] - 220, "summary": "A bright, compact escape for curious travelers who want the highlights with a local rhythm.", "includes": ["Boutique hotel", "3 guided experiences", "City pass", "Welcome dinner", "24/7 support"]},
    ] for destination in DESTINATIONS
}

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "customer"

class BookingRequest(BaseModel):
    destination_id: str
    package_id: str
    hotel_id: str
    guest_name: str
    email: EmailStr
    check_in: str
    guests: int = 2

@app.get("/")
async def home() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")

@app.get("/destinations")
async def destinations_page() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "destinations.html")

@app.get("/packages")
async def packages_page() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "packages.html")

@app.get("/hotels")
async def hotels_page() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "hotels.html")

@app.get("/payment")
async def payment_page() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "payment.html")

@app.get("/contact")
async def contact_page() -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "contact.html")

@app.get("/api/destinations")
async def destinations() -> list[dict[str, Any]]:
    return DESTINATIONS

@app.get("/api/destinations/{destination_id}")
async def destination(destination_id: str) -> dict[str, Any]:
    destination = next((item for item in DESTINATIONS if item["id"] == destination_id), None)
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {**destination, "hotels": HOTELS.get(destination_id, []), "packages": PACKAGES.get(destination_id, [])}

@app.post("/api/contact")
async def contact(payload: ContactRequest) -> dict[str, str]:
    return {"message": f"Thanks {payload.name}, your note is with our travel desk."}

@app.post("/api/login")
async def login(payload: LoginRequest) -> dict[str, str]:
    return {"message": f"Welcome back. Signed in as {payload.role}.", "role": payload.role, "email": str(payload.email)}

@app.post("/api/bookings")
async def create_booking(payload: BookingRequest) -> dict[str, Any]:
    destination = next((item for item in DESTINATIONS if item["id"] == payload.destination_id), None)
    package = next((item for item in PACKAGES.get(payload.destination_id, []) if item["id"] == payload.package_id), None)
    hotel = next((item for item in HOTELS.get(payload.destination_id, []) if item["id"] == payload.hotel_id), None)
    if not destination or not package or not hotel:
        raise HTTPException(status_code=400, detail="Please choose a valid destination, package, and hotel.")
    reference = f"WND-{datetime.now().strftime('%y%m%d%H%M')}"
    return {"reference": reference, "total": package["price"] + hotel["price"], "destination": destination["name"], "message": "Your booking request is ready for payment."}

@app.get("/{path:path}")
async def spa_fallback(path: str) -> FileResponse:
    return FileResponse(BASE_DIR / "templates" / "index.html")
