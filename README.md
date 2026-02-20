# 🍎 Shelf.io | Community Resource Logistics Engine

Shelf.io is a production-ready, secure inventory management system designed to optimize community food pantry operations. It facilitates a data-driven bridge between donors and volunteers, utilizing real-time auditing and role-based access control (RBAC) to minimize resource waste and maximize community impact.

---

## 🚀 Advanced Features

- **Role-Based Access Control (RBAC):** Cryptographically secure permission tiers for 'Donors' and 'Volunteers'.
- **Live Activity Auditing:** A comprehensive transaction log tracking every stock adjustment, addition, and deletion for accountability.
- **Urgent Needs Heuristics:** Dynamic UI alerts that highlight low-stock items (Qty < 5) to prioritize donor contributions.
- **Secure Authentication:** Password security powered by the **Scrypt** key derivation function.
- **Responsive Architecture:** A "Mobile-First" interface engineered with Tailwind CSS for high-velocity on-site pantry management.

## 🛠️ Tech Stack & Engineering Standards

- **Backend:** Python 3.x / Flask
- **Database:** SQLAlchemy ORM (Relational SQLite/PostgreSQL)
- **Security:** - `python-dotenv` for Environment Variable isolation.
  - `Werkzeug` security for advanced password hashing.
  - Cross-Site Request Forgery (CSRF) protection via Flask-Login session management.
- **Frontend:** HTML5, Tailwind CSS, Lucide Icons, Asynchronous JavaScript (Fetch API).



## 🔐 System Permissions & Security Matrix

| Action                 | Donor (Guest) | Volunteer (Admin) | Requirement          |
|------------------------|:-------------:|:-----------------:|----------------------|
| Register New Account   |      ✅       |      ✅           | Volunteer Code Valid |
| Add New Inventory      |      ✅       |      ✅           | Authenticated        |
| Increase Stock (+)     |      ✅       |      ✅           | Authenticated        |
| Edit Item Details      |      ❌       |      ✅           | Volunteer Role       |
| Decrease Stock (Take)  |      ❌       |      ✅           | Volunteer Role       |
| Delete Record          |      ❌       |      ✅           | Volunteer Role       |
| Access Activity Logs   |      ❌       |      ✅           | Volunteer Role       |

## 🏁 Installation & Deployment

### 1. Initialize Environment
Clone the repository and set up your virtual environment:
```bash
git clone [https://github.com/yourusername/shelf-io.git](https://github.com/yourusername/shelf-io.git)
cd shelf-io
pip install -r requirements.txt
