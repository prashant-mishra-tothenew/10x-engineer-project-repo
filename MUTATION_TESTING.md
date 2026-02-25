# Mutation Testing Guide

## What is Mutation Testing?

Mutation testing is an advanced technique that evaluates the quality of your test suite by introducing small bugs (mutations) into your code and checking if your tests catch them.

### The Concept

**Traditional Coverage**: Measures which lines of code are executed
**Mutation Testing**: Measures if your tests actually verify the code works correctly

### Example

```python
# Original code
def add(a, b):
    return a + b

# Mutation 1: Change operator
def add(a, b):
    return a - b  # Will your tests catch this?

# Mutation 2: Change return
def add(a, b):
    return a  # Will your tests catch this?
```

If your tests still pass after these mutations, they're not testing properly!

## Mutation Testing Tools

| Tool | Purpose |
|------|---------|
| mutmut | Most popular Python mutation testing tool |
| cosmic-ray | Alternative mutation testing framework |
| MutPy | Academic mutation testing tool |

## Installation

```bash
cd backend
pip install mutmut
```

## Basic Usage

### Run Mutation Testing

```bash
# Run on all code
mutmut run

# Run on specific file
mutmut run --paths-to-mutate=app/utils.py

# Run with specific test command
mutmut run --runner="pytest tests/"
```

### View Results

```bash
# Show summary
mutmut results

# Show specific mutation
mutmut show 1

# Show all surviving mutations (gaps in tests)
mutmut show --all
```

### Generate HTML Report

```bash
mutmut html
# Opens browser with detailed report
```

## Understanding Results

### Mutation States

1. **Killed** ✅ - Test caught the mutation (good!)
2. **Survived** ❌ - Test didn't catch the mutation (test gap!)
3. **Timeout** ⏱️ - Mutation caused infinite loop
4. **Suspicious** ⚠️ - Mutation behaved unexpectedly

### Mutation Score

```
Mutation Score = (Killed / Total) × 100%

Example:
- 100 mutations created
- 85 killed by tests
- 15 survived
- Score: 85%
```

**Good Scores:**
- 80%+ : Excellent test quality
- 60-80%: Good test quality
- <60%: Needs improvement

## Types of Mutations

### 1. Arithmetic Operators
```python
# Original
result = a + b

# Mutations
result = a - b  # Change +  to -
result = a * b  # Change + to *
result = a / b  # Change + to /
```

### 2. Comparison Operators
```python
# Original
if x > 5:

# Mutations
if x >= 5:  # Change > to >=
if x < 5:   # Change > to <
if x == 5:  # Change > to ==
```

### 3. Boolean Operators
```python
# Original
if a and b:

# Mutations
if a or b:   # Change and to or
if a:        # Remove b
if b:        # Remove a
```

### 4. Return Values
```python
# Original
return True

# Mutations
return False  # Flip boolean
return None   # Change to None
```

### 5. Constants
```python
# Original
limit = 10

# Mutations
limit = 11  # Increment
limit = 9   # Decrement
limit = 0   # Set to zero
```

## Running on PromptLab

### Step 1: Install mutmut

```bash
cd backend
pip install mutmut
```

### Step 2: Configure mutmut

Create `.mutmut-config.py`:

```python
def pre_mutation(context):
    """Skip certain files or lines"""
    # Skip test files
    if 'test_' in context.filename:
        context.skip = True

    # Skip __init__.py
    if '__init__' in context.filename:
        context.skip = True
```

### Step 3: Run on a Small Module First

```bash
# Start with utils.py (small, well-tested)
mutmut run --paths-to-mutate=app/utils.py --runner="pytest tests/test_utils.py -x"

# View results
mutmut results
```

### Step 4: Analyze Survivors

```bash
# Show mutations that survived
mutmut show --all

# Show specific mutation
mutmut show 5
```

### Step 5: Fix Test Gaps

If a mutation survives, add a test to catch it!

## Example: Finding a Test Gap

### Original Code (app/utils.py)
```python
def validate_prompt_content(content: str) -> bool:
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10
```

### Mutation Created
```python
def validate_prompt_content(content: str) -> bool:
    if not content or not content.strip():
        return False
    return len(content.strip()) > 10  # Changed >= to >
```

### If This Survives
Your tests don't check the boundary condition (exactly 10 characters)!

### Fix: Add Test
```python
def test_validate_content_exactly_10_chars():
    """Test boundary: exactly 10 characters should be valid"""
    content = "1234567890"  # Exactly 10 chars
    assert validate_prompt_content(content) == True
```

## Practical Workflow

### 1. Run Mutation Testing
```bash
mutmut run --paths-to-mutate=app/utils.py
```

### 2. Check Score
```bash
mutmut results
# Output: 15/20 killed (75%)
```

### 3. Find Survivors
```bash
mutmut show --all
```

### 4. Add Missing Tests
Write tests to kill surviving mutations

### 5. Re-run
```bash
mutmut run --paths-to-mutate=app/utils.py
# Goal: 100% killed
```

## Configuration File

Create `setup.cfg` or `pyproject.toml`:

```toml
[tool.mutmut]
paths_to_mutate = "app/"
backup = false
runner = "pytest tests/ -x --tb=short"
tests_dir = "tests/"
```

## Common Mutations to Watch For

### 1. Off-by-One Errors
```python
# Original: range(10)
# Mutation: range(11) or range(9)
```

### 2. Boundary Conditions
```python
# Original: if x >= 5
# Mutation: if x > 5
```

### 3. Boolean Logic
```python
# Original: if a and b
# Mutation: if a or b
```

### 4. Return Values
```python
# Original: return True
# Mutation: return False
```

### 5. Empty Collections
```python
# Original: return []
# Mutation: return [None]
```

## Interpreting Results

### High Mutation Score (80%+)
✅ Excellent test quality
✅ Tests verify behavior, not just coverage
✅ Confident in refactoring

### Medium Score (60-80%)
⚠️ Good coverage but some gaps
⚠️ Add tests for edge cases
⚠️ Check boundary conditions

### Low Score (<60%)
❌ Tests are too weak
❌ Many untested scenarios
❌ High risk of bugs

## Best Practices

### DO:
✅ Start with small, well-tested modules
✅ Run mutation testing regularly
✅ Focus on critical business logic
✅ Use mutation testing to guide test writing
✅ Aim for 80%+ mutation score on core code

### DON'T:
❌ Run on entire codebase initially (too slow)
❌ Aim for 100% on everything (diminishing returns)
❌ Ignore surviving mutations
❌ Run mutation testing in CI (too slow)
❌ Mutate test files themselves

## Performance Tips

### Speed Up Mutation Testing

1. **Test Specific Modules**
   ```bash
   mutmut run --paths-to-mutate=app/utils.py
   ```

2. **Use Parallel Execution**
   ```bash
   mutmut run --use-coverage --parallel=4
   ```

3. **Skip Slow Tests**
   ```bash
   mutmut run --runner="pytest tests/ -m 'not slow'"
   ```

4. **Use Coverage Data**
   ```bash
   # Only mutate covered lines
   pytest --cov=app --cov-report=xml
   mutmut run --use-coverage
   ```

## Integration with CI/CD

**Don't run in CI** (too slow), but run locally:

```bash
# Before committing critical changes
mutmut run --paths-to-mutate=app/models.py
mutmut results
```

## Example Session

```bash
$ cd backend

$ mutmut run --paths-to-mutate=app/utils.py
- Mutation testing starting -
These are the steps:
1. A full test suite run will be made to make sure we
   can run the tests successfully and we know how long
   it takes (to detect infinite loops for example)
2. Mutants will be generated and checked

Running tests without mutations
⠏ Running...
✅ Tests pass (2.3s)

Creating mutants
⠏ Creating...
✅ 25 mutants created

Running mutants
⠙ 1/25 ⠹ 2/25 ⠸ 3/25 ... ✅ 25/25

Results:
- Killed: 20 (80%)
- Survived: 5 (20%)
- Timeout: 0
- Suspicious: 0

$ mutmut show --all
Survived mutants:
1. app/utils.py:15 (>= to >)
2. app/utils.py:23 (and to or)
3. app/utils.py:30 (return [] to return [None])
4. app/utils.py:45 (+ to -)
5. app/utils.py:52 (True to False)

$ mutmut show 1
--- app/utils.py
+++ app/utils.py
@@ -12,7 +12,7 @@
 def validate_prompt_content(content: str) -> bool:
     if not content or not content.strip():
         return False
-    return len(content.strip()) >= 10
+    return len(content.strip()) > 10

# Now add a test for exactly 10 characters!
```

## Resources

- [Mutmut Documentation](https://mutmut.readthedocs.io/)
- [Mutation Testing Concepts](https://en.wikipedia.org/wiki/Mutation_testing)
- [Python Testing Best Practices](https://docs.pytest.org/)

## Summary

Mutation testing helps you:
1. Find gaps in your test suite
2. Improve test quality beyond coverage
3. Catch edge cases and boundary conditions
4. Build confidence in your tests
5. Ensure tests actually verify behavior

**Remember**: 87% code coverage doesn't mean 87% of bugs are caught. Mutation testing tells you how well your tests actually work!
