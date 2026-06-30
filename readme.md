# Flask + PostgreSQL + Redis — Order Management API 🛒

A multi-container backend system simulating a simple e-commerce order flow — built with Flask, PostgreSQL, and Redis, orchestrated using Docker Compose.

---

## 📌 What It Does

A REST API to:
- Add and list products
- Place and list orders
- Backed by a real relational database (PostgreSQL) with foreign key relationships

---

## 🏗️ Architecture

```
Client (curl/Postman)
        │
        ▼
   Flask API (port 5000)
        │
   ┌────┴─────┐
   ▼          ▼
PostgreSQL   Redis
(data store) (cache layer)
```

| Service | Image | Role |
|--------|-------|------|
| `flask` | Built from Dockerfile | REST API — handles requests |
| `postgres` | `postgres:latest` | Stores products & orders (relational data) |
| `redis` | `redis:latest` | Reserved for caching/session use |

---

## 🗃️ Database Schema

**products**
| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| name | TEXT |
| price | DECIMAL |

**orders**
| Column | Type |
|--------|------|
| id | SERIAL PRIMARY KEY |
| product_id | INTEGER → references products(id) |
| customer_name | TEXT |
| status | TEXT (default: pending) |

`orders.product_id` is a foreign key — links each order to a real product, avoiding duplicate data.

---

## 🚀 How to Run

```bash
git clone https://github.com/Siddhesh-07/flask-postgres-redis-orders.git
cd flask-postgres-redis-orders
docker compose up -d --build
```

Use curl/Postman to interact


## 📡 API Endpoints

**Add a product**
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 50000}'
```

**List all products**
```bash
curl http://localhost:5000/products
```

**Place an order**
```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "customer_name": "Test User"}'
```

**List all orders**
```bash
curl http://localhost:5000/orders
```

---

## 🛠️ Useful Commands

```bash
docker compose ps          # check running containers
docker compose logs flask  # view flask logs
docker compose down        # stop and remove containers
```

---

## 💡 What I Learned

- Designing a relational schema with a foreign key relationship
- Connecting Flask to PostgreSQL using `psycopg2`
- Running a 3-container stack with Docker Compose
- **Real production issue hit:** `depends_on` only waits for a container to *start*, not for the service inside to be *ready*. PostgreSQL took a few seconds to accept connections after starting, causing Flask to fail on first boot with a connection refused error. Fixed by restarting the Flask container — in production this would be solved properly using Compose healthchecks.
- Why caching (Redis) and persistent storage (PostgreSQL) serve different purposes in a real system

---

## 🗂️ Project Structure

```
flask-postgres-redis-orders/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

> **Tech Stack:** Python · Flask · PostgreSQL · Redis · Docker · Docker Compose · AWS EC2
