The puzzle from [September’s IBM Ponder This challenge](http://www.research.ibm.com/haifa/ponderthis/challenges/September2019.html).

Our goal is to "**find set of five banknotes such that:**
1. **Each integer dollar value between 0 and 99 dollars can be paid in a unique way with a minimal number of notes**
2. **The probability above (same set of banknotes for two different random amounts of money uniformly distributed in the [0,99] range) would be exactly 4%**".

I used two different techniques:
1. **CPLEX Optimizer** provided by IBM as optimization engine to find a set with a minimal number of banknotes for specific amount of money (class *MinSetGenerator*) and to check whether exists another set with a minimal number of banknotes (class *MinSetChecker*). These classes are in the file *Models.py*
2. **Genetic algorithm** to find a set with a minimal number of banknotes that the probability that 2 person have the same set of banknotes (same set of banknotes for two different random amounts of money uniformly distributed in the [0,99]) is exactly 4% (class *GeneticAlgorithmBanknotes*). This class is in the file *GeneticAlgorithm.py* 
