# HeritageAI Architecture

## Overview

HeritageAI is a production-grade AI-powered Heritage Preservation Platform built as a Progressive Web Application (PWA).

The project follows a modular monorepo architecture to ensure scalability, maintainability, and independent deployment of services.

---

# High-Level Architecture

Users
↓
Next.js PWA
↓
REST API (FastAPI)
↓
Application Services
↓
PostgreSQL + AI Services + Cloudinary

---

# Repository Structure

heritageai/
├── apps/
│   ├── web/
│   └── api/
│
├── packages/
│   ├── ui/
│   ├── config/
│   ├── types/
│   └── utils/
│
├── database/
├── ai/
├── docker/
├── docs/
├── scripts/
└── .github/

---

# Frontend

- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- TanStack Query

---

# Backend

- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication
- Pydantic Validation

---

# Database

- PostgreSQL
- UUID Primary Keys
- Foreign Keys
- Indexed Columns
- Alembic Migrations

---

# AI Layer

- Gemini API
- EasyOCR
- OpenCV
- YOLOv8
- Sentence Transformers
- FAISS
- Real-ESRGAN

AI integrations will be accessed through service interfaces to allow provider replacement without affecting business logic.

---

# Deployment

Frontend:
- Vercel

Backend:
- Render

Database:
- Neon PostgreSQL

Storage:
- Cloudinary

---

# Security

- JWT Authentication
- Password Hashing
- RBAC
- Input Validation
- Rate Limiting
- Environment Variables
- HTTPS

---

# Development Principles

- Mobile-first
- PWA-first
- Accessibility
- Clean Architecture
- Modular Design
- API-first
- Testable Code
- Production-ready Quality