# GitHub Actions CI/CD

This directory contains GitHub Actions workflows for continuous integration and deployment.

## Workflows

### CI Workflow (`ci.yml`)

Runs on every push and pull request to main/master/develop branches.

**Steps:**
1. Checkout code
2. Set up Python 3.11
3. Cache pip dependencies for faster builds
4. Install dependencies from `backend/requirements.txt`
5. Run flake8 linting (critical errors only)
6. Run pytest with coverage
7. Fail if coverage < 80%
8. Upload coverage to Codecov (optional)

**Local Testing:**

To test the CI workflow locally before pushing:

```bash
cd backend

# Install dependencies
pip install -r requirements.txt
pip install flake8

# Run linting (critical errors)
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics

# Run linting (all warnings)
flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run tests with coverage
pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=80
```

**Coverage Requirements:**
- Minimum: 80%
- Current: 86%

**Linting Rules:**
- Critical errors (E9, F63, F7, F82) will fail the build
- Style warnings are reported but don't fail the build
- Max line length: 127 characters
- Max complexity: 10

## Configuration Files

- `.flake8` - Flake8 configuration in backend directory
- `requirements.txt` - Python dependencies

## Badge

Add this to your README.md to show CI status:

```markdown
![CI](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/badge.svg)
```
