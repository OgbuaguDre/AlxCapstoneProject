
from pathlib import Path

A **Task Management API** built with **Django** and **Django REST Framework (DRF)**.  
The API allows users to manage personal tasks, with full **CRUD operations**, user authentication, and task ownership controls.



### Task Management (CRUD)
- Create, Read, Update, and Delete tasks.
- Task attributes: **Title, Description, Due Date, Priority Level (Low, Medium, High), Status (Pending, Completed)**.
- Validations: 
  - Due date must be in the future.  
  - Priority level restricted to predefined choices.  
  - Status updates enforce rules (completed tasks cannot be edited unless reverted).

### User Management (CRUD)
- Register, update, and delete users.
- Each user manages their own tasks only.
- Secure authentication to prevent unauthorized access.

### Task Completion Control
- Mark tasks as complete or incomplete.
- Store timestamp when a task is completed.
- Completed tasks cannot be edited unless reverted to incomplete.

### Task Filters and Sorting
- Filter tasks by **status, priority, or due date**.
- Sort tasks by **due date or priority level**.

---

### Authentication
- User authentication via **Django’s built-in system**.
- Optional **JWT (JSON Web Tokens)** for token-based authentication.

--

---

## 📖 API Design Principles
- RESTful architecture with proper HTTP methods:  
  - `GET` → Retrieve data  
  - `POST` → Create resources  
  - `PUT/PATCH` → Update resources  
  - `DELETE` → Remove resources  
- Proper error handling & status codes:  
  - `200` OK  
  - `201` Created  
  - `400` Bad Request  
  - `401` Unauthorized  
  - `403` Forbidden  
  - `404` Not Found  

---

## My Stretch Goals
- Task Categories  
- Notifications (email or in-app)  
- Task History  
- Collaborative Tasks (shared task editing)  

---


"""

# Write README.md file
readme_path = Path("/mnt/data/README.md")
readme_path.write_text(readme_content)

readme_path
