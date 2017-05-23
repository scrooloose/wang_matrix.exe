Install
-------

Check out this repo, then run `bundle install` in the root dir.


Usage
-----

```
./bin/wang_matrix.exe [maze-file-path]
```

Maze files must consist of walls `#`, a starting point `s` and an end point `e`.

Random Maze
-------------

You can have Wang Matrix solve a random maze as follows:

```
./bin/wang_matrix.exe <(python generate.py 100 40 5)
```
