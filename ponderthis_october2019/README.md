The puzzle from [October’s IBM Ponder This challenge](http://www.research.ibm.com/haifa/ponderthis/challenges/October2019.html).

Our goal is to "**find set of five banknotes such that:**
1. **Each integer dollar value between 0 and 99 dollars can be paid in a unique way with a minimal number of notes**
2. **The probability of the amount of money uniformly distributed in the [0,99] range being the same if the set of notes of 2 persons is the same takes a maximum value**".

I used two different techniques:
1. **CPLEX Optimizer** provided by IBM as optimization engine to find a set with a minimal number of banknotes for specific amount of money (class *MinSetGenerator*) and to check whether exists another set with a minimal number of banknotes (class *MinSetChecker*). These classes are in the file [Models.py](Models.py)
2. **Genetic algorithm** to find a set with a minimal number of banknotes that the probability of the amount of money uniformly distributed in the [0,99] range being the same if the set of notes of 2 persons is the same takes a maximum value (class *GeneticAlgorithmBanknotes*). This class is in the file [GeneticAlgorithmBanknotes.py](GeneticAlgorithmBanknotes.py)

This puzzle is very similar on September challenge (just simply change fitness function).
