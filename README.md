# CV Revamping Application

A modern, full-stack application for creating, editing, and managing professional CVs with real-time collaboration features.

## 🚀 Tech Stack

### Frontend
- **Angular 17+** - Modern reactive UI framework
- **Angular Material** - Material Design components
- **RxJS** - Reactive programming
- **NgRx** - State management
- **Tailwind CSS** - Utility-first CSS framework

### Backend
- **Python 3.11+** - Core backend language
- **FastAPI** - Modern, fast web framework
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Database ORM
- **Alembic** - Database migrations
- **Celery** - Background task processing
- **Redis** - Caching and message broker

### Database
- **PostgreSQL** - Primary database
- **Redis** - Caching layer

### DevOps & Tools
- **Docker** - Containerization
- **GitHub Actions** - Continuous integration/deployment
- **Docusaurus** - Documentation site
- **Git** - Version control

## 📁 Project Structure

```
cv-revamp-app/
├── frontend/                 # Angular application
├── backend/                  # FastAPI application
├── docs/                     # Docusaurus documentation
├── docker/                   # Docker configurations
├── scripts/                  # Utility scripts
├── .github/workflows/        # GitHub Actions workflows
└── docker-compose.yml        # Development environment
```

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git

### Development Setup
1. Clone the repository
2. Run `./scripts/setup.sh` for development environment
3. Run `docker-compose up -d` to start all services
4. Access the application at `http://localhost:4200`

## 📚 Documentation
- [API Documentation](http://localhost:8000/docs)
- [Frontend Guide](./docs/frontend.md)
- [Backend Guide](./docs/backend.md)
- [Deployment Guide](./docs/deployment.md)

## 🤝 Contributing
Please read our [Contributing Guidelines](./CONTRIBUTING.md) before submitting pull requests.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
