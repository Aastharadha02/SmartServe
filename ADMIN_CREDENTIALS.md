# SmartServe Admin Credentials & Role Permission Matrix

> **Environment URL:** [http://localhost:5173/admin/login](http://localhost:5173/admin/login)  
> **Backend API URL:** [http://127.0.0.1:8000/api/v1](http://127.0.0.1:8000/api/v1)

---

## 1. Admin Accounts & Passwords

| Admin Name | Email Address | Password | Role Name | System Key |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@smartserve.com` | `AdminPassword123!` | Super Admin | `super_admin` |
| **Priya Sharma** | `priya.sharma@smartserve.com` | `AdminPassword123!` | Operations Admin | `operations_admin` |
| **Vikram Patel** | `vikram.patel@smartserve.com` | `AdminPassword123!` | Catalog Admin | `catalog_admin` |
| **Rahul Verma** | `rahul.verma@smartserve.com` | `AdminPassword123!` | Support Admin | `support_admin` |

---

## 2. Admin Roles & Permission Scope

### 1. Super Admin (`admin@smartserve.com`)
- **Access Level:** **Full Unrestricted Access**
- **Permissions:** Unrestricted wildcard (`*`) across all modules.
- **Allowed Actions:** Catalog mutations, emergency dispatch, provider reassignment, provider/customer suspensions, support ticketing, system email template management, security audit log revocation, admin account creation.

### 2. Operations Admin (`priya.sharma@smartserve.com`)
- **Access Level:** **Operations & Catalog Management**
- **Permissions:** `dashboard:view`, `catalog:edit`, `providers:manage`, `customers:view`, `bookings:manage`, `support:manage`
- **Allowed Actions:** Emergency dispatch, provider reassignment, state transitions, provider document verification & suspension, catalog pricing/details editing, support ticket replies & status updates.
- **Restricted (Read-Only):** Security center administration, creating new admin accounts, email template modifications.

### 3. Catalog Admin (`vikram.patel@smartserve.com`)
- **Access Level:** **Service Catalog Specialist**
- **Permissions:** `dashboard:view`, `catalog:manage`, `catalog:export`, `catalog:import`
- **Allowed Actions:** Full catalog CRUD, pricing updates, Excel bulk import (`.xlsx`), Excel catalog export.
- **Restricted (Read-Only):** All Bookings (cannot dispatch/reassign), People (cannot verify/suspend providers/customers), Support (cannot reply/escalate), Security (cannot revoke sessions).

### 4. Support Admin (`rahul.verma@smartserve.com`)
- **Access Level:** **Customer Support & Ticketing Specialist**
- **Permissions:** `dashboard:view`, `catalog:view`, `providers:view`, `customers:view`, `bookings:view`, `support:manage`
- **Allowed Actions:** Support ticket responses, ticket escalation, updating ticket priority & status.
- **Restricted (Read-Only):** Cannot edit service catalog, cannot dispatch emergency bookings, cannot reassign booking providers, cannot suspend providers or customers.

---

## 3. RBAC System Rules

1. **Navbar Visibility:** Every authenticated admin sees all 10 module sections in the navbar and sidebar.
2. **Read-Only Mode:** Viewing, searching, and filtering are open to all authenticated admins across all pages.
3. **Action-Level Locking:** Mutation buttons and form fields are disabled for admins lacking required permissions, displaying explicit tooltips and view-only banners.
4. **Backend Security:** FastAPI backend endpoints enforce `require_permission(...)` on all `POST`, `PUT`, `PATCH`, and `DELETE` requests and return **HTTP 403 Forbidden** if unauthorized.
