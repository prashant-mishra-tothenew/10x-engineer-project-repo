# PromptLab Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Option 1: Docker (Recommended)

```bash
# Start the application
docker-compose up

# API available at: http://localhost:8000
# Docs available at: http://localhost:8000/docs
```

### Option 2: Local Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run server
python main.py

# API available at: http://localhost:8000
```

## 📝 Common Commands

### Development
```bash
make up          # Start with Docker
make logs        # View logs
make test        # Run tests
make shell       # Open shell in container
make down        # Stop containers
```

### Testing
```bash
cd backend
pytest tests/ -v                    # Run all tests
pytest tests/ --cov=app            # With coverage
pytest tests/test_tags.py -v      # Specific file
```

### Code Quality
```bash
cd backend
flake8 app/                        # Lint code
black app/                         # Format code
pre-commit run --all-files         # Run all checks
```

### Git Workflow
```bash
git add .
git commit -m "message"            # Pre-commit hooks run automatically
git push
```

## 📚 Key Documentation

- `README.md` - Project overview
- `DOCKER.md` - Docker setup and commands
- `PRE_COMMIT_SETUP.md` - Pre-commit hooks guide
- `REFACTORING.md` - Code quality improvements
- `WEEK3_COMPLETION.md` - Week 3 summary

## 🔗 Important URLs

- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## 📊 Project Status

- ✅ 177 tests passing
- ✅ 86% code coverage
- ✅ CI/CD configured
- ✅ Docker ready
- ✅ Pre-commit hooks active
- ✅ Tagging system complete

## 🎯 Week 3 Achievements

1. Comprehensive test suite (80%+ coverage)
2. Tagging system with TDD (40 new tests)
3. GitHub Actions CI/CD
4. Docker configuration
5. Code refactoring
6. Pre-commit hooks (bonus)

## 🆘 Need Help?

- Check `docs/` folder for detailed guides
- Run `make help` for Docker commands
- See `PRE_COMMIT_SETUP.md` for hook issues
- Review test files in `backend/tests/` for examples
