# Dive - Job Search Application

A modern full-stack job search application with web scraping capabilities, focused on the South African job market.

## 🚀 Features

- **Job Search & Scraping**: Automated job scraping from multiple South African job sites
- **Modern Frontend**: Angular-based responsive web interface
- **RESTful API**: FastAPI backend with comprehensive job management
- **Real-time Updates**: Live job search and filtering
- **Database Storage**: SQLite database for job persistence
- **Material Design**: Clean, modern UI with Angular Material

## 🏗️ Architecture

```
Dive/
├── backend/           # FastAPI backend application
│   ├── app/          # Main application code
│   │   ├── api/      # API endpoints
│   │   ├── core/     # Core configuration
│   │   ├── models/   # Database models
│   │   └── schemas/  # Pydantic schemas
│   ├── scraper/      # Job scraping modules
│   ├── tests/        # Backend tests
│   └── requirements*.txt
├── frontend/         # Angular frontend application
│   ├── src/
│   │   ├── app/      # Angular components & services
│   │   │   ├── components/  # UI components
│   │   │   ├── pages/       # Page components
│   │   │   ├── services/    # Angular services
│   │   │   └── guards/      # Route guards
│   │   └── environments/    # Environment configs
│   └── package.json
├── start-dev.ps1     # Development startup script
├── stop-dev.ps1      # Development stop script
└── cleanup.py        # Project cleanup utility
```

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database
- **Pydantic**: Data validation
- **BeautifulSoup4**: Web scraping
- **Requests**: HTTP client

### Frontend
- **Angular 17**: Frontend framework
- **Angular Material**: UI component library
- **TypeScript**: Programming language
- **RxJS**: Reactive programming
- **SCSS**: Styling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Dive
   ```

2. **Start the development environment**
   ```bash
   # Windows PowerShell
   .\start-dev.ps1
   ```

3. **Access the application**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Stop the development environment**
   ```bash
   .\stop-dev.ps1
   ```

### Manual Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 📊 API Endpoints

### Jobs
- `GET /api/jobs` - Get all jobs with filtering
- `POST /api/jobs/scrape` - Trigger job scraping
- `GET /api/jobs/stats` - Get job statistics
- `GET /api/jobs/{id}` - Get specific job details

### Health
- `GET /health` - Health check endpoint
- `GET /` - API information

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.py` to configure:
- Database settings
- Scraping parameters
- CORS origins
- Debug mode

### Frontend Configuration
Edit `frontend/src/environments/environment.ts` for:
- API base URL
- Feature flags
- Environment-specific settings

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

The application includes Docker configurations for easy deployment:

```bash
# Build and run with Docker Compose
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the codebase structure
- Create an issue for bugs or feature requests

---

**Built with ❤️ for the South African job market**
