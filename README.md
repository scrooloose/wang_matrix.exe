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
./bin/wang_matrix.exe <(python generate.py 80 40 30)
```

Python Solver
----------------

There's a Python solver too. It does a breadth first search of the maze.

```
python solver.py mazes/2.maze
```

```
       5    10   15   20   25   30   35   40   45   50   55   60
   ################################################################
   #        #        #  oooooooooooooooooooooooooooooooooooooooo  #
   #  ####  #  ####### o############################  ##########o #
   #     #     # oooooo #     #     #  oooooooooo  #     #  oooo  #
 5 ####  #  ####o #######  #  #  #  # o##########o ####  # o#######  5
   #     #  #  o  #        #     #  #  o     #  # o#     #  o  #  #
   #  ####  # o####  ###################o ####### o##########o ####
   #  #     #o #  #  #              #  #o # ooo #  o  o  #  # oo  #
   #  ####### o####  #  ##########  #  # o#o # o####oo#o #######o #
10 #        #o #     #     #     #  #  #  o  #  o  #  # oooooooo  # 10
   #  ####  #o #  #######  ####  #  #############o #  #############
   #  #     # o#        #     #  #              # o#           #  #
   #  #  ####o #############  #  #############  # o####  ####  ####
   #  #  #  o                 #              #  #  o  #  #  #     #
15 #  #  # o######################  #######  ## ####o #  #  ####  # 15
   #  #     o  #     #                    #  #     #o #     #     #
   #  #######o #  #  #  ####  #######  #######  #  #o ####  #  ####
   #  #  oooo  #  #  #     #        #  #        #  # o#  #  #     #
   #  # o#######  #  ####  #  ##########  ########## o#  #  ####  #
20 #  # o#        #     #  #     #     #           # o#     #  #  # 20
   #  #o #  #############  ####  #  #############  # o##########  #
   #  #o                      #  #     #  #  #     #  oooo  #  #  #
   #  # o############################  #######  ##########o ####  #
   #  #  oooo  #     #  #        #  #  #  #              # o#     #
25 ##########o #  #  #  #  ####  ####  ####  ####  #######o #  #### 25
   #     #  o  #  #  #  #  #  #        #  #  #     #     #o #     #
   #  #### o####  #  #  #  ################  #  ####  #  # o#######
   #        o  #  #  #  #                 #  #  #     #  #  oooo  #
   ##########o ####  #  ################  #  #  ################o #
30 sooooooooo        #                 #     #              # oo  # 30
   ##########################################################e#####
       5    10   15   20   25   30   35   40   45   50   55   60

```
