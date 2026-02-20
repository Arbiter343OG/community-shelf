# 🍎 Shelf.io | Multi-Tenant Community Logistics Platform

Shelf.io is a scalable, secure, and production-ready inventory management engine designed for decentralized community support. Unlike single-instance trackers, Shelf.io utilizes a **Multi-Tenant Architecture**, allowing multiple independent organizations to manage their own private resource silos within a unified infrastructure.

---

## 🏗️ Architectural Evolution
The project has evolved from a simple inventory tool into a **SaaS-ready logistics platform**. By implementing foreign-key isolation, we ensure that data from one community center is cryptographically and logically separated from others.



## 🚀 Key Platform Features

- **Multi-Tenant Isolation:** Dynamic organization registration creates private data environments for each community center.
- **Role-Based Access Control (RBAC):** Tiered permissions for 'Donors' and 'Volunteers' within specific organizational boundaries.
- **Dynamic Logistics Dashboard:** Real-time inventory heuristics including total impact tracking and automated "Low Stock" alerts.
- **Cryptographic Security:** User authentication powered by the **Scrypt** key derivation function for industry-standard password hashing.
- **Audit Provenance:** A robust `ActivityLog` system that records every transaction, providing a transparent audit trail for resource movement.

## 🛠️ Engineering Stack

- **Backend:** Python 3.x / Flask
- **ORM:** SQLAlchemy (Relational mapping with foreign-key constraints)
- **Security:** - `python-dotenv` for secret management.
  - `Werkzeug` for secure hashing.
  - Session-based authentication via `Flask-Login`.
- **UI/UX:** Tailwind CSS, Lucide Icons, and Mobile-First responsive design.

## 🔐 System Logic & Permissions

| Feature                | Donor         | Volunteer     | Org Admin      |
|------------------------|:-------------:|:-------------:|:--------------:|
| Register New Center    |      ✅       |      ✅       |      ✅        |
| Add Items              |      ✅       |      ✅       |      ✅        |
| Increase Stock         |      ✅       |      ✅       |      ✅        |
| Decrease Stock (Take)  |      ❌       |      ✅       |      ✅        |
| View Activity Logs     |      ❌       |      ✅       |      ✅        |
| Delete Item Records    |      ❌       |      ✅       |      ✅        |

## 🚦 Getting Started

### 1. Prerequisites
- Python 3.10+
- Virtual Environment (`venv`)

### 2. Installation
```bash
git clone [https://github.com/yourusername/shelf-io.git](https://github.com/yourusername/shelf-io.git)
cd shelf-io
pip install -r requirements.txt
