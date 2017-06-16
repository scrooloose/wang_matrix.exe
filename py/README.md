# Install

```
pip install --user virtualenv
virtualenv ~/.local/venvs/wangmatrix
~/.local/venvs/wangmatrix/bin/pip install --editable .
```

# Run

```
source ~/.local/venvs/wangmatrix/bin/activate
wangmatrix.solve.py <(wangmatrix.generate.py 100 40 10)
```

# Test

```
pip install --user tox
tox
```
