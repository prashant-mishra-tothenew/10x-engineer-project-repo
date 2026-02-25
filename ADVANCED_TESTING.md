# Advanced Testing Techniques

This document covers advanced testing strategies beyond basic unit and integration tests.

## 1. Mutation Testing ✅

**Tool**: mutmut
**Purpose**: Test your tests by introducing bugs
**Status**: Configured and ready to use

### Quick Start

```bash
cd backend

# Install
pip install mutmut

# Run on utils module
mutmut run

# View results
mutmut results
mutmut html
```

### What It Does

Mutation testing introduces small changes (mutations) to your code:
- Changes `+` to `-`
- Changes `>` to `>=`
- Changes `and` to `or`
- Flips `True` to `False`

If your tests still pass after these changes, you have a test gap!

### Example

```python
# Original code
def add(a, b):
    return a + b

# Mutation: Change + to -
def add(a, b):
    return a - b

# If tests still pass, you need better tests!
```

**See `MUTATION_TESTING.md` for complete guide.**

## 2. Property-Based Testing ✅

**Tool**: Hypothesis
**Purpose**: Generate random test cases automatically
**Status**: Already implemented in test suite

### Example from Our Tests

```python
from hypothesis import given, strategies as st

@given(
    title=st.text(min_size=1, max_size=200),
    content=st.text(min_size=1)
)
def test_prompt_creation_with_random_data(title, content):
    """Test prompt creation with randomly generated data"""
    prompt = Prompt(title=title, content=content)
    assert prompt.title == title
    assert prompt.content == content
```

Hypothesis generates hundreds of test cases automatically!

## 3. Fuzzing

**Tool**: atheris (Google's fuzzer for Python)
**Purpose**: Find crashes and security issues
**Status**: Optional - can be added

### What It Does

Fuzzing throws random/malformed data at your code to find:
- Crashes
- Hangs
- Security vulnerabilities
- Unexpected behavior

### Example Use Case

```python
import atheris
import sys

def fuzz_api_endpoint(data):
    """Fuzz test an API endpoint"""
    try:
        # Try to crash the endpoint with random data
        response = client.post("/prompts", json=data)
    except Exception as e:
        # Log crashes for investigation
        print(f"Crash found: {e}")

atheris.Setup(sys.argv, fuzz_api_endpoint)
atheris.Fuzz()
```

## 4. Load Testing

**Tool**: locust
**Purpose**: Test performance under load
**Status**: Can be added for production

### Example

```python
from locust import HttpUser, task, between

class PromptLabUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def list_prompts(self):
        self.client.get("/prompts")

    @task(3)  # 3x more frequent
    def create_prompt(self):
        self.client.post("/prompts", json={
            "title": "Test",
            "content": "Test content"
        })
```

Run with: `locust -f locustfile.py`

## 5. Contract Testing

**Tool**: pact-python
**Purpose**: Test API contracts between services
**Status**: Useful for microservices

### What It Does

Ensures frontend and backend agree on API structure:
- Request format
- Response format
- Status codes
- Error messages

## 6. Snapshot Testing

**Tool**: pytest-snapshot
**Purpose**: Detect unexpected changes in output
**Status**: Can be added

### Example

```python
def test_api_response_structure(snapshot):
    """Ensure API response structure doesn't change"""
    response = client.get("/prompts")
    snapshot.assert_match(response.json())
```

If response structure changes, test fails and shows diff.

## 7. Security Testing

**Tools**: bandit, safety
**Purpose**: Find security vulnerabilities
**Status**: ✅ Bandit configured in pre-commit hooks

### Current Setup

```bash
# Run security scan
bandit -r app/

# Check for vulnerable dependencies
safety check
```

## 8. Performance Testing

**Tool**: pytest-benchmark
**Purpose**: Track performance regressions
**Status**: Can be added

### Example

```python
def test_search_performance(benchmark):
    """Ensure search stays fast"""
    result = benchmark(search_prompts, prompts, "test")
    assert result  # Benchmark tracks time automatically
```

## Testing Pyramid

```
        /\
       /  \
      / E2E \          Few, slow, expensive
     /------\
    /  API   \         More, medium speed
   /----------\
  / Unit Tests \       Many, fast, cheap
 /--------------\
```

### Our Current Coverage

1. **Unit Tests** ✅ - 177 tests
   - Models, storage, utils
   - Fast, isolated
   - 87% coverage

2. **Integration Tests** ✅ - API tests
   - Full request/response cycle
   - TestClient
   - All endpoints covered

3. **Property-Based** ✅ - Hypothesis
   - Random data generation
   - Edge case discovery

4. **Mutation Testing** ✅ - mutmut
   - Test quality verification
   - Gap identification

5. **Security** ✅ - Bandit
   - Vulnerability scanning
   - Pre-commit hooks

## Python Testing Ecosystem

| Python Tool | Purpose |
|-------------|---------|
| pytest | Unit testing framework |
| hypothesis | Property-based testing |
| mutmut | Mutation testing |
| locust | Load testing |
| bandit | Security scanning |
| pytest-cov | Coverage reporting |

## Recommended Testing Strategy

### For Every Feature
1. ✅ Write unit tests (TDD)
2. ✅ Write integration tests
3. ✅ Check coverage (>80%)
4. ✅ Run linting/security checks

### Weekly
1. Run mutation testing on critical modules
2. Review and fix surviving mutations
3. Update tests for edge cases

### Before Release
1. Run full test suite
2. Check mutation score on core logic
3. Run security scans
4. Performance benchmarks
5. Load testing (if applicable)

## Tools We're Using

### Active ✅
- pytest - Unit/integration testing
- pytest-cov - Coverage reporting
- hypothesis - Property-based testing
- flake8 - Linting
- bandit - Security scanning
- mutmut - Mutation testing
- pre-commit - Automated checks

### Can Add Later
- locust - Load testing
- pytest-benchmark - Performance testing
- atheris - Fuzzing
- pact - Contract testing
- pytest-snapshot - Snapshot testing

## Quick Commands

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# Mutation testing
mutmut run
mutmut results

# Security scan
bandit -r app/

# Property-based tests only
pytest tests/ -k "hypothesis"

# Performance benchmarks (if added)
pytest tests/ --benchmark-only
```

## Best Practices

### DO:
✅ Write tests first (TDD)
✅ Aim for 80%+ coverage
✅ Use property-based testing for complex logic
✅ Run mutation testing on critical code
✅ Automate with pre-commit hooks
✅ Keep tests fast (<5 seconds total)

### DON'T:
❌ Skip tests for "simple" code
❌ Aim for 100% coverage everywhere
❌ Write slow tests
❌ Test implementation details
❌ Ignore failing tests
❌ Commit without running tests

## Resources

- [Mutation Testing Guide](MUTATION_TESTING.md)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://testdriven.io/)

## Summary

We've implemented a comprehensive testing strategy:
- **177 unit/integration tests** (all passing)
- **87% code coverage** (exceeds 80% goal)
- **Property-based testing** with Hypothesis
- **Mutation testing** configured with mutmut
- **Security scanning** with Bandit
- **Automated checks** with pre-commit hooks

This gives us high confidence in code quality and catches bugs early!
