```markdown
# 🍽️ RestoAI System

An intelligent Restaurant Management System built with **Python, PyQt6, SQLite, and Speech Recognition**.  
The system combines restaurant order management, employee control, and smart interaction features like voice commands.

---

## 🚀 Features

### 👨‍🍳 Cashier System
- Browse meals and drinks with images
- Add orders with quantity selection
- Voice command ordering (Arabic support)
- Automatic total calculation
- Payment processing and change calculation
- Order reset after payment

### 👨‍💼 Manager System
- Add new employees
- Edit employee data
- Delete employees
- View all employees in a table

### 🗄️ Database (SQLite)
- Users table (login system)
- Employees table (CRUD operations)
- Persistent local storage

### 🎤 Voice Control
- Add orders using speech recognition
- Arabic language support (ar-SA)

---

## 🧠 Technologies Used

- Python 3
- PyQt6 (GUI)
- SQLite3 (Database)
- SpeechRecognition (Voice Input)
- Regex (Text Processing)

---

## 📁 Project Structure

```

RestoAI-System/
│
├── database_setup.py        # Create database & users
├── main.py                  # Main application (GUI system)
│
├── meals.ui                 # Cashier interface UI
├── log_in.ui                # Login interface
├── Manager.ui               # Manager dashboard
├── AddEmployee.ui
├── EditEmployee.ui
├── DeleteEmployee.ui
├── getEmployees.ui
│
├── photo/                   # Images for meals & drinks
│
└── restaurant.db           # SQLite database (auto generated)

````

---

## 🔐 Login System

Default users in database:

| Username | Password |
|----------|----------|
| Aiham    | 1234     |
| Mohammed | 1234     |
| Taiseer  | 1212     |
| Raed     | 1212     |

---

## ▶️ How to Run

1. Install requirements:
```bash
pip install PyQt6 SpeechRecognition pyaudio
````

2. Run database setup (first time only):

```bash
python database_setup.py
```

3. Run the project:

```bash
python main.py
```

---

## 💡 Future Improvements

* Add AI recommendation system for menu
* Online ordering system
* Cloud database integration
* Sales analytics dashboard
* Multi-language support UI

---

## 👨‍💻 Author

Developed by **Taiseer Al-Aidroos**

---

## ⭐ License

This project is for educational purposes.

```
```
