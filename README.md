# moustanadati 🚀

**moustanadati** is a lightweight document management system designed for environments with limited infrastructure and small teams.

🧪 **Status**: Early development — version 
🔐 **Current features**: Login and logout only

---

## 🎯 Mission

> **To build a lightweight, modular document management system tailored for limited infrastructure and small teams.**

*moustanadati* aims to deliver essential document handling features — authentication, access control, and structured storage — without the complexity of enterprise-grade solutions. It’s designed to be deployable on modest servers, maintainable by small dev teams, and extensible without friction.

---

## 🧱 Architecture Overview

The project follows Clean Architecture principles to ensure separation of concerns and long-term maintainability:

- **Use Cases**: Core business logic
- **Controllers**: Orchestrate use case execution
- **Presenters & ViewModels**: Decouple logic from presentation
- **Renderers**: Convert ViewModels into HTTP responses
- **Infrastructure**: Concrete implementations (Flask, SQLite, bcrypt…)

---

## 🔐 Current Features

- ✅ Login with bcrypt password verification
- ✅ Session-based authentication
- ✅ Logout with flash messaging

> ⚠️ No document features yet — this version is a technical foundation only.

---

## 📌 Roadmap

- [ ] Document container
- [ ] Document upload and storage
- [ ] Document versioning
- [ ] Document status and tags
- [ ] Trash and restore
- [ ] Favorites
- [ ] Sharing 
- [ ] Commenting
- [ ] Notifications
- [ ] Validation workflow
- [ ] Administration panel 

---

---

## 🚀 Getting Started

```bash
# Initialize the database with a default user
python init_db.py
# Start the Flask server 
python app.py
```

To log in during development, use the following credentials:
Username: user  
Password: 1234

