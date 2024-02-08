# unittest

---

### unittest

```zsh
py -m unittest
```

### unittest with verbose

```zsh
py -m unittest -v
```

### unittest discover tests

```zsh
py -m unittest discover -v
```

### unittest tests a single module

```zsh
py -m unittest tests.test_unittest_001 -v
```

### unittest tests a class in a particular module

```zsh
py -m unittest tests.test_unittest_002.TestBankAccount -v
```

### unittest tests a particular test

```zsh
py -m unittest tests.test_unittest_002.TestBankAccount.test_withdraw -v
```

# What is a test coverage

Test coverage is a ratio between the number of lines executed by at least one
test case and the total number of lines of the code base.

```math
test coverage = lines of code executed / total number of lines
```

```zsh
 python -m coverage run -m unittest
 python -m coverage report
 python -m coverage html
```

---

# pytest

```zsh
pytest -v
pytest -m "not slow"
pytest -m "slow"
pytest -m "not slow and structured"
pytest -s
pytest -s --cov
pytest -s --cov

```
