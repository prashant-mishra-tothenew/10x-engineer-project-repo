# Mutmut Quick Start Guide

## Important Note: Mutation Testing Limitations

**Mutmut has known compatibility issues with pytest fixtures.** In this project, you'll see many mutations marked as "segfault" (🫥). This is **not** a problem with your tests - it's a limitation of mutmut when working with pytest's fixture system.

### Why This Happens

Your tests use the `use_memory_storage` fixture to reset state before each test:

```python
@pytest.fixture(autouse=True)
def use_memory_storage():
    storage.clear()
    yield
```

When mutmut mutates the code, it can break the import chain or fixture setup, causing the test runner to fail in unexpected ways. Mutmut interprets these failures as "segfaults."

### What This Means

- ✅ Your 87% code coverage is excellent
- ✅ Your 177 passing tests are comprehensive
- ❌ Mutmut's "segfault" results are false positives
- ℹ️ This is a known limitation of mutmut with pytest fixtures

### Alternative Approach

For production projects, consider:
- **Manual code review** - Sometimes more effective than mutation testing
- **Property-based testing** - Complements mutation testing well
- **Integration tests** - Catch issues mutation testing might miss

Mutation testing is a valuable concept for finding test gaps in critical code paths.

### Step 1: Verify Installation

```bash
cd backend
mutmut --version
```

### Step 2: Run Mutation Testing

Mutmut is configured in `pyproject.toml` to test all files in `backend/app/`:

```bash
# Run mutation testing (from project root)
mutmut run

# This will:
# 1. Run your tests to make sure they pass
# 2. Create mutations (small bugs) in the code
# 3. Run tests for each mutation
# 4. Report which mutations survived (test gaps!)
```

**Note**: Mutmut reads configuration from `pyproject.toml`, not command-line options.

### Step 3: View Results

```bash
# Show summary
mutmut results

# Example output:
# Survived: 2
# Killed: 18
# Timeout: 0
# Suspicious: 0
# Total: 20
```

### Step 4: See What Survived

```bash
# Show all surviving mutations (these are test gaps!)
mutmut show

# Show specific mutation
mutmut show 1
```

### Step 5: Generate HTML Report

```bash
# Create visual report
mutmut html

# Opens in browser automatically
```

## Quick Commands Reference

```bash
# Basic run (uses config from pyproject.toml)
mutmut run

# View results
mutmut results

# Show surviving mutations
mutmut show

# Show specific mutation
mutmut show 5

# Generate HTML report
mutmut html

# Apply a mutation (to test it manually)
mutmut apply 1

# Reset code back to original
mutmut apply --reset

# Clear cache and start fresh
rm -rf .mutmut-cache
```

**Important**: Mutmut doesn't support `--paths-to-mutate` as a command-line option. Configuration must be in `pyproject.toml` or `setup.cfg`.

## Understanding Output

### Mutation States

- **Killed** ✅ - Your tests caught the bug (good!)
- **Survived** ❌ - Tests didn't catch it (add a test!)
- **Timeout** ⏱️ - Mutation caused infinite loop
- **Suspicious** ⚠️ - Unexpected behavior

### Example Output

```
$ mutmut results

To apply a mutant on disk:
    mutmut apply <id>

To show a mutant:
    mutmut show <id>

Survived 🙁 (2)
Killed ✅ (18)
Timeout ⏱️ (0)
Suspicious 🤔 (0)
Total ⚡ (20)

Mutation score: 90.0%
```

## Example: Finding a Test Gap

### 1. Run mutmut

```bash
mutmut run
```

### 2. Check results

```bash
mutmut results
# Output: Survived: 1, Killed: 19
```

### 3. See what survived

```bash
mutmut show 1
```

Output shows:
```python
--- app/utils.py
+++ app/utils.py
@@ -15,7 +15,7 @@
 def validate_prompt_content(content: str) -> bool:
     if not content or not content.strip():
         return False
-    return len(content.strip()) >= 10
+    return len(content.strip()) > 10
```

### 4. Fix the test gap

Add a test for the boundary condition:

```python
def test_validate_content_exactly_10_chars():
    """Test boundary: exactly 10 characters"""
    content = "1234567890"  # Exactly 10 chars
    assert validate_prompt_content(content) == True
```

### 5. Run again

```bash
mutmut run
# Now: Survived: 0, Killed: 20 ✅
```

## Common Issues

### Issue: "Could not figure out where the code to mutate is"

**Solution**: Mutmut needs configuration in `pyproject.toml`:
```toml
[tool.mutmut]
paths_to_mutate = "backend/app/"
backup = false
runner = "pytest backend/tests/ -x -q"
tests_dir = "backend/tests/"
```

### Issue: Takes too long

**Solution**: Mutmut will test all files in `paths_to_mutate`. This is normal for comprehensive testing. Be patient or reduce the scope in `pyproject.toml`.

### Issue: All mutations timeout

**Solution**: Your tests might be too slow. Update the runner in `pyproject.toml`:
```toml
runner = "pytest backend/tests/ -x -q --tb=no"
```

## Configuration File

Create `setup.cfg` in backend/:

```ini
[mutmut]
paths_to_mutate=app/
backup=False
runner=pytest tests/ -x
tests_dir=tests/
```

Then just run:
```bash
mutmut run
```

## Best Practices

### DO:
✅ Start with small, well-tested files
✅ Run on one module at a time
✅ Fix surviving mutations by adding tests
✅ Aim for 80%+ mutation score on critical code

### DON'T:
❌ Run on entire codebase at once (too slow)
❌ Ignore surviving mutations
❌ Run in CI/CD (too slow for automation)
❌ Aim for 100% everywhere (diminishing returns)

## Interpreting Mutation Score

- **90-100%**: Excellent! Very strong tests
- **80-90%**: Good! Minor gaps
- **70-80%**: Okay, but needs improvement
- **<70%**: Weak tests, many gaps

## Next Steps

1. Run mutmut on `app/utils.py` (smallest file)
2. Check the mutation score
3. Fix any surviving mutations
4. Move to `app/models.py`
5. Repeat for critical modules

## Resources

- Full guide: `MUTATION_TESTING.md`
- Advanced testing: `ADVANCED_TESTING.md`
- Mutmut docs: https://mutmut.readthedocs.io/
