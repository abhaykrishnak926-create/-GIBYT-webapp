# GIBYT — Phase 3 (Auth + PostgreSQL)

This adds a real Flask backend on top of the existing static site: user
accounts, PostgreSQL storage, hashed passwords, and working `/login` and
`/signup` pages. The public marketing pages (Home, About, Our Work,
Products, Careers, Contact) are unchanged in content — they're now served
by Flask instead of being flat files, so the nav links and asset paths use
`url_for(...)`.

## What's in this folder

```
gibyt/
├── app.py                  # Flask app factory
├── config.py                # Reads SECRET_KEY / DATABASE_URL from .env
├── extensions.py            # Shared db / bcrypt / login_manager / csrf / migrate
├── requirements.txt
├── .env.example             # Copy to .env and fill in
├── models/
│   └── user.py               # User table: id, name, email, password_hash, created_at
├── forms/
│   └── auth_forms.py         # SignupForm / LoginForm (Flask-WTF, includes CSRF)
├── routes/
│   ├── main.py                # Public pages + protected /dashboard
│   └── auth.py                 # /signup, /login, /logout, /forgot-password
├── templates/                # All existing pages + new login.html, signup.html,
│                              # dashboard.html, forgot_password.html
└── static/
    ├── css/style.css          # Your existing styles + small auth/flash additions
    ├── js/script.js           # Unchanged
    └── images/                # Put logo2.png here (not included in this handoff)
```

**You still need to add `static/images/logo2.png`** — it wasn't part of
this handoff, so copy your existing logo file into that folder.

## 1. Install dependencies

```bash
cd gibyt
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Set up PostgreSQL

Create a database and a user for it, e.g.:

```sql
CREATE DATABASE gibyt;
CREATE USER gibyt_user WITH PASSWORD 'gibyt_password';
GRANT ALL PRIVILEGES ON DATABASE gibyt TO gibyt_user;
```

(Or use a hosted Postgres instance — Render, Supabase, Railway, etc. all
give you a connection string you can drop straight into `DATABASE_URL`.)

## 3. Configure environment variables

```bash
cp .env.example .env
```

Then edit `.env`:
- `SECRET_KEY` — generate one with `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_URL` — your Postgres connection string, e.g.
  `postgresql://gibyt_user:gibyt_password@localhost:5432/gibyt`

## 4. Create the database tables

```bash
flask --app app db init
flask --app app db migrate -m "create users table"
flask --app app db upgrade
```

This uses Flask-Migrate so future schema changes (Phase 4's dashboard
fields, etc.) are tracked instead of hand-editing the database.

## 5. Run it

```bash
flask --app app run --debug
```

Visit `http://127.0.0.1:5000`. Try:
- `/signup` — create an account (name, email, password, confirm password)
- `/login` — log back in, with "remember me"
- `/dashboard` — protected route, redirects to `/login` if you're not
  signed in, then sends you back to `/dashboard` after login
- `/logout`

## Security notes

- Passwords are hashed with bcrypt (`Flask-Bcrypt`) — never stored in
  plain text.
- All forms use Flask-WTF, which gives CSRF protection automatically.
- Duplicate signups are blocked by a unique constraint + an explicit check
  on `email`.
- Cookies are marked `Secure` automatically when `FLASK_ENV=production`.

## What's intentionally NOT done here (by design, per the project's "be honest" rule)

- **Forgot password** — the link exists (`/forgot-password`) but it's an
  honest "coming soon" placeholder, not a fake flow. Real password reset
  needs an email-sending service (e.g. SendGrid, SES, Postmark) wired in,
  which wasn't part of this handoff.
- **Dashboard content** — `/dashboard` is a minimal placeholder that
  confirms the login flow works end-to-end. The real dashboard (profile,
  products, account settings) is Phase 4.
- **Contact form backend** — still front-end only, as before. Wiring it to
  actually send messages is a separate, small addition whenever you're
  ready — happy to do that next.
- **Rate limiting / account lockout on login** — worth adding before a
  public launch (Phase 5 hardening), not included yet.

## Suggested next steps

1. Drop your real `logo2.png` into `static/images/`.
2. Run through steps 1–5 above locally to confirm signup/login/logout work.
3. Then decide: Phase 4 (real dashboard) or finish wiring the contact form.
