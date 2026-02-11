# Sindh Police IMEI Registration System - Build Instructions

## Project Overview
Build a complete full-stack application for Sindh Police Mobile IMEI Registration and Management Platform.

**Specification File:** `project-spec.md` (READ THIS FIRST!)

---

## Tech Stack & Skills to Use

### Backend
- **Framework:** FastAPI (use `/fastapi` skill)
- **Database:** PostgreSQL with SQLModel (use `/sqlmodel` skill)
- **Testing:** Pytest (use `/pytest` skill)

### Frontend
- **Framework:** Next.js (use `/nextjs` skill)
- **Styling:** Tailwind CSS (use `/tailwindcss` skill)
- **UI/UX:** Use `/uiux-design-context7` skill for professional design
- **Authentication:** Better Auth (use `/better-auth` skill)
- **Type Safety:** TypeScript (use `/typescript-context7` skill)

### Additional Skills
- **React Components:** Use `/react-context7` skill
- **Design System:** Use `/designsystemet-context7` for consistent UI
- **UX Principles:** Use `/lawsofux-context7` for better user experience

---

## Phase 1 Implementation Tasks

### Task 1: Project Structure Setup
Create the following folder structure:

```
sindh_police_application/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── database.py
│   │   ├── config.py
│   │   └── utils/
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/
├── frontend/
│   ├── app/
│   │   ├── page.tsx (Landing)
│   │   ├── register/
│   │   ├── login/
│   │   └── dashboard/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.ts
│   └── tsconfig.json
└── README.md
```

---

### Task 2: Backend Development (FastAPI + SQLModel)

#### Use Skills:
- `/fastapi` - For API structure and best practices
- `/sqlmodel` - For database models
- `/pytest` - For testing

#### Create Files:

1. **backend/requirements.txt**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic-settings==2.1.0
alembic==1.13.0
```

2. **backend/app/config.py**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/sindh_police_imei"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    class Config:
        env_file = ".env"

settings = Settings()
```

3. **backend/app/models/user.py** - User SQLModel
4. **backend/app/database.py** - Database connection
5. **backend/app/utils/security.py** - Password hashing, JWT
6. **backend/app/routes/auth.py** - Register, Login, Logout endpoints
7. **backend/app/routes/user.py** - User profile endpoints
8. **backend/app/main.py** - FastAPI app initialization

---

### Task 3: Frontend Development (Next.js + Tailwind)

#### Use Skills:
- `/nextjs` - For Next.js 14 App Router best practices
- `/tailwindcss` - For styling
- `/react-context7` - For React components
- `/uiux-design-context7` - For professional UI/UX
- `/better-auth` - For authentication

#### Create Files:

1. **frontend/package.json**
```json
{
  "name": "sindh-police-imei-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "typescript": "5.3.3",
    "tailwindcss": "3.4.0",
    "lucide-react": "0.263.1",
    "axios": "1.6.2",
    "better-auth": "^0.5.0"
  }
}
```

2. **frontend/app/page.tsx** - Landing Page
   - Bilingual (English/Urdu) header
   - Hero section with title and description
   - Two CTA buttons (Register, Police Portal)
   - Features grid (4 cards)
   - Use Sindh Police colors: Green (#0a4d3c), Gold (#ffd700)

3. **frontend/app/register/page.tsx** - Registration Page
   - Form with all 7 fields (Full Name, CNIC, Mobile, Email, Username, Password, Confirm Password)
   - Client-side validation
   - API integration with backend
   - Professional government design

4. **frontend/app/login/page.tsx** - Login Page
   - Username and password fields
   - JWT token handling
   - Redirect to dashboard on success

5. **frontend/app/dashboard/layout.tsx** - Dashboard Layout
   - Left sidebar with navigation
   - Top header with user info
   - Protected route (check JWT)

6. **frontend/app/dashboard/page.tsx** - My Mobiles (default view)
   - Welcome message
   - Stats cards (0 devices, 0 transfers, 0 reports)
   - "Register New Mobile" button

7. **frontend/app/dashboard/transfer/page.tsx** - Transfer Ownership
8. **frontend/app/dashboard/report/page.tsx** - Report Snatching
9. **frontend/app/dashboard/profile/page.tsx** - User Profile

10. **frontend/components/** - Reusable components
    - Sidebar.tsx
    - Header.tsx
    - StatsCard.tsx
    - Button.tsx
    - Input.tsx

11. **frontend/tailwind.config.ts** - Tailwind configuration with Sindh Police colors

---

### Task 4: Database Setup

Create Alembic migrations for:
1. Users table (id, full_name, cnic, mobile, email, username, password_hash, role, created_at, updated_at, is_active)
2. Sessions table (id, user_id, token_hash, expires_at, created_at, ip_address, user_agent)

---

## Design Requirements

### Color Palette (Sindh Police Brand)
```css
--primary-green: #0a4d3c;
--primary-green-light: #1a7f5e;
--accent-gold: #ffd700;
--white: #ffffff;
--gray: #6c757d;
```

### Typography
- **English:** Inter font family
- **Urdu:** Noto Nastaliq Urdu font family
- Professional, clean, government aesthetic

### UI Components
- Rounded buttons with hover effects
- Input fields with focus states
- Cards with subtle shadows
- Sidebar with green background
- Gold accents for highlights

---

## Implementation Order

1. ✅ **Read project-spec.md** thoroughly
2. **Backend First:**
   - Database models (SQLModel)
   - API routes (FastAPI)
   - Authentication (JWT + bcrypt)
   - Testing (Pytest)
3. **Frontend Second:**
   - Landing page (Next.js + Tailwind)
   - Registration & Login pages
   - Dashboard with sidebar
   - Protected routes
4. **Integration:**
   - Connect frontend to backend API
   - Test authentication flow
   - Verify all Phase 1 features

---

## Key Features to Implement (Phase 1)

### Landing Page
✅ Bilingual header (English/Urdu)
✅ Hero section with description
✅ Two CTA buttons (Register, Police Portal)
✅ Features grid (4 cards)
✅ Professional government design

### Registration
✅ 7 input fields with validation
✅ CNIC format validation (XXXXX-XXXXXXX-X)
✅ Mobile format validation (03XX-XXXXXXX)
✅ Password strength requirements
✅ API integration with backend

### Login
✅ Username/password authentication
✅ JWT token generation
✅ Secure session management
✅ Redirect to dashboard

### Dashboard
✅ Left sidebar navigation (4 items)
✅ Protected routes (JWT verification)
✅ User profile display
✅ My Mobiles section with stats
✅ Placeholder sections (Transfer, Report, Profile)

---

## Skills Reference Guide

When implementing features, refer to these skills:

- **Backend API:** `/fastapi`
- **Database:** `/sqlmodel`
- **Testing:** `/pytest`
- **Frontend Framework:** `/nextjs`
- **Styling:** `/tailwindcss`, `/tailwindcss-animate-context7`
- **UI/UX:** `/uiux-design-context7`, `/designsystemet-context7`
- **React:** `/react-context7`
- **TypeScript:** `/typescript-context7`
- **Auth:** `/better-auth`

---

## Environment Setup

### Backend (.env)
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sindh_police_imei
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Sindh Police IMEI Platform
```

---

## Commands to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Database
```bash
createdb sindh_police_imei
cd backend
alembic upgrade head
```

---

## Success Criteria

Phase 1 is complete when:
- ✅ Landing page loads with correct branding
- ✅ Registration creates user in database
- ✅ Login generates JWT token
- ✅ Dashboard is protected and shows user info
- ✅ All 4 sidebar navigation items work
- ✅ UI matches Sindh Police brand colors
- ✅ Bilingual support works (English/Urdu)
- ✅ All validation rules work correctly
- ✅ API endpoints return proper responses
- ✅ Tests pass for critical functionality

---

## Next Steps (Phase 2)

After Phase 1 is complete, we will implement:
- Device registration (IMEI, model, brand)
- Ownership transfer workflow
- Snatching incident reporting
- Police dashboard
- Admin panel
- SMS/Email notifications
- Document upload/verification

---

**START BUILDING NOW!**

Read project-spec.md and begin implementing Phase 1 using the skills mentioned above.
