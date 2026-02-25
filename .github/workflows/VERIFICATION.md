# CI Workflow Verification Guide

## How to Verify Your CI Workflow

### Method 1: Validate YAML Syntax

```bash
# Using Python
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"

# Should output nothing if valid, or show syntax errors
```

### Method 2: Install and Use actionlint

```bash
# Install actionlint (GitHub Actions linter)
brew install actionlint

# Validate workflow
actionlint .github/workflows/ci.yml

# Should show no errors if valid
```

### Method 3: Test Locally (Simulate CI)

Run the same commands that CI will run:

```bash
cd backend

# 1. Check dependencies are installed
pip list | grep -E "pytest|flake8|pytest-cov"

# 2. Run linting (critical errors only)
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics

# 3. Run tests with coverage
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80

# All should pass with exit code 0
```

### Method 4: Push to GitHub and Check Actions Tab

The most reliable way:

1. Commit your changes:
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "Add CI workflow"
   ```

2. Push to GitHub:
   ```bash
   git push origin main
   ```

3. Check the Actions tab on GitHub:
   - Go to your repository on GitHub
   - Click "Actions" tab
   - You should see your workflow running
   - Green checkmark = success ✅
   - Red X = failure ❌

### Method 5: Use GitHub CLI

```bash
# Install GitHub CLI
brew install gh

# Authenticate
gh auth login

# View workflow runs
gh run list

# View specific run details
gh run view <run-id>
```

## Current Verification Status

### ✅ YAML Syntax: Valid
```
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"
# Output: No errors
```

### ✅ Local Test Simulation: Passed

**Linting:**
```bash
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
# Output: 0 errors
```

**Tests:**
```bash
pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80
# Output: 177 passed, 87% coverage (exceeds 80% requirement)
```

**Python Version:**
```bash
python --version
# Output: Python 3.11.11 (matches CI configuration)
```

## What the CI Workflow Does

1. **Triggers**: Runs on push/PR to main, master, or develop branches
2. **Environment**: Ubuntu latest with Python 3.11
3. **Steps**:
   - Checkout code
   - Set up Python 3.11
   - Cache pip dependencies (faster builds)
   - Install dependencies from requirements.txt
   - Run flake8 linting (critical errors fail build)
   - Run pytest with coverage
   - Fail if coverage < 80%
   - Upload coverage to Codecov (optional)

## Troubleshooting

### Issue: "YAML syntax error"
**Solution**: Check indentation (use 2 spaces, not tabs)

### Issue: "Tests fail in CI but pass locally"
**Solution**:
- Check Python version matches (3.11)
- Ensure all dependencies in requirements.txt
- Check for environment-specific code

### Issue: "Coverage fails in CI"
**Solution**:
- Run locally: `pytest tests/ --cov=app --cov-fail-under=80`
- Ensure coverage is actually ≥80%

### Issue: "Flake8 fails in CI"
**Solution**:
- Run locally: `flake8 app/`
- Fix any E9, F63, F7, F82 errors
- Or run pre-commit: `pre-commit run --all-files`

## Best Practices

1. **Test locally before pushing** - Run the same commands CI will run
2. **Use pre-commit hooks** - Catch issues before commit
3. **Check Actions tab regularly** - Monitor CI health
4. **Fix failures quickly** - Don't let broken builds accumulate
5. **Keep dependencies updated** - Update requirements.txt when adding packages

## Quick Verification Checklist

Before pushing:
- [ ] YAML syntax is valid
- [ ] Tests pass locally
- [ ] Coverage ≥ 80%
- [ ] No critical flake8 errors
- [ ] All dependencies in requirements.txt
- [ ] Python version matches CI (3.11)

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [actionlint](https://github.com/rhysd/actionlint)
- [pytest Documentation](https://docs.pytest.org/)
- [flake8 Documentation](https://flake8.pycqa.org/)
