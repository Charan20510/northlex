# 🏛️ NORTHEAST LEGAL PORTAL — FULL STACK DJANGO BUILD PROMPT

## PROJECT OVERVIEW
Build a complete, end-to-end deployable **Legal Client Portal** for Northeast India using **Django (strictly)**. This is a multi-role platform connecting Clients, Advocates, and Admins — with location-based advocate booking, case tracking, secure chat, payments, and a special Northeast Law Hub.

The portal must be:
- Modern, premium, and visually stunning (teal/blue/white palette)
- Designed for **common people** — simple, fast, mobile-friendly
- Production-ready and deployable on platforms like Railway, Render, or VPS
- Strictly Django (no React/Next.js) — use Django templates + HTMX + Alpine.js for interactivity

---

## TECH STACK (STRICT)
- **Backend**: Django 4.2+ (Python 3.11+)
- **Database**: PostgreSQL (primary), SQLite (dev fallback)
- **Frontend**: Django Templates + TailwindCSS (via CDN or django-tailwind) + Alpine.js + HTMX
- **Auth**: Django Allauth (OTP via mobile + email login)
- **Chat**: Django Channels (WebSocket) + Redis
- **Payments**: Razorpay (Indian UPI/card/wallet)
- **File Storage**: Django Storages + AWS S3 (or local media for dev)
- **PDF Generation**: WeasyPrint or ReportLab
- **Maps/Location**: Leaflet.js (OpenStreetMap, no Google API key needed)
- **Task Queue**: Celery + Redis (for notifications, emails)
- **Deployment**: Gunicorn + Nginx ready; `.env` based config; `Procfile` for Railway/Render

---

## PROJECT STRUCTURE
```
legal_portal/
├── manage.py
├── requirements.txt
├── .env.example
├── Procfile
├── legal_portal/          # Django project settings
│   ├── settings/
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── asgi.py            # Channels/WebSocket
│   └── celery.py
├── apps/
│   ├── accounts/          # Users, roles, OTP, registration
│   ├── advocates/         # Advocate profiles, HC/SC AOR
│   ├── clients/           # Client profiles, onboarding
│   ├── bookings/          # Location-based advocate booking
│   ├── cases/             # Case management, status, timeline
│   ├── chat/              # WebSocket chat (client↔advocate, client↔admin)
│   ├── payments/          # Razorpay integration, receipts
│   ├── feedback/          # Star ratings, reviews, moderation
│   ├── northeast_hub/     # NE Law Hub content management
│   ├── documents/         # Secure document upload/storage
│   ├── notifications/     # In-app + email notifications
│   └── admin_panel/       # Extended Django admin + custom views
├── templates/
│   ├── base.html
│   ├── components/
│   ├── accounts/
│   ├── dashboard/
│   ├── advocates/
│   ├── cases/
│   ├── chat/
│   ├── payments/
│   ├── northeast_hub/
│   └── admin_panel/
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## DATABASE MODELS (Build All of These)

### App: `accounts`
```python
# CustomUser — base model for all roles
class CustomUser(AbstractUser):
    role = CharField(choices=['CLIENT', 'ADVOCATE', 'ADMIN'])
    mobile = CharField(unique=True)
    is_mobile_verified = BooleanField(default=False)
    is_approved = BooleanField(default=False)  # Admin must approve
    profile_photo = ImageField(upload_to='profiles/')
    created_at = DateTimeField(auto_now_add=True)

class OTPVerification:
    user, otp_code, created_at, is_used
```

### App: `clients`
```python
class ClientProfile:
    user (OneToOne → CustomUser)
    full_name, father_or_spouse_name, dob, gender
    mobile, email, permanent_address
    state, district
    aadhaar_number, pan_number, voter_id
    photo (ImageField), id_proof (FileField), signature (ImageField)
    latitude, longitude  # live location (optional)
    issue_category (FK → IssueCategory)
    is_location_enabled (BooleanField)
```

### App: `advocates`
```python
class AdvocateProfile:
    user (OneToOne → CustomUser)
    full_name, father_or_spouse_name, dob, gender
    mobile, email, residential_address
    bar_council_state, enrollment_number, enrollment_date
    years_of_practice
    practice_type (choices: Independent/Law Firm/Chamber/Corporate)
    office_address
    court_of_practice (choices: District/High Court/Supreme Court/Tribunal)
    primary_practice_area, secondary_practice_area
    aadhaar_number (optional), pan_number
    emergency_contact_name, emergency_contact_relation, emergency_contact_number
    profile_photo, signature
    is_aor = BooleanField()  # Supreme Court Advocate-on-Record
    is_verified = BooleanField(default=False)
    is_available = BooleanField(default=True)
    latitude, longitude  # for location matching
    consultation_fee, case_fee
    rating (DecimalField, computed from feedback)

class AdvocateDocument:
    advocate (FK), document_type, file, uploaded_at
```

### App: `bookings`
```python
class Booking:
    client (FK → ClientProfile)
    advocate (FK → AdvocateProfile)
    booking_type (choices: DISTRICT/HIGH_COURT/SUPREME_COURT_AOR)
    issue_category (FK)
    status (choices: PENDING/APPROVED/REJECTED/COMPLETED/CANCELLED)
    admin_approved = BooleanField(default=False)
    notes (TextField)
    created_at, updated_at
    # Admin can replace advocate
    replaced_advocate (FK → AdvocateProfile, null=True)
    admin_notes (TextField)

class IssueCategory:
    name, description, icon_name
```

### App: `cases`
```python
class Case:
    client (FK → ClientProfile)
    advocate (FK → AdvocateProfile)
    booking (OneToOne → Booking)
    case_title, case_number, case_type (Civil/Criminal/Arbitration)
    court_name, filing_date
    status (choices: PENDING/ACTIVE/CLOSED/ADJOURNED)
    stage (choices: FILING/EVIDENCE/ARGUMENT/JUDGMENT)
    opponent_details (TextField)
    case_summary (TextField)
    admin_notes (TextField)

class Hearing:
    case (FK → Case)
    hearing_date, next_hearing_date
    what_happened (TextField)
    judge_remarks (TextField)
    status (choices: SCHEDULED/COMPLETED/ADJOURNED)
    added_by (FK → CustomUser)

class CaseDocument:
    case (FK)
    uploaded_by (FK → CustomUser)
    document_type (choices: EVIDENCE/ID/COURT_ORDER/OTHER)
    file (FileField)
    notes, uploaded_at

class CaseTimeline:
    case (FK), event_description, created_by (FK), created_at
```

### App: `chat`
```python
class ChatRoom:
    room_type (choices: CLIENT_ADVOCATE/CLIENT_ADMIN/ADMIN_ADVOCATE)
    client (FK → ClientProfile, null=True)
    advocate (FK → AdvocateProfile, null=True)
    booking (FK → Booking)
    created_at

class Message:
    room (FK → ChatRoom)
    sender (FK → CustomUser)
    content (TextField)  # text only, no phone numbers allowed
    is_read (BooleanField)
    sent_at
    # Content filter: auto-block phone number patterns
```

### App: `payments`
```python
class Payment:
    client (FK → ClientProfile)
    booking (FK → Booking)
    payment_type (choices: CONSULTATION/CASE_ASSIGNMENT/DRAFTING/AOR_FEE)
    amount (DecimalField)
    razorpay_order_id, razorpay_payment_id
    status (choices: PENDING/SUCCESS/FAILED/REFUNDED)
    created_at
    admin_commission (DecimalField)
    advocate_share (DecimalField)

class CommissionConfig:
    payment_type, commission_percentage, updated_by, updated_at
```

### App: `feedback`
```python
class Feedback:
    client (FK → ClientProfile)
    advocate (FK → AdvocateProfile)
    booking (FK → Booking)
    rating (IntegerField, 1-5)
    review_text (TextField)
    attachment (FileField, optional)
    is_visible (BooleanField, default=True)  # Admin can hide
    public_reply (TextField, null=True)  # Advocate public reply, moderated
    created_at
```

### App: `northeast_hub`
```python
class NEHubArticle:
    title, slug, state (choices: all NE states)
    category (choices: STATE_LAW/CUSTOMARY_LAW/CRIMINAL/LAND_LAW/HUMAN_RIGHTS/WOMEN_CHILD/HELPLINE/JUDGMENTS)
    content (RichTextField)
    is_published (BooleanField)
    author (FK → CustomUser)
    created_at, updated_at

class HelplineContact:
    name, state, phone, email, category, is_active
```

---

## VIEWS & URL STRUCTURE

### Public Pages
```
/                          → Landing page (premium hero, features, CTA)
/login/                    → OTP/email login
/register/                 → Client registration (3-step onboarding)
/northeast-hub/            → NE Law Hub (public)
/northeast-hub/<slug>/     → Article detail
```

### Client Dashboard (login required, role=CLIENT)
```
/dashboard/                → Main dashboard with all icons
/dashboard/book-advocate/  → Location-based booking
/dashboard/high-court/     → High Court advocates list
/dashboard/supreme-court/  → Supreme Court AOR list
/dashboard/cases/          → My cases list
/dashboard/cases/<id>/     → Case detail + timeline + documents
/dashboard/chat/           → Chat rooms list
/dashboard/chat/<room_id>/ → Chat room (WebSocket)
/dashboard/payments/       → Payment history
/dashboard/payments/pay/<booking_id>/ → Make payment (Razorpay)
/dashboard/feedback/<booking_id>/    → Submit feedback
/dashboard/contact-admin/  → Message admin
/dashboard/profile/        → Edit profile
```

### Advocate Portal (login required, role=ADVOCATE)
```
/advocate/dashboard/       → Advocate dashboard
/advocate/bookings/        → Incoming booking requests
/advocate/cases/           → Assigned cases
/advocate/cases/<id>/update/ → Add hearing/update case status
/advocate/cases/<id>/documents/ → Upload documents
/advocate/chat/            → Chat rooms (NO client phone numbers shown EVER)
/advocate/profile/         → Edit profile + update location
/advocate/feedback/        → View feedback (public replies only)
```

### Admin Panel (login required, role=ADMIN)
```
/admin-portal/             → Admin dashboard
/admin-portal/clients/     → All clients (view/approve/reject/ban)
/admin-portal/advocates/   → All advocates (verify/approve/ban)
/admin-portal/bookings/    → All bookings (approve/reject/replace advocate)
/admin-portal/cases/       → All cases (edit status, add notes)
/admin-portal/chat-logs/   → All chat logs
/admin-portal/payments/    → Full payment records + commission config
/admin-portal/feedback/    → Moderate feedback
/admin-portal/northeast-hub/ → Add/edit/delete NE Hub articles
/admin-portal/notifications/ → Send broadcast notifications
```

---

## CORE FEATURE IMPLEMENTATIONS

### 1. OTP-Based Login
- Use `django-allauth` or custom OTP with `twilio`/`MSG91`/`fast2sms` (Indian provider)
- Fallback: email link login
- On mobile: 6-digit OTP sent to number, expires in 10 minutes

### 2. Location-Based Advocate Matching
```python
# In bookings/views.py
def get_nearest_advocates(client_lat, client_lon, radius_km=50):
    from math import radians, cos, sin, asin, sqrt
    # Haversine formula — no external API needed
    # Filter advocates by district first, then by specialization
    # Return ordered queryset by distance
```
- Use Leaflet.js on frontend to show map with advocate pins
- Client clicks "Book" → creates Booking record → notifies Admin + Advocate via Django Channels

### 3. Privacy Protection (CRITICAL)
```python
# In chat/consumers.py and advocate/views.py
# NEVER pass client.mobile or client.email to advocate context
# Middleware check: strip phone patterns from chat messages
import re
PHONE_PATTERN = re.compile(r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}')

def sanitize_message(content):
    return PHONE_PATTERN.sub('[Contact via Admin]', content)
```

### 4. WebSocket Chat (Django Channels)
```python
# In chat/consumers.py
class ChatConsumer(WebsocketConsumer):
    # Group by room_id
    # On receive: sanitize → save to DB → broadcast to room
    # Show sender role badge (Client / Advocate / Admin)
    # Admin can join ANY room
```

### 5. Razorpay Integration
```python
# In payments/views.py
def create_razorpay_order(request, booking_id):
    # Create Razorpay order
    # Store razorpay_order_id in Payment model
    # Return order_id to frontend

def razorpay_webhook(request):
    # Verify signature
    # Update Payment status
    # Calculate admin commission (from CommissionConfig)
    # Generate PDF receipt (WeasyPrint)
    # Send confirmation email/notification
```

### 6. PDF Receipt Generation
```python
# Using WeasyPrint
from django.template.loader import render_to_string
from weasyprint import HTML

def generate_receipt_pdf(payment):
    html = render_to_string('payments/receipt.html', {'payment': payment})
    return HTML(string=html).write_pdf()
```

### 7. Registration Forms (3-Step Onboarding for Client)
- **Step 1**: Name, DOB, Gender, Mobile (OTP verify here)
- **Step 2**: Address, State, District, Aadhaar, PAN
- **Step 3**: Issue category, location enable toggle, photo upload
- Use Django `SessionWizardView` or HTMX multi-step

---

## UI/UX DESIGN REQUIREMENTS

### Color Palette (CSS Variables)
```css
:root {
  --primary: #0D7377;      /* Deep Teal */
  --primary-light: #14A085; /* Bright Teal */
  --secondary: #1A3C5E;    /* Navy Blue */
  --accent: #F0A500;       /* Gold accent */
  --bg-main: #F0F4F8;      /* Off-white blue-tinted bg */
  --surface: #FFFFFF;
  --text-primary: #1A2332;
  --text-muted: #6B7C93;
  --success: #27AE60;
  --danger: #E74C3C;
}
```

### Dashboard Layout
- **Top bar**: Logo + notification bell + profile avatar
- **Sidebar** (desktop) / **Bottom nav** (mobile): 5 main icons
- **Main area**: 3x3 grid of big round icon cards with labels
- **Floating AI assistant button**: bottom-right corner (opens helpdesk chat)

### Dashboard Icon Cards (Client)
Build these 9 cards with SVG icons + gradient backgrounds:
1. 📋 Book an Advocate (teal gradient)
2. ⚖️ High Court Advocates (blue gradient)
3. 🏛️ Supreme Court (AOR) (navy gradient)
4. 📁 My Cases (green gradient)
5. 💬 Chat Support (purple gradient)
6. 💳 Payments (amber gradient)
7. ⭐ Feedback (orange gradient)
8. 🗺️ Northeast Law Hub (teal-green gradient)
9. 📞 Contact Admin (red gradient)

### Typography
- Display/Headings: `Playfair Display` (Google Fonts) — premium, legal feel
- Body: `DM Sans` — clean, readable for common people
- Code/IDs: `JetBrains Mono`

### Animations
- Card hover: subtle lift + shadow (CSS transform)
- Page transitions: fade-in (Alpine.js x-transition)
- Loading states: skeleton screens
- Chat messages: slide-in from left/right by sender role

---

## REGISTRATION FORM FIELDS (Implement as Django ModelForms)

### Client Registration Form
```
Personal: full_name, father_or_spouse_name, dob, gender
Contact: mobile (OTP verified), email, permanent_address, state, district
Identity: aadhaar_number, pan_number, voter_id (optional)
Uploads: profile_photo, id_proof, signature
Preferences: issue_category, enable_live_location
```

### Advocate Registration Form
```
Personal: full_name, father_or_spouse_name, dob, gender
Contact: mobile, email, residential_address
Professional: bar_council_state, enrollment_number, enrollment_date, years_of_practice
Practice: practice_type, office_address, court_of_practice (multi-select)
Areas: primary_practice_area, secondary_practice_area
Identity: aadhaar_number (optional), pan_number
Emergency: emergency_contact_name, emergency_contact_relation, emergency_contact_number
Uploads: profile_photo, signature, enrollment_certificate
Fees: consultation_fee, case_fee
AOR: is_aor (checkbox — only if Supreme Court)
```

### Case Form (Admin/Advocate fills)
```
case_title, case_number, case_type, court_name
client (select), advocate (select), opponent_details
filing_date, status, stage, case_summary
```

### Hearing Form
```
case (select), hearing_date, next_hearing_date
what_happened, judge_remarks, status
```

---

## NORTHEAST LAW HUB (Special Feature)

### Page Design
- Hero banner: NE India map illustration + tagline "Know Your Rights"
- 8 category cards (matching model categories above)
- State filter: Assam / Manipur / Meghalaya / Mizoram / Nagaland / Sikkim / Tripura / Arunachal Pradesh
- Article cards: title + state badge + category badge + read time
- Helpline section: emergency contacts in card format

### Content Structure
- Each article: title, state, category, rich content (summaryeditor or django-ckeditor), published date
- Admin can add/edit/delete from `/admin-portal/northeast-hub/`

---

## ADMIN PANEL (Custom, NOT just Django default admin)

Build a custom admin portal at `/admin-portal/` with:

### Dashboard Widgets
- Total clients, advocates, active cases, revenue today
- Pending approvals count (clients + advocates + bookings)
- Recent bookings table
- Revenue chart (last 30 days)

### Clients Management (`/admin-portal/clients/`)
- Table: name, mobile, state, district, registered date, status
- Actions: Approve / Reject / Ban / View Full Profile / Delete
- Search + filter by state, district, issue category

### Advocates Management (`/admin-portal/advocates/`)
- Table: name, enrollment no, court, AOR status, rating, availability
- Actions: Verify / Suspend / Ban / View Profile / Edit
- Filter by: court type, state, AOR, specialization

### Bookings Management (`/admin-portal/bookings/`)
- Table: client name, advocate name, type, date, status
- Actions: Approve / Reject / Replace Advocate / Add Notes
- **Replace Advocate**: dropdown to pick new advocate, notify both parties

### Cases (`/admin-portal/cases/`)
- Full case details editable
- Add admin notes
- Edit status and stage
- View all documents
- Link to chat logs for that booking

### Chat Logs (`/admin-portal/chat-logs/`)
- View any chat room
- Admin can join/message any room
- Flag/report messages

### Payments (`/admin-portal/payments/`)
- All transactions: client, advocate, type, amount, commission, status
- Commission config: set percentage per payment type
- Export to CSV

### Feedback Moderation (`/admin-portal/feedback/`)
- All reviews: client, advocate, rating, review, date
- Actions: Hide / Show / Delete / Approve public reply

---

## SECURITY REQUIREMENTS
- All views: `@login_required` + custom `role_required` decorator
- Advocate views: NEVER include `client.mobile` or `client.email` in context
- Admin views: CSRF protected, rate limited
- File uploads: validate MIME type + size limit (10MB)
- Chat: sanitize phone patterns in real-time
- Razorpay: verify webhook signature before processing
- Django settings: `DEBUG=False` in prod, `ALLOWED_HOSTS` configured, `SECRET_KEY` from env
- HTTPS enforced via `SECURE_SSL_REDIRECT = True` in prod settings

---

## DEPLOYMENT CONFIGURATION

### requirements.txt (core)
```
Django==4.2.*
psycopg2-binary
channels==4.*
channels-redis
celery
redis
razorpay
django-allauth
django-storages
boto3
WeasyPrint
Pillow
python-decouple
gunicorn
whitenoise
django-ckeditor
```

### .env.example
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/legal_portal
REDIS_URL=redis://localhost:6379/0
RAZORPAY_KEY_ID=rzp_live_xxx
RAZORPAY_KEY_SECRET=xxx
AWS_ACCESS_KEY_ID=xxx
AWS_SECRET_ACCESS_KEY=xxx
AWS_STORAGE_BUCKET_NAME=northeast-legal-portal
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=app-password
SMS_API_KEY=your-fast2sms-key
ADMIN_PHONE=+91XXXXXXXXXX
```

### Procfile (Railway/Render)
```
web: gunicorn legal_portal.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A legal_portal worker --loglevel=info
```

### settings/prod.py additions
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
CHANNEL_LAYERS = {'default': {'BACKEND': 'channels_redis.core.RedisChannelLayer', ...}}
```

---

## BUILD ORDER (Follow This Sequence)

1. **Setup**: Django project, PostgreSQL, env config, base template with Tailwind
2. **Accounts app**: CustomUser model, OTP login, role middleware
3. **Client + Advocate models + forms**: all registration forms
4. **Admin panel**: custom views for managing users + approvals
5. **Bookings app**: location matching, booking flow, notifications
6. **Cases app**: case model, hearing model, timeline, documents
7. **Chat app**: Django Channels setup, WebSocket consumer, privacy filter
8. **Payments app**: Razorpay integration, commission calc, PDF receipts
9. **Feedback app**: rating form, moderation
10. **Northeast Hub**: article CRUD, helplines, map
11. **Dashboard UI**: all icon cards, responsive layout
12. **Polish**: animations, loading states, mobile optimization
13. **Security audit**: role checks, phone leak prevention, HTTPS config
14. **Deploy**: Railway or Render with PostgreSQL + Redis add-ons

---

## FINAL NOTES FOR CODER
- Admin has COMPLETE control over everything — no action happens without admin oversight
- Advocates NEVER see client phone numbers or emails — enforce this at view + template level
- All chat is text-only, phone patterns auto-redacted
- The portal must work on mobile (responsive first design)
- Use HTMX for dynamic updates (no full page reloads for booking status, chat, etc.)
- Northeast Law Hub must be SEO-friendly (proper meta tags, slugs)
- Every payment must generate a downloadable PDF receipt
- Build with `django-debug-toolbar` for dev, disable completely in prod
