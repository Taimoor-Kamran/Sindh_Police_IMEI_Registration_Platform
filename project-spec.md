# Sindh Police IMEI Registration System - SpecifyPlus Specification

## Project Overview
**Project Name:** Sindh Police Mobile IMEI Registration Platform
**Description:** Mobile Snatching Prevention Platform powered by Sindh Police for device registration, ownership transfer, and incident reporting
**Tech Stack:** FastAPI + PostgreSQL + Next.js + Tailwind CSS
**Deployment:** Vercel (Frontend) + AWS (Backend + Database)

---

## Phase 1: Landing Page, Registration, Login & Dashboard

### 1.1 Landing Page
**Route:** `/`
**Page Title:** "Mobile Snatching Prevention Platform - Sindh Police"

**Layout:**
- Header with Sindh Police logo and bilingual text (English/Urdu)
- Hero section with main heading and description
- Two primary CTA buttons
- Features grid (4 cards)
- Footer

**Content:**
```
Main Heading: "Mobile Snatching Prevention Platform"
Subtitle (English): "Powered by Sindh Police Guidance"
Subtitle (Urdu): "سندھ پولیس کی رہنمائی میں"
Description: "Register your mobile devices, transfer ownership securely, and report snatching incidents for swift police action."
```

**UI Components:**
1. **Button 1 - Citizen Registration**
   - Text: "Citizen Registration" 
   - Icon: User icon
   - Action: Navigate to `/register`
   - Style: Primary button (green)

2. **Button 2 - Police Portal**
   - Text: "Police Portal"
   - Icon: Shield icon
   - Action: Navigate to `/login`
   - Style: Secondary button (gold accent)

**Features Grid:**
1. Device Registration - "Secure your mobile devices with official registration"
2. Ownership Transfer - "Legally transfer device ownership with proper documentation"
3. Report Incidents - "Quick reporting system for snatching incidents"
4. Police Action - "Direct connection to Sindh Police for swift response"

**Design Requirements:**
- Sindh Police brand colors: Primary green (#0a4d3c), Gold accent (#ffd700)
- Professional, trustworthy government aesthetic
- Bilingual support (English + Urdu)
- Responsive design (mobile-first)
- Tailwind CSS styling

---

### 1.2 Registration Page
**Route:** `/register`
**Page Title:** "Mobile Owner Registration"

**Form Fields:**
1. **Full Name**
   - Type: text
   - Required: Yes
   - Validation: Min 3 characters
   - Placeholder: "Enter your full name"

2. **CNIC (13 digits)**
   - Type: text
   - Required: Yes
   - Validation: Exactly 13 digits, format XXXXX-XXXXXXX-X
   - Placeholder: "XXXXX-XXXXXXX-X"
   - Pattern: ^[0-9]{5}-[0-9]{7}-[0-9]$

3. **Mobile Number**
   - Type: tel
   - Required: Yes
   - Validation: Must start with 03, 11 digits total
   - Placeholder: "03XX-XXXXXXX"
   - Pattern: ^03[0-9]{9}$

4. **Email**
   - Type: email
   - Required: Yes
   - Validation: Valid email format
   - Placeholder: "your.email@example.com"

5. **Username**
   - Type: text
   - Required: Yes
   - Validation: Min 4 characters, alphanumeric
   - Placeholder: "Choose a username"
   - Unique: Yes

6. **Password**
   - Type: password
   - Required: Yes
   - Validation: Min 8 characters, must include uppercase, lowercase, number
   - Placeholder: "Minimum 8 characters"

7. **Confirm Password**
   - Type: password
   - Required: Yes
   - Validation: Must match password field
   - Placeholder: "Re-enter your password"

**Submit Button:**
- Text: "Register"
- Action: POST to `/api/auth/register`
- On Success: Navigate to `/dashboard`
- On Error: Display validation errors inline

**Footer Link:**
- Text: "Already have an account? Login here"
- Action: Navigate to `/login`

**Backend API Endpoint:**
```
POST /api/auth/register
Request Body: {
  full_name: string,
  cnic: string (13 digits),
  mobile: string (11 digits),
  email: string,
  username: string,
  password: string
}
Response: {
  success: boolean,
  message: string,
  user_id: integer,
  token: string (JWT)
}
```

**Database Table: users**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  full_name VARCHAR(255) NOT NULL,
  cnic VARCHAR(15) UNIQUE NOT NULL,
  mobile VARCHAR(15) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'citizen',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  is_active BOOLEAN DEFAULT true
);
```

---

### 1.3 Login Page
**Route:** `/login`
**Page Title:** "Login to Portal"

**Form Fields:**
1. **Username**
   - Type: text
   - Required: Yes
   - Placeholder: "Enter your username"

2. **Password**
   - Type: password
   - Required: Yes
   - Placeholder: "Enter your password"

**Submit Button:**
- Text: "Login"
- Action: POST to `/api/auth/login`
- On Success: Navigate to `/dashboard`
- On Error: Display error message

**Footer Link:**
- Text: "Don't have an account? Register here"
- Action: Navigate to `/register`

**Backend API Endpoint:**
```
POST /api/auth/login
Request Body: {
  username: string,
  password: string
}
Response: {
  success: boolean,
  message: string,
  token: string (JWT),
  user: {
    id: integer,
    username: string,
    full_name: string,
    role: string
  }
}
```

---

### 1.4 Dashboard Page
**Route:** `/dashboard`
**Page Title:** "Dashboard - Sindh Police IMEI"
**Authentication:** Required (JWT)

**Layout:**
- Left sidebar with navigation
- Top header with user info and logout
- Main content area

**Sidebar Navigation Items:**
1. **My Mobiles**
   - Icon: Phone icon
   - Route: `/dashboard/mobiles`
   - Active by default

2. **Transfer Ownership**
   - Icon: Users icon
   - Route: `/dashboard/transfer`

3. **Report Snatching**
   - Icon: FileText icon
   - Route: `/dashboard/report`

4. **My Profile**
   - Icon: User icon
   - Route: `/dashboard/profile`

**Top Header:**
- Sindh Police logo
- User name display
- Logout button

**My Mobiles Section (Default View):**
- Welcome message
- Stats cards showing:
  - Total registered devices: 0
  - Pending transfers: 0
  - Active reports: 0
- Primary action button: "Register New Mobile"
- Empty state message (initially)

**Sidebar Design:**
- Fixed left sidebar (250px width)
- Green background (#0a4d3c)
- White text
- Active item highlighted with gold accent
- Responsive: Collapsible on mobile

**Protected Route:**
- Check JWT token validity
- If not authenticated, redirect to `/login`
- Store token in localStorage/cookies

---

## Security Requirements

### Authentication
- JWT tokens with 24-hour expiration
- Secure password hashing (bcrypt, min 10 rounds)
- HTTP-only cookies for token storage
- CSRF protection

### Authorization
- Role-based access control (citizen, police_officer, admin)
- Protected API endpoints
- Route guards on frontend

### Data Validation
- Server-side validation for all inputs
- SQL injection prevention (parameterized queries)
- XSS protection
- Rate limiting on authentication endpoints

---

## Database Schema (Phase 1)

```sql
-- Users table (already defined above)

-- Sessions table for JWT tracking
CREATE TABLE sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  token_hash VARCHAR(255) NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  ip_address VARCHAR(45),
  user_agent TEXT
);

-- Create indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_cnic ON users(cnic);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_expires_at ON sessions(expires_at);
```

---

## API Endpoints (Phase 1)

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/verify` - Verify JWT token
- `POST /api/auth/refresh` - Refresh JWT token

### User Profile
- `GET /api/user/profile` - Get current user profile
- `PUT /api/user/profile` - Update user profile

---

## Frontend Routes (Phase 1)

### Public Routes
- `/` - Landing page
- `/register` - Registration page
- `/login` - Login page

### Protected Routes (require authentication)
- `/dashboard` - Main dashboard (redirects to /dashboard/mobiles)
- `/dashboard/mobiles` - My mobiles section
- `/dashboard/transfer` - Transfer ownership section
- `/dashboard/report` - Report snatching section
- `/dashboard/profile` - User profile section

---

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/sindh_police_imei
JWT_SECRET_KEY=<generate-secure-random-key>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
BACKEND_PORT=8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=Sindh Police IMEI Platform
```

---

## Deployment Configuration

### Vercel (Frontend)
- Framework: Next.js
- Build command: `npm run build`
- Output directory: `.next`
- Environment variables: NEXT_PUBLIC_API_URL

### AWS (Backend)
- Service: EC2 or ECS
- Database: RDS PostgreSQL
- Load Balancer: ALB
- SSL: ACM Certificate
- Environment: Production

### GitHub
- Repository: sindh-police-imei-system
- Branches: main (production), develop (staging)
- CI/CD: GitHub Actions
- Auto-deploy on push to main

---

## Design System

### Colors
```css
Primary Green: #0a4d3c
Primary Green Light: #1a7f5e
Accent Gold: #ffd700
White: #ffffff
Gray: #6c757d
Success: #28a745
Danger: #dc3545
Warning: #ffc107
```

### Typography
- Primary Font: Inter (English)
- Urdu Font: Noto Nastaliq Urdu
- Headings: 700 weight
- Body: 400 weight

### Components
- Buttons: Rounded (md), shadow on hover
- Inputs: Border gray-300, focus ring green
- Cards: White background, shadow-md
- Sidebar: Fixed, green background
- Modals: Centered, backdrop blur

---

## Development Commands

### Generate Project
```bash
specifyplus generate --spec project-spec.md --output .
```

### Install Dependencies
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### Run Development
```bash
# Backend
cd backend && uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm run dev
```

### Database Setup
```bash
# Create database
createdb sindh_police_imei

# Run migrations
cd backend && alembic upgrade head
```

---

## Next Steps (Phase 2 - To be specified later)
- Device registration functionality
- Ownership transfer workflow
- Incident reporting system
- Police dashboard
- Admin panel
- SMS/Email notifications
- Document upload/verification
- IMEI verification with PTA database
- Reporting and analytics
