# NorthLex — Northeast Legal Portal

## Stack
Django 4.2, PostgreSQL, Redis, Django Channels,
Razorpay, WeasyPrint, HTMX, TailwindCSS (CDN)

## Apps build order
- [ ] accounts (OTP login, roles)
- [ ] clients (profile, onboarding)
- [ ] advocates (profile, HC/SC AOR)
- [ ] bookings (location-based matching)
- [ ] cases (status, hearings, timeline)
- [ ] chat (WebSocket, privacy filter)
- [ ] payments (Razorpay, PDF receipt)
- [ ] feedback (ratings, moderation)
- [ ] northeast_hub (articles, helplines)
- [ ] admin_panel (custom dashboard)

## Rules
- Django templates + HTMX only, no React
- Advocates NEVER see client mobile/email
- Filter phone numbers from all chat messages
- Commit after every working app
