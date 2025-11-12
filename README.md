# 🏫 Hostel Management System

A full-featured **web-based hostel management system** built with **Flask**, **SQLAlchemy**, **Bootstrap 5**, and **Chart.js** for visual analytics. This system allows admins to manage students, rooms, hostels, staff, allocations, fees, complaints, maintenance requests, and visitors efficiently.

---

## 🌟 Features

### Core Features
- **Student Management:** Add, view, update, and delete student records.  
- **Room & Hostel Management:** Manage room capacity, status, and hostel details.  
- **Staff Management:** Track staff roles (warden, security, maintenance).  
- **Allocations:** Assign students to rooms with date ranges.  
- **Fees:** Track payment status (Paid, Unpaid, Overdue).  
- **Complaints & Maintenance:** Log complaints and maintenance requests.  
- **Visitors:** Record visitor details with host student association.  

### Dashboard Analytics
- Total students, rooms, hostels, staff, active allocations, visitors, complaints, and maintenance requests.  
- **Charts using Chart.js:**
  - Rooms per hostel  
  - Students per hostel  
  - Fee status breakdown  
  - Complaint status breakdown  
  - Staff role distribution  
  - Allocations per room  

---

## 🛠️ Technologies Used

- **Backend:** Python, Flask, SQLAlchemy  
- **Frontend:** HTML, CSS, Bootstrap 5, Jinja2 templates  
- **Charts & Visualizations:** Chart.js  
- **Database:** SQLite (or any SQLAlchemy-supported DB)  
- **Version Control:** Git & GitHub  

---

## ⚡ Installation

1. **Clone the repository:**
```bash
    git clone https://github.com/YOUR_USERNAME/hostel-management.git
    cd hostel-management
```

2. **Create a virtual environment and activate it:**
```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
```

3. **Install dependencies:**
```bash
    pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
# Create a .env file in the project root
    FLASK_APP=run.py
    FLASK_ENV=development
    DATABASE_URL=sqlite:///hostel.db
    SECRET_KEY=your_secret_key_here
```

5. **Initialize the database (if applicable):**
```bash
    flask db upgrade
```

6. **Run the application:**
```bash
    python run.py
```

7. **Open in browser:**
```bash
    Go to http://127.0.0.1:5000/dashboard
```

---

## 🔗 Project Structure

hostel-management/
├── app/
│   ├── models.py
│   ├── routes/
│   ├── templates/
│   └── static/
├── venv/
├── run.py
├── requirements.txt
└── .gitignore

---

## 📄 License

This project is licensed under the MIT License. See LICENSE for details.

---

## ⚡ Author

Yash Chugani
GitHub: [https://github.com/YashChugani](https://github.com/YashChugani)