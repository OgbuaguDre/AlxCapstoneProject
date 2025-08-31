# Task Management API

A backend API built with **Django** and **Django REST Framework (DRF)** that allows users to manage tasks with authentication, ownership, and filtering/sorting capabilities.

---

## Features Implemented 

- **User Authentication**
  - Registration and login using DRF token authentication.
  - Each user can only access and manage their own tasks.

- **Task Management (CRUD)**
  - Create, read, update, and delete tasks.
  - Task fields: `title`, `description`, `due_date`, `priority` (Low/Medium/High), `status` (Pending/Completed).
  - Validations: due date must be in the future, valid priority levels only.

- **Mark Tasks Complete/Incomplete**
  - Endpoints to toggle completion status.
  - Completion timestamp is stored when marked complete.
  - Tasks cannot be edited once completed unless reverted to incomplete.

- **Filters & Sorting**
  - Filter tasks by status (Pending/Completed), priority, or due date.
  - Sort tasks by due date or priority.

- **Testing**
  - Automated tests for:
    - User registration & login
    - Task CRUD operations
    - Ownership restrictions
    - Filters and sorting

---

## Project Status 

-  Functional requirements for tasks & users implemented.
-  Database schema with `User` and `Task` models designed.
-  Authentication + permissions working.
-  CRUD + completion toggle endpoints working.
-  Filters, sorting, and test coverage added.

---

## Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Database:** SQLite (dev), PostgreSQL (planned for production)
- **Authentication:** DRF Token Authentication






