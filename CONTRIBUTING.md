# Contributing to CV Revamping Application

Thank you for your interest in contributing to the CV Revamping Application! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/cv-revamp-app.git
   cd cv-revamp-app
   ```

### 2. Set Up Development Environment

```bash
# Run the setup script
./scripts/setup.sh

# Start the development environment
docker-compose up -d
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 4. Make Your Changes

- Follow the coding standards (see below)
- Write tests for new features
- Update documentation as needed
- Keep commits small and focused

### 5. Test Your Changes

```bash
# Frontend tests
cd frontend && npm test

# Backend tests
cd backend && pytest

# Linting
cd frontend && npm run lint
cd backend && flake8 app/ && black app/
```

### 6. Commit Your Changes

```bash
git add .
git commit -m "feat: add new CV template feature"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `style:` for formatting changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a pull request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots (if UI changes)

## 📋 Coding Standards

### Frontend (Angular)

- Use TypeScript strict mode
- Follow Angular style guide
- Use Angular Material components
- Implement proper error handling
- Write unit tests for components and services
- Use RxJS for reactive programming

### Backend (FastAPI)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Implement proper error handling
- Write unit tests with pytest
- Use Pydantic for data validation

### General

- Write clear, readable code
- Add comments for complex logic
- Use meaningful variable and function names
- Keep functions small and focused
- Follow DRY (Don't Repeat Yourself) principle

## 🧪 Testing

### Frontend Testing

```bash
cd frontend

# Unit tests
npm test

# E2E tests
npm run e2e

# Coverage report
npm run test:ci
```

### Backend Testing

```bash
cd backend

# Unit tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py
```

## 📚 Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation
- Create/update user guides

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details**
   - OS and version
   - Node.js version
   - Python version
   - Docker version

2. **Steps to reproduce**
   - Clear, step-by-step instructions
   - Expected vs actual behavior

3. **Additional information**
   - Error messages/logs
   - Screenshots (if applicable)
   - Browser console errors (for frontend issues)

## 💡 Feature Requests

When suggesting features:

1. **Describe the problem**
   - What issue does this solve?
   - Who would benefit from this?

2. **Propose a solution**
   - How should this work?
   - Any specific requirements?

3. **Consider alternatives**
   - Are there existing solutions?
   - What are the trade-offs?

## 🔄 Pull Request Process

1. **Code Review**
   - All PRs require review
   - Address feedback promptly
   - Keep discussions constructive

2. **CI/CD Checks**
   - All tests must pass
   - Code coverage should not decrease
   - Linting must pass

3. **Merge Strategy**
   - Squash and merge for feature branches
   - Rebase and merge for hotfixes
   - Delete feature branches after merge

## 🏷️ Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature or request
- `documentation`: Improvements to documentation
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## 📞 Getting Help

- Check existing issues and PRs
- Join our discussions
- Ask questions in issues
- Review documentation

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the CV Revamping Application! 🚀 