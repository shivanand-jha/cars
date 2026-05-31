#!/usr/bin/env python3
import json
import os
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
DB_PATH = os.path.join(BASE_DIR, "shortlists.db")
HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "8000"))


CARS = [
    {
        "id": "baleno-zeta",
        "make": "Maruti Suzuki",
        "model": "Baleno",
        "variant": "Zeta Petrol",
        "price_lakh": 8.4,
        "mileage_kmpl": 22.3,
        "safety_rating": 3,
        "body_type": "Hatchback",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 9,
        "highway_score": 6,
        "features_score": 7,
        "comfort_score": 6,
        "reliability_score": 9,
        "pros": ["Excellent mileage", "Easy city driving", "Large service network"],
        "cons": ["Average crash-test rating", "Light highway feel"],
        "review": "Owners like the smooth engine, low running costs, and hassle-free ownership.",
    },
    {
        "id": "fronx-delta-plus",
        "make": "Maruti Suzuki",
        "model": "Fronx",
        "variant": "Delta+ Turbo",
        "price_lakh": 9.7,
        "mileage_kmpl": 20.0,
        "safety_rating": 4,
        "body_type": "Compact SUV",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 8,
        "highway_score": 7,
        "features_score": 7,
        "comfort_score": 7,
        "reliability_score": 8,
        "pros": ["Punchy turbo engine", "SUV stance", "Efficient for daily use"],
        "cons": ["Rear seat is not the widest", "Some premium features reserved for top trims"],
        "review": "A good middle path for buyers wanting hatchback ease with crossover presence.",
    },
    {
        "id": "nexon-creative",
        "make": "Tata",
        "model": "Nexon",
        "variant": "Creative Petrol",
        "price_lakh": 12.2,
        "mileage_kmpl": 17.4,
        "safety_rating": 5,
        "body_type": "Compact SUV",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 7,
        "highway_score": 8,
        "features_score": 8,
        "comfort_score": 8,
        "reliability_score": 7,
        "pros": ["Strong safety package", "Feature-rich cabin", "Confident highway manners"],
        "cons": ["Mileage trails lighter cars", "After-sales experience can vary by city"],
        "review": "Frequently shortlisted by families that put crash safety and road presence first.",
    },
    {
        "id": "punch-accomplished",
        "make": "Tata",
        "model": "Punch",
        "variant": "Accomplished Petrol",
        "price_lakh": 8.9,
        "mileage_kmpl": 20.1,
        "safety_rating": 5,
        "body_type": "Micro SUV",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 8,
        "highway_score": 6,
        "features_score": 6,
        "comfort_score": 6,
        "reliability_score": 7,
        "pros": ["Five-star safety", "Compact footprint", "High seating position"],
        "cons": ["Engine feels relaxed rather than quick", "Rear width is best for two adults"],
        "review": "Buyers praise the confidence it gives first-time owners in crowded cities.",
    },
    {
        "id": "venue-sx",
        "make": "Hyundai",
        "model": "Venue",
        "variant": "SX Turbo",
        "price_lakh": 12.6,
        "mileage_kmpl": 18.1,
        "safety_rating": 4,
        "body_type": "Compact SUV",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 8,
        "highway_score": 7,
        "features_score": 9,
        "comfort_score": 8,
        "reliability_score": 8,
        "pros": ["Polished interior", "Loaded feature list", "Easy automatic option"],
        "cons": ["Rear seat space is average", "Higher trims get expensive"],
        "review": "A polished choice for city buyers who value features and cabin quality.",
    },
    {
        "id": "city-vx",
        "make": "Honda",
        "model": "City",
        "variant": "VX Petrol",
        "price_lakh": 14.1,
        "mileage_kmpl": 17.8,
        "safety_rating": 5,
        "body_type": "Sedan",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 7,
        "highway_score": 9,
        "features_score": 8,
        "comfort_score": 9,
        "reliability_score": 9,
        "pros": ["Excellent rear-seat comfort", "Refined engine", "Strong reliability reputation"],
        "cons": ["Low stance is not for rough roads", "Price overlaps compact SUVs"],
        "review": "Still a benchmark for families who travel often and prefer sedan comfort.",
    },
    {
        "id": "seltos-htk-plus",
        "make": "Kia",
        "model": "Seltos",
        "variant": "HTK+ Petrol",
        "price_lakh": 15.3,
        "mileage_kmpl": 17.0,
        "safety_rating": 4,
        "body_type": "SUV",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 7,
        "highway_score": 8,
        "features_score": 9,
        "comfort_score": 8,
        "reliability_score": 8,
        "pros": ["Premium cabin feel", "Strong feature package", "Good road presence"],
        "cons": ["Not the cheapest to buy", "Ride can feel firm on broken roads"],
        "review": "Often chosen by buyers who want a premium-feeling SUV without going too large.",
    },
    {
        "id": "ertiga-zxi",
        "make": "Maruti Suzuki",
        "model": "Ertiga",
        "variant": "ZXI Petrol",
        "price_lakh": 11.2,
        "mileage_kmpl": 20.5,
        "safety_rating": 3,
        "body_type": "MPV",
        "fuel_type": "Petrol",
        "seats": 7,
        "city_score": 7,
        "highway_score": 7,
        "features_score": 6,
        "comfort_score": 8,
        "reliability_score": 9,
        "pros": ["Practical seven-seat layout", "Efficient for its size", "Low ownership cost"],
        "cons": ["Safety rating is modest", "Third row is best for short trips"],
        "review": "A sensible family mover where space and running cost matter more than flash.",
    },
    {
        "id": "carens-prestige",
        "make": "Kia",
        "model": "Carens",
        "variant": "Prestige Petrol",
        "price_lakh": 13.4,
        "mileage_kmpl": 16.8,
        "safety_rating": 3,
        "body_type": "MPV",
        "fuel_type": "Petrol",
        "seats": 7,
        "city_score": 6,
        "highway_score": 8,
        "features_score": 8,
        "comfort_score": 9,
        "reliability_score": 8,
        "pros": ["Comfortable three-row cabin", "Premium dashboard", "Good highway cruiser"],
        "cons": ["Mileage is not a strength", "Large footprint in tight parking"],
        "review": "A nicer-feeling alternative to basic MPVs for larger families.",
    },
    {
        "id": "i20-asta",
        "make": "Hyundai",
        "model": "i20",
        "variant": "Asta Petrol",
        "price_lakh": 9.3,
        "mileage_kmpl": 20.3,
        "safety_rating": 3,
        "body_type": "Hatchback",
        "fuel_type": "Petrol",
        "seats": 5,
        "city_score": 9,
        "highway_score": 6,
        "features_score": 8,
        "comfort_score": 7,
        "reliability_score": 8,
        "pros": ["Premium hatchback cabin", "Feature-rich", "Easy to drive daily"],
        "cons": ["Rear seat is adequate, not huge", "Safety score trails newer Tata options"],
        "review": "A city-friendly premium hatchback for buyers who enjoy features and refinement.",
    },
]


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shortlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at INTEGER NOT NULL,
                buyer_name TEXT NOT NULL,
                preferences TEXT NOT NULL,
                car_ids TEXT NOT NULL,
                notes TEXT NOT NULL
            )
            """
        )


def parse_json(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length == 0:
        return {}
    try:
        return json.loads(handler.rfile.read(length).decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON body")


def score_car(car, prefs):
    budget = float(prefs.get("budget_lakh") or 12)
    family_size = int(prefs.get("family_size") or 4)
    usage = prefs.get("usage") or "mixed"
    mileage_priority = int(prefs.get("mileage_priority") or 3)
    safety_priority = int(prefs.get("safety_priority") or 4)
    feature_priority = int(prefs.get("feature_priority") or 3)
    body_preference = prefs.get("body_preference") or "any"

    score = 28
    reasons = []
    cautions = []

    if car["price_lakh"] <= budget:
        headroom = budget - car["price_lakh"]
        score += min(16, 7 + headroom * 1.3)
        reasons.append("fits your budget with room for insurance and accessories")
    else:
        over = car["price_lakh"] - budget
        score -= min(30, 8 + over * 7)
        cautions.append("is above your stated budget")

    if family_size >= 6:
        if car["seats"] >= 7:
            score += 16
            reasons.append("has the seating flexibility your family size needs")
        else:
            score -= 24
            cautions.append("may feel cramped for six or more people")
    elif family_size == 5 and car["comfort_score"] >= 8:
        score += 5
        reasons.append("has stronger comfort for a full five-person family")

    score += (car["mileage_kmpl"] - 15) * mileage_priority * 0.55
    if mileage_priority >= 4 and car["mileage_kmpl"] >= 20:
        reasons.append("keeps running costs low with strong mileage")

    score += (car["safety_rating"] - 3) * safety_priority * 2.6
    if safety_priority >= 4 and car["safety_rating"] >= 5:
        reasons.append("matches your safety-first priority")
    if safety_priority >= 4 and car["safety_rating"] <= 3:
        cautions.append("has a modest safety rating for your safety priority")

    score += car["features_score"] * feature_priority * 0.72
    if feature_priority >= 4 and car["features_score"] >= 8:
        reasons.append("has the feature depth you asked for")

    if usage == "city":
        score += car["city_score"] * 1.45
        if car["city_score"] >= 8:
            reasons.append("is easy to live with in city traffic")
    elif usage == "highway":
        score += car["highway_score"] * 1.45
        if car["highway_score"] >= 8:
            reasons.append("is better suited to highway trips")
    else:
        score += (car["city_score"] + car["highway_score"]) * 0.72
        reasons.append("balances city use and weekend highway drives")

    if body_preference != "any":
        if car["body_type"].lower() == body_preference.lower():
            score += 8
            reasons.append("matches your preferred body style")
        else:
            score -= 6

    score += car["reliability_score"] * 1.0

    if not reasons:
        reasons.append("is a reasonable all-rounder for the preferences entered")

    return {
        **car,
        "match_score": max(0, min(100, round(score))),
        "reasons": reasons[:4],
        "cautions": cautions[:3],
    }


def recommend(prefs):
    ranked = [score_car(car, prefs) for car in CARS]
    ranked.sort(key=lambda car: car["match_score"], reverse=True)
    return ranked


def save_shortlist(payload):
    buyer_name = (payload.get("buyer_name") or "Anonymous buyer").strip()[:80]
    preferences = payload.get("preferences") or {}
    car_ids = payload.get("car_ids") or []
    notes = (payload.get("notes") or "").strip()[:1200]

    valid_ids = {car["id"] for car in CARS}
    car_ids = [car_id for car_id in car_ids if car_id in valid_ids]
    if not car_ids:
        raise ValueError("Select at least one car to save")

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            INSERT INTO shortlists (created_at, buyer_name, preferences, car_ids, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                int(time.time()),
                buyer_name,
                json.dumps(preferences),
                json.dumps(car_ids),
                notes,
            ),
        )
        shortlist_id = cursor.lastrowid
    return {"id": shortlist_id, "buyer_name": buyer_name, "car_ids": car_ids, "notes": notes}


def list_shortlists():
    cars_by_id = {car["id"]: car for car in CARS}
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM shortlists ORDER BY created_at DESC LIMIT 20"
        ).fetchall()
    results = []
    for row in rows:
        car_ids = json.loads(row["car_ids"])
        results.append(
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "buyer_name": row["buyer_name"],
                "preferences": json.loads(row["preferences"]),
                "cars": [cars_by_id[car_id] for car_id in car_ids if car_id in cars_by_id],
                "notes": row["notes"],
            }
        )
    return results


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, path):
        if path == "/":
            file_path = os.path.join(STATIC_DIR, "index.html")
        else:
            requested = os.path.normpath(path.lstrip("/"))
            file_path = os.path.join(STATIC_DIR, requested)
            if not file_path.startswith(STATIC_DIR):
                self.send_error(403)
                return

        if not os.path.exists(file_path):
            self.send_error(404)
            return

        ext = os.path.splitext(file_path)[1]
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }.get(ext, "application/octet-stream")
        with open(file_path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/cars":
            self.send_json({"cars": CARS})
        elif path == "/api/shortlists":
            self.send_json({"shortlists": list_shortlists()})
        else:
            self.send_static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = parse_json(self)
            if path == "/api/recommend":
                self.send_json({"recommendations": recommend(payload)})
            elif path == "/api/shortlist":
                saved = save_shortlist(payload)
                self.send_json({"shortlist": saved}, status=201)
            else:
                self.send_error(404)
        except ValueError as exc:
            self.send_json({"error": str(exc)}, status=400)
        except Exception as exc:
            self.send_json({"error": "Unexpected server error", "detail": str(exc)}, status=500)


def main():
    init_db()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print("CarDekho Shortlist Coach running at http://%s:%s" % (HOST, PORT))
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
