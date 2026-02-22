# Shelf.io | Community Resource Management

A high-performance, real-time logistics and team management portal designed for community shelves and food banks. Built with a focus on administrative transparency and seamless volunteer onboarding.

## 🚀 Key Features (Cycle 2 Complete)

* **Live Audit Trail:** Real-time transaction logging with an encrypted ledger feel, tracking every item addition and removal with timestamps.
* **Dynamic Team Management:** Founder-level controls to authorize volunteers or revoke access instantly via an asynchronous administrative API.
* **Edit-in-Place Mission Statement:** A premium UX feature allowing Founders to update the organization's mission statement directly from the hero section without page reloads.
* **Role-Based Access Control (RBAC):** Distinct permission tiers for Founders (Full Control), Volunteers (Write Access), and Donors (Read-Only).
* **Onboarding System:** Secure, organization-specific access codes for rapid volunteer deployment.

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLAlchemy (SQLite)
* **Frontend:** Tailwind CSS, Jinja2 Templates
* **Icons:** Lucide-JS
* **Authentication:** Flask-Login

## 📂 Project Structure

```text
├── app.py              # Central logic and API endpoints
├── models.py           # Database schema (User, Org, Logs, Items)
├── templates/
│   ├── index.html      # Main Shelf Dashboard
│   ├── team.html       # Team Management & Audit Portal
│   └── login.html      # Secure Gateway
└── static/             # Assets and custom JS
