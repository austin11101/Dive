# Changelog

## [2025-07-29] - Bootstrap Migration & Login Fix

### 🎉 Major Changes
- **Complete Tailwind CSS to Bootstrap Migration**: Replaced Tailwind CSS with Bootstrap for better compatibility and easier maintenance
- **Fixed Login Authentication Issues**: Resolved backend database connection problems and CORS issues

### 🔧 Backend Changes
- **Database Configuration**: Updated to use SQLite for local development instead of PostgreSQL
- **Environment Settings**: Disabled `.env` file loading for local development to use hardcoded settings
- **CORS Configuration**: Updated `ALLOWED_HOSTS` to include all necessary frontend ports
- **SQLite Support**: Added proper SQLite connection configuration with thread safety
- **Redis Handling**: Made Redis connection optional for local development

### 🎨 Frontend Changes
- **Bootstrap Integration**: 
  - Installed Bootstrap CSS
  - Updated `angular.json` to include Bootstrap styles
  - Updated `styles.scss` to import Bootstrap
- **Component Migration**: Migrated all major components to use Bootstrap classes:
  - Login page
  - Signup page
  - Landing page
  - Dashboard
- **Responsive Design**: Improved responsive layout using Bootstrap grid system
- **UI Improvements**: Enhanced visual consistency and modern styling

### 🐛 Bug Fixes
- **Login Authentication**: Fixed "invalid credentials" error by resolving database connection issues
- **Node.js Compatibility**: Updated Node.js version to v20.19.0 for Angular compatibility
- **Build Issues**: Resolved Angular CLI prompts and cache permission issues

### 🧹 Code Cleanup
- **Removed Temporary Files**: Cleaned up test files and temporary scripts
- **Cache Cleanup**: Removed Python cache files and build artifacts
- **Dependency Management**: Updated package dependencies and lock files

### 📦 Dependencies Updated
- **Frontend**: 
  - Added Bootstrap CSS
  - Removed Tailwind CSS packages
  - Updated Angular Material (kept existing)
- **Backend**: 
  - SQLite support for local development
  - Updated configuration for local environment

### 🚀 Deployment Notes
- **Local Development**: Both frontend and backend now work seamlessly for local development
- **Database**: Uses SQLite file (`cv_database.db`) for local development
- **Ports**: 
  - Frontend: `http://localhost:4200`
  - Backend: `http://localhost:8000`

### ✅ Testing
- **Login Functionality**: Verified working with test credentials
- **User Registration**: Confirmed working properly
- **API Endpoints**: All authentication endpoints tested and working
- **Frontend-Backend Communication**: CORS issues resolved

### 🔑 Test Credentials
```
Email: test@example.com
Password: testpassword123
```

### 📝 Next Steps
- Test login functionality in the Angular application
- Create additional user accounts through signup
- Verify all dashboard functionality works correctly
- Consider adding more Bootstrap components as needed 