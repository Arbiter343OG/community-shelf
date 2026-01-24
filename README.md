# 🍎 Shelf.io | Community Food Pantry Manager

Shelf.io is a lightweight, secure inventory management system designed for community food pantries. It bridges the gap between donors and volunteers, ensuring real-time visibility of stock levels to reduce food waste and improve community support.

## 🚀 Key Features
- **Role-Based Access:** Distinct permissions for 'Donors' (Guests) and 'Volunteers' (Admins).
- **Real-Time Inventory:** Search, filter by category, and track stock quantities.
- **Impact Tracking:** Live dashboard showing total items shared with the community.
- **Mobile Responsive:** Clean, modern UI built with Tailwind CSS for use on-site at pantries.

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Database:** SQLAlchemy (SQLite/PostgreSQL)
- **Auth:** Flask-Login (Password Hashing with PBKDF2)
- **Frontend:** HTML5, Tailwind CSS, Lucide Icons

## 🔐 Permissions Matrix
| Action                | Donor (Guest) | Volunteer (Admin) |
|-----------------------|:-------------:|:-----------------:|
| Add New Items         |      ✅       |        ✅         |
| Increase Stock (+)    |      ✅       |        ✅         |
| Edit Details          |      ✅       |        ✅         |
| Decrease Stock (Take) |      ❌       |        ✅         |
| Delete Items          |      ❌       |        ✅         |

## 🏁 Quick Start
1. **Clone the repo:** `git clone https://github.com/yourusername/shelf-io.git`
2. **Install dependencies:** `pip install flask flask-sqlalchemy flask-login`
3. **Run the app:** `python app.py`
4. **Log in:** Use `admin/123` for Volunteer access or `guest/123` for Donor access.
