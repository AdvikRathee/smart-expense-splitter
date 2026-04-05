# 💸 Smart Expense Splitter API

A **Splitwise-like REST API** built with FastAPI that helps groups split expenses and calculates the **minimum number of transactions** to settle all debts.

---

## 🚀 Features

- ✅ Create groups and add members
- ✅ Add expenses — specify who paid and split among whom
- ✅ **Debt minimization algorithm** — get the least number of transactions to settle up
- ✅ Auto-generated interactive API docs at `/docs`
- ✅ SQLite database — zero setup required

---

## 🛠️ Tech Stack

- **Python** + **FastAPI**
- **SQLAlchemy** ORM
- **SQLite** (no DB setup needed)
- **Pydantic** for data validation

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/your-username/expense-splitter.git
cd expense-splitter
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the server
```bash
uvicorn app.main:app --reload
```

### 4. Open API docs
```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/groups/` | Create a new group |
| GET | `/groups/` | List all groups |
| POST | `/groups/{id}/members` | Add member to group |
| GET | `/groups/{id}/members` | List group members |
| POST | `/expenses/` | Add an expense |
| GET | `/expenses/group/{id}` | List group expenses |
| GET | `/settle/{group_id}` | Get minimum transactions to settle |

---

## 🧪 Example Flow

**1. Create a group**
```json
POST /groups/
{ "name": "Goa Trip", "description": "March 2025" }
```

**2. Add members**
```json
POST /groups/1/members
{ "name": "Advik", "group_id": 1 }
{ "name": "Rahul", "group_id": 1 }
{ "name": "Priya", "group_id": 1 }
```

**3. Add expense**
```json
POST /expenses/
{
  "description": "Hotel",
  "amount": 3000,
  "paid_by": 1,
  "group_id": 1,
  "split_among": [1, 2, 3]
}
```

**4. Settle up**
```json
GET /settle/1

Response:
{
  "group": "Goa Trip",
  "total_expenses": 3000,
  "transactions": [
    { "from_member": "Rahul", "to_member": "Advik", "amount": 1000.0 },
    { "from_member": "Priya", "to_member": "Advik", "amount": 1000.0 }
  ]
}
```

---

## 👨‍💻 Author

**Advik Rathee**  
[GitHub](https://github.com/AdvikRathee) | [LinkedIn](https://linkedin.com/in/advik-rathee)
