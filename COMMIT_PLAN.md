# Week 3 Commit Plan

## Recommended Commit Strategy

Organize commits by feature/task for clear history and easy review.

---

## Commit 1: Add comprehensive test suite specification

**Files:**
```bash
git add .kiro/specs/comprehensive-test-suite/
```

**Commit message:**
```bash
git commit -m "docs: add comprehensive test suite specification

- Add requirements.md with 80%+ coverage goal
- Add design.md with testing strategy
- Add tasks.md with 17 implementation tasks
- Define 33 correctness properties for property-based testing

Task: 3.1 - Write Comprehensive Test Suite Spec"
```

---

## Commit 2: Implement comprehensive test suite

**Files:**
```bash
git add backend/tests/test_fixtures.py
git add backend/tests/test_models.py
git add backend/tests/test_storage.py
git add backend/tests/test_utils.py
git add backend/tests/test_api.py
git add backend/tests/conftest.py
```

**Commit message:**
```bash
git commit -m "test: implement comprehensive test suite with 87% coverage

- Add 137 tests across 5 test files
- Achieve 87% total coverage (99.5% excluding unused files)
- Add fixtures for reusable test data
- Test all API endpoints, models, storage, and utils
- All 177 tests passing

Coverage breakdown:
- api.py: 100%
- models.py: 100%
- storage.py: 98%
- utils.py: 100%

Task: 3.1 - Write Comprehensive Test Suite"
```

---

## Commit 3: Implement tagging system using TDD

**Files:**
```bash
git add backend/app/models.py
git add backend/app/storage.py
git add backend/app/api.py
git add backend/app/utils.py
git add backend/tests/test_tags.py
```

**Commit message:**
```bash
git commit -m "feat: implement tagging system using TDD approach

- Add Tag model with validation
- Add tag storage operations (create, get, list)
- Add tag API endpoints (POST /tags, GET /tags, GET /tags/{id})
- Add tags field to Prompt model
- Add tag filtering (GET /prompts?tags=python,ai)
- Add PUT /prompts/{id}/tags endpoint

Followed strict TDD (RED-GREEN-REFACTOR):
- 6 TDD cycles completed
- 40 new tests (all passing)
- Total: 177 tests passing

Task: 3.2 - Implement Feature Using TDD"
```

---

## Commit 4: Set up GitHub Actions CI/CD pipeline

**Files:**
```bash
git add .github/workflows/ci.yml
git add .github/workflows/README.md
git add .github/workflows/VERIFICATION.md
git add backend/.flake8
git add backend/requirements.txt
```

**Commit message:**
```bash
git commit -m "ci: add GitHub Actions CI/CD pipeline

- Add CI workflow for automated testing
- Trigger on push/PR to main/master/develop
- Python 3.11 environment with dependency caching
- Run flake8 linting (critical errors fail build)
- Run pytest with coverage reporting
- Fail if coverage < 80%
- Add Codecov integration (optional)
- Add flake8 configuration
- Add verification documentation

Task: 3.3 - Set Up GitHub Actions CI"
```

---

## Commit 5: Add Docker configuration

**Files:**
```bash
git add backend/Dockerfile
git add backend/Dockerfile.dev
git add backend/.dockerignore
git add docker-compose.yml
git add docker-compose.prod.yml
git add Makefile
git add .env.example
git add DOCKER.md
```

**Commit message:**
```bash
git commit -m "docker: add containerization configuration

- Add production Dockerfile with optimized image
- Add development Dockerfile with hot reload
- Add docker-compose.yml for development
- Add docker-compose.prod.yml with resource limits
- Add Makefile for convenient commands
- Add .env.example for environment variables
- Add comprehensive Docker documentation
- Add .dockerignore to exclude unnecessary files

Features:
- Hot reload in development
- Health checks
- Volume mounts for live updates
- Optimized image size

Task: 3.4 - Create Docker Configuration"
```

---

## Commit 6: Refactor code to eliminate code smells

**Files:**
```bash
git add backend/app/helpers.py
git add backend/app/api.py
git add REFACTORING.md
```

**Commit message:**
```bash
git commit -m "refactor: eliminate DRY violations and improve code quality

- Create helpers.py with reusable functions
- Add create_prompt_copy() to reduce duplication
- Add nullify_collection_for_prompts() extracted from delete_collection
- Refactor 3 functions in api.py to use helpers
- Reduce code duplication by ~60 lines
- All functions now < 20 lines
- Maintain 87% coverage with all 177 tests passing

Task: 3.5 - Refactor Code Smells"
```

---

## Commit 7: Add pre-commit hooks (bonus)

**Files:**
```bash
git add .pre-commit-config.yaml
git add pyproject.toml
git add PRE_COMMIT_SETUP.md
git add backend/requirements.txt
```

**Commit message:**
```bash
git commit -m "chore: add pre-commit hooks for code quality (bonus)

- Configure 9 automated checks
- Add Black (code formatter)
- Add isort (import sorter)
- Add Flake8 (linter)
- Add Bandit (security checker)
- Add Hadolint (Dockerfile linter)
- Add trailing whitespace/EOF fixers
- Add YAML/JSON validators
- Add pyproject.toml for tool configuration
- Add comprehensive setup documentation

Bonus Task: Pre-commit Hooks"
```

---

## Commit 8: Add mutation testing setup (bonus)

**Files:**
```bash
git add backend/setup.cfg
git add backend/.mutmut-config
git add pyproject.toml
git add MUTATION_TESTING.md
git add ADVANCED_TESTING.md
git add MUTMUT_QUICKSTART.md
git add backend/requirements.txt
```

**Commit message:**
```bash
git commit -m "test: add mutation testing configuration (bonus)

- Install and configure mutmut
- Add setup.cfg with mutmut configuration
- Add pyproject.toml mutation testing config
- Create comprehensive mutation testing guide
- Create advanced testing strategies document
- Create quick start tutorial
- Document pytest fixture limitations

Bonus Task: Mutation Testing"
```

---

## Commit 9: Add project documentation

**Files:**
```bash
git add WEEK3_COMPLETION.md
git add QUICK_START.md
git add .github/copilot-instructions.md
```

**Commit message:**
```bash
git commit -m "docs: add Week 3 completion summary and quick start guide

- Add comprehensive Week 3 completion summary
- Document all tasks and achievements
- Add quick start guide for new developers
- Update copilot instructions
- Document final metrics (177 tests, 87% coverage)

Week 3 Complete: All tasks + 2 bonus tasks"
```

---

## Commit 10: Add submission script and cleanup

**Files:**
```bash
git add SUBMIT.sh
git add coverage.json
```

**Commit message:**
```bash
git commit -m "chore: add submission script and coverage report

- Add SUBMIT.sh for easy submission
- Add coverage.json for CI integration
- Ready for Week 3 submission"
```

---

## Quick Commit Script

Save this as `commit-week3.sh`:

```bash
#!/bin/bash

# Commit 1: Specification
git add .kiro/specs/comprehensive-test-suite/
git commit -m "docs: add comprehensive test suite specification

- Add requirements.md with 80%+ coverage goal
- Add design.md with testing strategy
- Add tasks.md with 17 implementation tasks
- Define 33 correctness properties for property-based testing

Task: 3.1 - Write Comprehensive Test Suite Spec"

# Commit 2: Tests
git add backend/tests/test_fixtures.py backend/tests/test_models.py backend/tests/test_storage.py backend/tests/test_utils.py backend/tests/test_api.py backend/tests/conftest.py
git commit -m "test: implement comprehensive test suite with 87% coverage

- Add 137 tests across 5 test files
- Achieve 87% total coverage (99.5% excluding unused files)
- Add fixtures for reusable test data
- Test all API endpoints, models, storage, and utils
- All 177 tests passing

Coverage breakdown:
- api.py: 100%
- models.py: 100%
- storage.py: 98%
- utils.py: 100%

Task: 3.1 - Write Comprehensive Test Suite"

# Commit 3: Tagging
git add backend/app/models.py backend/app/storage.py backend/app/api.py backend/app/utils.py backend/tests/test_tags.py
git commit -m "feat: implement tagging system using TDD approach

- Add Tag model with validation
- Add tag storage operations (create, get, list)
- Add tag API endpoints (POST /tags, GET /tags, GET /tags/{id})
- Add tags field to Prompt model
- Add tag filtering (GET /prompts?tags=python,ai)
- Add PUT /prompts/{id}/tags endpoint

Followed strict TDD (RED-GREEN-REFACTOR):
- 6 TDD cycles completed
- 40 new tests (all passing)
- Total: 177 tests passing

Task: 3.2 - Implement Feature Using TDD"

# Commit 4: CI/CD
git add .github/workflows/ backend/.flake8
git commit -m "ci: add GitHub Actions CI/CD pipeline

- Add CI workflow for automated testing
- Trigger on push/PR to main/master/develop
- Python 3.11 environment with dependency caching
- Run flake8 linting (critical errors fail build)
- Run pytest with coverage reporting
- Fail if coverage < 80%
- Add Codecov integration (optional)
- Add flake8 configuration
- Add verification documentation

Task: 3.3 - Set Up GitHub Actions CI"

# Commit 5: Docker
git add backend/Dockerfile backend/Dockerfile.dev backend/.dockerignore docker-compose.yml docker-compose.prod.yml Makefile .env.example DOCKER.md
git commit -m "docker: add containerization configuration

- Add production Dockerfile with optimized image
- Add development Dockerfile with hot reload
- Add docker-compose.yml for development
- Add docker-compose.prod.yml with resource limits
- Add Makefile for convenient commands
- Add .env.example for environment variables
- Add comprehensive Docker documentation
- Add .dockerignore to exclude unnecessary files

Features:
- Hot reload in development
- Health checks
- Volume mounts for live updates
- Optimized image size

Task: 3.4 - Create Docker Configuration"

# Commit 6: Refactoring
git add backend/app/helpers.py backend/app/api.py REFACTORING.md
git commit -m "refactor: eliminate DRY violations and improve code quality

- Create helpers.py with reusable functions
- Add create_prompt_copy() to reduce duplication
- Add nullify_collection_for_prompts() extracted from delete_collection
- Refactor 3 functions in api.py to use helpers
- Reduce code duplication by ~60 lines
- All functions now < 20 lines
- Maintain 87% coverage with all 177 tests passing

Task: 3.5 - Refactor Code Smells"

# Commit 7: Pre-commit
git add .pre-commit-config.yaml pyproject.toml PRE_COMMIT_SETUP.md
git commit -m "chore: add pre-commit hooks for code quality (bonus)

- Configure 9 automated checks
- Add Black (code formatter)
- Add isort (import sorter)
- Add Flake8 (linter)
- Add Bandit (security checker)
- Add Hadolint (Dockerfile linter)
- Add trailing whitespace/EOF fixers
- Add YAML/JSON validators
- Add pyproject.toml for tool configuration
- Add comprehensive setup documentation

Bonus Task: Pre-commit Hooks"

# Commit 8: Mutation Testing
git add backend/setup.cfg backend/.mutmut-config MUTATION_TESTING.md ADVANCED_TESTING.md MUTMUT_QUICKSTART.md
git commit -m "test: add mutation testing configuration (bonus)

- Install and configure mutmut
- Add setup.cfg with mutmut configuration
- Add pyproject.toml mutation testing config
- Create comprehensive mutation testing guide
- Create advanced testing strategies document
- Create quick start tutorial
- Document pytest fixture limitations

Bonus Task: Mutation Testing"

# Commit 9: Documentation
git add WEEK3_COMPLETION.md QUICK_START.md .github/copilot-instructions.md
git commit -m "docs: add Week 3 completion summary and quick start guide

- Add comprehensive Week 3 completion summary
- Document all tasks and achievements
- Add quick start guide for new developers
- Update copilot instructions
- Document final metrics (177 tests, 87% coverage)

Week 3 Complete: All tasks + 2 bonus tasks"

# Commit 10: Submission
git add SUBMIT.sh coverage.json backend/requirements.txt
git commit -m "chore: add submission script and final updates

- Add SUBMIT.sh for easy submission
- Add coverage.json for CI integration
- Update requirements.txt with all dependencies
- Ready for Week 3 submission"

echo "✅ All commits created successfully!"
echo "Run 'git log --oneline' to verify"
echo "Run 'git push origin main' to push to GitHub"
```

---

## Alternative: Single Commit (Not Recommended)

If you prefer one commit:

```bash
git add .
git commit -m "feat: complete Week 3 - Testing & DevOps

Tasks completed:
- 3.1: Comprehensive test suite (177 tests, 87% coverage)
- 3.2: Tagging system with TDD (40 tests, 6 cycles)
- 3.3: GitHub Actions CI/CD pipeline
- 3.4: Docker configuration (dev + prod)
- 3.5: Code refactoring (eliminate DRY violations)
- Bonus: Pre-commit hooks (9 checks)
- Bonus: Mutation testing (mutmut configured)

Final metrics:
- 177 tests passing (100%)
- 87% code coverage
- All quality checks passing
- Production-ready backend"
```

---

## Verification Before Push

```bash
# Check what will be committed
git status

# Review changes
git diff --cached

# Verify tests still pass
cd backend && pytest tests/ -v

# Verify coverage
pytest tests/ --cov=app --cov-report=term-missing

# Push to GitHub
git push origin main
```

---

## Notes

- **Recommended**: Use the 10-commit strategy for clear history
- Each commit is focused on a single task/feature
- Commit messages follow conventional commits format
- Easy to review and understand changes
- Can cherry-pick or revert specific features if needed

**After pushing, check GitHub Actions tab to see CI running!**
