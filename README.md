# 🛡️ Shelf.io
### Smart Community Inventory & Donation Management

> **Making sure donations reach people—not landfills.**

Shelf.io is a modern inventory management platform built for food banks, charities, NGOs, and community organizations. It helps teams track incoming donations, monitor inventory in real time, reduce waste through expiry management, and maintain transparent audit records.

Designed with simplicity and reliability in mind, Shelf.io transforms traditional donation storage into a collaborative, data-driven system.

---

# ✨ Features

## 📦 Real-Time Inventory

- Instant quantity updates without page reloads
- Live stock levels
- Fast Add/Take workflows
- Dynamic inventory cards

---

## 🏷️ Smart Categorization

Organize donations into dedicated categories:

- 🍎 Produce
- 🥛 Dairy
- 🍞 Bakery
- 🥫 Canned Goods
- 📦 General Supplies

Each category automatically suggests appropriate units of measurement.

---

## 📏 Intelligent Unit Management

Category-specific units such as:

| Category | Units |
|----------|--------|
| Produce | kg, g, pcs, bundles |
| Dairy | L, ml, cartons |
| Bakery | loaves, dozens |
| Canned | cans, cases |
| General | units, boxes |

---

## ⏰ Expiry Tracking

Shelf.io actively monitors expiration dates and visually prioritizes inventory.

### Fresh
🟢 Plenty of time remaining

### Expires Soon
🟡 Approaching expiration

### Urgent
🔴 Critical attention required

### Expired
⚫ Clearly marked for removal

---

## 🚨 Low Stock Intelligence

Custom thresholds allow organizations to monitor essential items.

- Configurable alerts
- Visual warning badges
- Automatic inventory monitoring

---

## 👥 Role-Based Access Control

Different users have different capabilities.

### Founder
- Full inventory management
- Team management
- Mission editing
- Data exports

### Volunteer
- Inventory operations
- Stock updates
- Export reports

### Donor
- View inventory
- Contribute supplies

---

## 🎙️ Voice Search

Quickly search inventory using browser speech recognition.

- Hands-free lookup
- Instant search results

---

## 📊 Audit Trail

Every inventory action is logged.

Track:

- User
- Timestamp
- Item
- Quantity change

Providing accountability and transparency.

---

## 📈 Data Export

Generate audit-ready reports.

Supported format:

- Excel (.xlsx)

Perfect for:

- Administrative reviews
- Grant reporting
- Internal analytics

---

## 🌙 Modern Interface

- Responsive design
- Persistent dark mode
- Mobile-friendly layout
- Animated interactions
- Lucide icon system

---

# 🛠 Technology Stack

## Backend

- Python
- Flask
- SQLAlchemy
- SQLite

## Frontend

- Tailwind CSS
- Jinja2
- Vanilla JavaScript
- Lucide Icons

## Data

- OpenPyXL
- Pandas

---

# 🏗 Architecture

```
Donor
   │
   ▼
Shelf.io Dashboard
   │
   ├── Inventory Engine
   ├── Expiry Manager
   ├── Audit Logger
   ├── Role Manager
   └── Reporting System
          │
          ▼
     SQLite Database
```

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/shelf-io.git
cd shelf-io
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

# 🎯 Project Goals

Shelf.io aims to:

- Reduce donation waste
- Improve inventory visibility
- Simplify volunteer workflows
- Increase organizational transparency
- Support local communities through better logistics

---

# 🔮 Roadmap

## Current

- ✅ Real-time inventory
- ✅ Expiry tracking
- ✅ Audit logs
- ✅ RBAC
- ✅ Voice search
- ✅ Data exports
- ✅ Dark mode

## Planned

- 🔄 Barcode scanning
- 📱 Progressive Web App
- 📊 Advanced analytics
- 🔔 Smart notifications
- 📦 Multi-location inventory
- 🤖 AI demand forecasting

---

# 🤝 Contributing

Contributions, suggestions, and feature requests are welcome.

Fork the repository, create a branch, and submit a pull request.

---

# 📄 License

This project is licensed under the MIT License.

---

# ❤️ Built for Communities

Shelf.io was created with a simple idea:

**Donations should spend less time being managed and more time helping people.**
