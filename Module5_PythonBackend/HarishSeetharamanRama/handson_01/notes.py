# ============================================================
# Hands-On 1 – Web Framework Foundations & Django Project Setup
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

# ============================================================
# TASK 1: Request-Response Cycle
# ============================================================

# STEP 1: Journey of GET /api/courses/ through Django:
#
# Browser sends HTTP GET /api/courses/
#   ↓
# Django WSGI/ASGI server receives the request
#   ↓
# Middleware stack (request phase) — SecurityMiddleware, SessionMiddleware etc.
#   ↓
# URL Router (urls.py) — matches /api/courses/ to CourseListView
#   ↓
# View (views.py) — CourseListView.get() is called
#   ↓
# Model (models.py) — Course.objects.all() queries the database
#   ↓
# Database returns queryset
#   ↓
# View serializes data to JSON
#   ↓
# Middleware stack (response phase)
#   ↓
# HTTP Response sent back to browser with JSON data

# STEP 2: Where middleware sits:
# Middleware sits BETWEEN the URL router and the view (both for request AND response)
# It wraps every request/response like an onion — each layer processes before passing on
#
# Two built-in Django middleware classes:
#
# 1. SecurityMiddleware (django.middleware.security.SecurityMiddleware)
#    → Adds security headers like HTTPS redirect, HSTS, XSS protection headers
#    → Protects against common web vulnerabilities
#
# 2. SessionMiddleware (django.contrib.sessions.middleware.SessionMiddleware)
#    → Manages user sessions using cookies
#    → Enables request.session dictionary to store per-user data across requests

# STEP 3: WSGI vs ASGI
#
# WSGI (Web Server Gateway Interface):
#   - Synchronous interface — handles one request at a time per thread
#   - Django uses WSGI by default (wsgi.py)
#   - Good for traditional web apps and REST APIs
#   - Served by gunicorn, uWSGI in production
#
# ASGI (Asynchronous Server Gateway Interface):
#   - Asynchronous interface — handles multiple requests concurrently
#   - Django also supports ASGI (asgi.py)
#   - Switch to ASGI when you need: WebSockets, long-polling,
#     async views, high-concurrency real-time features
#   - Served by uvicorn, daphne in production
#
# Django uses WSGI by default.
# Switch to ASGI when building real-time features like chat apps or live notifications.

# STEP 4: MVC vs Django's MVT
#
# MVC Pattern:
#   Model      → Data & business logic
#   View       → What the user sees (UI/template)
#   Controller → Handles user input, calls model, returns view
#
# Django's MVT Pattern:
#   Model    → Same as MVC Model (models.py — database tables & ORM)
#   View     → Acts like MVC Controller (views.py — handles request, calls model)
#   Template → Acts like MVC View (HTML templates — what user sees)
#
# Key difference: Django's "View" = MVC's "Controller"
#                 Django's "Template" = MVC's "View"
#                 Django's URL router handles the routing (part of Controller in MVC)


# ============================================================
# TASK 2: Django Project Setup (run these commands in terminal)
# ============================================================

# pip install django
# django-admin startproject coursemanager
# cd coursemanager
# python manage.py startapp courses

# FILE STRUCTURE AFTER SETUP:
# coursemanager/                  ← Project root
# ├── manage.py                   ← CLI tool to run commands
# ├── coursemanager/              ← Project config package
# │   ├── settings.py             ← All project settings (DB, apps, middleware)
# │   ├── urls.py                 ← Root URL configuration
# │   ├── wsgi.py                 ← WSGI entry point for deployment
# │   └── asgi.py                 ← ASGI entry point for async deployment
# └── courses/                    ← Django app (reusable module)
#     ├── models.py               ← Database models
#     ├── views.py                ← Request handlers
#     ├── urls.py                 ← App-level URL config
#     ├── admin.py                ← Admin interface registration
#     └── apps.py                 ← App configuration

# DIFFERENCE between Django PROJECT and Django APP:
# Project = overall configuration (settings, root URLs, WSGI) — one per deployment
# App     = self-contained module with models/views/URLs — one project can have MANY apps
# Example: 'courses', 'students', 'auth' can all be separate apps in one project

# VERIFICATION: After setup, browser should show:
# http://127.0.0.1:8000/api/hello/ → 'Course Management API is running'