# Wanderly Travel Booking

A FastAPI travel booking experience with destination discovery, packages, hotels, contact form, and customer/admin login modal.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`.

## Pages

- `/` home
- `/destinations` destination catalog
- `/packages?destination=santorini` package selection
- `/hotels?destination=santorini&package=santorini-slow-explorer` related hotel selection
- `/payment` payment confirmation page
- `/contact` contact form and studio details

The API currently uses seeded in-memory data so the interface works immediately. `pymysql` is included for the next persistence step; connect the booking, contact, and auth handlers to your MySQL schema when credentials are available.
