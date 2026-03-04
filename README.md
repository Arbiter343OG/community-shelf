# 🛡️ Shelf.io | Community Inventory Engine

**Shelf.io** is a real-time inventory management system designed to bridge the gap between donors and community organizations. Built with a focus on speed, reliability, and ease of use, it allows teams to track essential supplies, monitor stock levels, and generate audit-ready intelligence.

---

## 🚀 Key Features

* **Real-Time Stock Tracking**: Dynamic quantity updates using AJAX/Fetch API for instant "Add" and "Take" actions.
* **Intelligent Unit Management**: Category-specific Unit of Measure (UOM) selection (e.g., kg for Produce, Liters for Dairy).
* **Low-Stock Alerts**: Automated visual pulses and badges triggered when items fall below a custom-defined threshold.
* **Audit Logging**: Full traceability of every transaction, capturing timestamps, users, and specific inventory changes.
* **Data Intelligence**: Export capability for inventory and activity logs to `.xlsx` for administrative reporting.
* **Role-Based Access Control (RBAC)**: Specialized permissions for Founders, Volunteers, and Donors.

## 🛠️ Tech Stack

* **Backend**: Python / Flask
* **Database**: SQLAlchemy (SQLite)
* **Frontend**: Tailwind CSS, Jinja2 Templates
* **Interactivity**: Vanilla JavaScript / Lucide Icons
* **Data Processing**: Openpyxl / Pandas

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/yourusername/shelf-io.git](https://github.com/yourusername/shelf-io.git)
   cd shelf-io
