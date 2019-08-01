The puzzle from [July’s IBM Ponder This challenge](http://www.research.ibm.com/haifa/ponderthis/challenges/July2019.html).

Our goal is to "**find two non-intersecting knight's cycles of length 14 on boards of size <= 40 such that the difference between their areas is at least 7**".

Let's discuss point-by-point.

* Board size is the product of number of vertical squares X and horizontal squares Y. Because of X * Y <= 40, then we may reduce the number of combination (X,Y):
  * since knight's movement looks like the letter "L", so min(X,Y) >= 2
  * since knight's cycle must be closed and non-intersected, so min(X,Y) >= 3
  * consider that (X,Y) is invariant to (Y,X)
  * don't consider subsets, i.e. (7,5) is subset of (8,5)
  * consider [the longest uncrossed knight's cycle](https://en.wikipedia.org/wiki/Longest_uncrossed_knight%27s_path)
  
  So, our candidates (X,Y) are: **(13,3), (10,4), (8,5)**.

* The costraint that knight's cycle must be non-intersecting may be obtained from [this article](http://www.cs.swan.ac.uk/~cssimon/line_intersection.html). Let's define one of the khight's cycle edge as e1 with start point (x1,y1) and end point (x2,y2), another as e2 with start point (x3,y3) and end point (x4,y4). Then calculate t(a) and t(b) to check lines intersection.

* To compute polygon area we may use results from [this article](https://www.mathopenref.com/coordpolygonarea.html).

The puzzle was solved using *Constraint Programming (CP)* - a powerful paradigm for solving combinatorial search problems that draws on a wide range of techniques from artificial intelligence, operations research, algorithms, graph theory and elsewhere. 

I used **CP Optimizer** provided by IBM as optimization engine. The optimization model was written in **OPL**.

On the one hand, we need to find the non-intersecting knight's cycle with minimum polygon area. We should solve the minimization problem - minimize polygon area of khight's cycle depending on board size (X,Y).

The results are given in the table below. 

| Parameter                   | Value                                            |
| :---                        | :---                                             |
| board size (X,Y)            | **(8,5)**                                        | 
| knight's cycle              | **b2 c4 d6 b5 c7 a8 b6 a4 c5 b3 a1 c2 e1 d3 b2** |
| polygon area:               | **8**                                            |

On the other hand, we need to find the non-intersecting knight's cycle with maximum polygon area. We should solve the maximization problem - maximize polygon area of khight's cycle depending on board size (X,Y). 

The results are given in the table below. 

| Parameter                   | Value                                            |
| :---                        | :---                                             |
| board size (X,Y)            | **(8,5)**                                        | 
| knight's cycle              | **c2 a1 b3 a5 c6 a7 c8 e7 d5 e3 c4 b2 d3 e1 c2** |
| polygon area:               | **15**                                           |

So, the difference between their areas is exactly 7.

Graphical perspectives of these khight's cycles are given below (left: polygon area is 8, right: polygon area is 15):
<img src="https://github.com/rsalikhov/pao/blob/master/ponderthis_july2019/polygon_area_8.jpg" width="200"> 
<img src="https://github.com/rsalikhov/pao/blob/master/ponderthis_july2019/polygon_area_15.jpg" width="200"> 
