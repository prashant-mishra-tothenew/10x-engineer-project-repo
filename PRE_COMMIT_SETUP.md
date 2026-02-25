# Pre-commit Hooks Setup Guide

This guide explains how to set up and use pre-commit hooks to automatically check code quality before every commit.

## What are Pre-commit Hooks?

- Automatically runs checks before `git commit` succeeds
- Prevents bad code from being committed

## Installation

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This installs:
- `pre-commit` - The hook framework
- `black` - Code formatter (like Prettier)
- `isort` - Import sorter
- `flake8` - Linter (like ESLint)
- `bandit` - Security checker

### Step 2: Install Git Hooks

```bash
# From project root
pre-commit install
```

This creates a `.git/hooks/pre-commit` file that runs automatically.

### Step 3: (Optional) Run on All Files

```bash
# Run hooks on all files (not just staged)
pre-commit run --all-files
```

## What Gets Checked?

### 1. General File Checks
- ✅ Remove trailing whitespace
- ✅ Ensure files end with newline
- ✅ Check YAML syntax
- ✅ Check JSON syntax
- ✅ Detect large files (>1MB)
- ✅ Detect merge conflicts
- ✅ Detect private keys

### 2. Python Code Formatting (Black)
- ✅ Auto-format code to consistent style
- ✅ Line length: 127 characters
- ✅ Consistent code formatting across the project

### 3. Import Sorting (isort)
- ✅ Sort imports alphabetically
- ✅ Group imports (stdlib, third-party, local)
- ✅ Compatible with Black

### 4. Linting (Flake8)
- ✅ Check code style (PEP 8)
- ✅ Find syntax errors
- ✅ Detect unused imports
- ✅ Enforce Python style guidelines (PEP 8)

### 5. Security Checks (Bandit)
- ✅ Detect security issues
- ✅ Find hardcoded passwords
- ✅ Check for SQL injection risks
- ✅ Identify security vulnerabilities in code

### 6. Dockerfile Linting (Hadolint)
- ✅ Check Dockerfile best practices
- ✅ Detect security issues
- ✅ Optimize image size

## Usage

### Normal Workflow

```bash
# Make changes to code
vim backend/app/api.py

# Stage changes
git add backend/app/api.py

# Commit (hooks run automatically)
git commit -m "Add new feature"
```

**What happens:**
1. Pre-commit runs all configured hooks
2. If any hook fails, commit is aborted
3. Fix the issues and try again
4. Some hooks auto-fix issues (black, isort)

### Example Output

```bash
$ git commit -m "Add feature"

Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check Yaml...............................................................Passed
Check for added large files..............................................Passed
Check JSON...............................................................Passed
Check Toml...............................................................Passed
Check for merge conflicts................................................Passed
Detect Private Key.......................................................Passed
black....................................................................Passed
isort....................................................................Passed
flake8...................................................................Passed
bandit...................................................................Passed
hadolint-docker..........................................................Passed

[main abc1234] Add feature
 1 file changed, 10 insertions(+)
```

### If a Hook Fails

```bash
$ git commit -m "Add feature"

black....................................................................Failed
- hook id: black
- files were modified by this hook

reformatted backend/app/api.py
All done! ✨ 🍰 ✨
1 file reformatted.
```

**What to do:**
1. The hook auto-fixed the file
2. Review the changes: `git diff`
3. Stage the fixes: `git add backend/app/api.py`
4. Commit again: `git commit -m "Add feature"`

## Skipping Hooks (Not Recommended)

```bash
# Skip all hooks (emergency only!)
git commit -m "Quick fix" --no-verify

# Skip specific hook
SKIP=flake8 git commit -m "WIP: ignore linting"
```

⚠️ **Warning**: Only skip hooks when absolutely necessary!

## Configuration Files

### `.pre-commit-config.yaml`
Main configuration file defining which hooks to run.

### `pyproject.toml`
Configuration for Black, isort, Bandit, and pytest.

### `backend/.flake8`
Configuration for Flake8 linting rules.

## Updating Hooks

```bash
# Update to latest versions
pre-commit autoupdate

# Re-install hooks after update
pre-commit install
```

## Troubleshooting

### Hook Installation Failed

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install
```

### Hook Takes Too Long

```bash
# Run only on changed files (default)
git commit -m "message"

# Skip slow hooks temporarily
SKIP=bandit git commit -m "message"
```

### Black and Flake8 Conflict

Our configuration is already set up to avoid conflicts:
- Black line length: 127
- Flake8 line length: 127
- Flake8 ignores Black-incompatible rules

### Pre-commit Not Found

```bash
# Install pre-commit
pip install pre-commit

# Or reinstall all dependencies
cd backend
pip install -r requirements.txt
```

## CI/CD Integration

Pre-commit hooks also run in GitHub Actions CI:

```yaml
# .github/workflows/ci.yml
- name: Run pre-commit
  run: pre-commit run --all-files
```

This ensures code quality even if someone skips local hooks.

## Pre-commit Tools Overview

| Tool | Purpose |
|------|---------|
| pre-commit | Hook management framework |
| black | Code formatter |
| isort | Import sorter |
| flake8 | Linter |
| bandit | Security checker |

## Best Practices

✅ **DO:**
- Run `pre-commit run --all-files` before pushing
- Fix issues immediately
- Keep hooks updated
- Review auto-fixes before committing

❌ **DON'T:**
- Skip hooks regularly with `--no-verify`
- Ignore hook failures
- Commit without reviewing auto-fixes
- Disable hooks permanently

## Benefits

1. **Consistent Code Style** - Everyone's code looks the same
2. **Catch Bugs Early** - Find issues before code review
3. **Save Time** - Auto-fix formatting issues
4. **Better Code Quality** - Enforce best practices
5. **Security** - Detect vulnerabilities early

## Additional Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
