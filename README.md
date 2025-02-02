# 🛒 IITM MAD1 - Grocery Store App

## 📌 Project Overview
This project is a **grocery store web application** built as part of the IIT Madras **Modern Application Development 1 (MAD1)** course. The project consists of three major segments:
- **Shop** (Customer Interface)
- **Manager** (Admin/Store Management)
- **User** (Authentication & Profiles)

The application enables users to browse grocery products, add items to the cart, and manage their accounts. Store managers have additional access to manage products and view transaction details.

🚫 **Restrictions:**  
- **No JavaScript or Frontend Frameworks:** JavaScript was **not** allowed for this project.
- **No CSS Frameworks like Tailwind or Bootstrap:** Only **pure CSS** was used for styling.

---

## 🏗️ Architecture & Features

### 🏛️ Structure
The project is structured as follows:

```
iitm-mad1-project/
│   api.yaml
│   app.py
│   database.db
│   Project Report.pdf
│   readme.txt
│   requirements.txt
│
├───app_contents
│   │   api.py
│   │   functions.py
│   │   routes_manager.py
│   │   routes_market.py
│   │   routes_user.py
│   │   tempCodeRunnerFile.py
│   │   __init__.py
│   │
│   ├───static
│   │   │   styles.css
│   │   │
│   │   └───styles
│   │           cart.css
│   │           common.css
│   │           delete_page.css
│   │           manager.css
│   │           register.css
│   │           search.css
│   │           shop.css
│   │
│   └───templates
│           add_category.html
│           add_product.html
│           base.html
│           cart.html
│           delete_page.html
│           edit_category.html
│           edit_product.html
│           home.html
│           login.html
│           management_cat.html
│           management_prod.html
│           manager.html
│           manager_login.html
│           new_manager.html
│           register.html
│           search.html
│           shop.html
│           user_page.html
│
└───media
        (Contains product images)
```

### 🔹 Features
✔️ **User Registration & Login** (with validation)  
✔️ **Shopping Cart System** (Add, Remove, View Items)  
✔️ **Form Validations** (Regex-based input validation)  
✔️ **Manager Dashboard** (Manage categories & products)  
✔️ **Dark Theme UI** (Minimal and easy on the eyes)  
✔️ **Flash Messages** (User feedback messages for actions)  
✔️ **Image Storage** (Base64 conversion for storing images)  
✔️ **REST API** (Fetching categories and products, adding items to cart)  

---

## 🔧 Technologies Used
The project is built using:

- **Backend:** Flask (Python)
- **Database:** SQLite3
- **Styling:** Pure CSS (No Tailwind, Bootstrap, or any CSS framework)
- **Modules Used:**
  - `flask`
  - `sqlite3`
  - `datetime` (For timestamps)
  - `random` (For generating barcodes)
  - `os` (For file paths & directories)
  - `re` (For regex-based form validation)
  - `base64` (For encoding images)

---

## 🔍 Database Schema
The project has **six tables** in SQLite:

1. **items** - Stores product details.
2. **transactions** - Records all purchase activities.
3. **category** - Contains product classifications.
4. **images** - Stores image data.
5. **manager** - Holds store manager details.
6. **users** - Stores customer profiles.

---

## 🔨 How to Run Locally
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/iitm-mad1-project.git
cd iitm-mad1-project
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Flask Server
```bash
python app.py
```
The app should now be running at **`http://127.0.0.1:5000/`** 🎉

---



## 🎥 Demo Video
Watch the full project demo here:  
[![Watch on YouTube](https://img.shields.io/badge/YouTube-Watch-red?style=flat&logo=youtube)](https://youtu.be/QDkbHYFHq-E)

---

## 📜 License
This project is licensed under **MIT License**. Feel free to use and modify it.

---

## 📞 Contact
For any queries, reach out:  
📧 **21f3000492@ds.study.iitm.ac.in**  
👨‍💻 **[LinkedIn Profile](#)** _(Optional)_



🚀 **Developed with ❤️ by Subrahmanyam H V S P Balabhadrapatruni** 🚀  

