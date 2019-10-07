from docplex.mp.model import Model
import math


class MinSetGenerator:
    """
    Optimization model that generate a set with a minimal number of banknotes
    Attributes:
        n: number of banknotes (int)
        banknotes: set of banknotes (list)
        money: amount of money (int)
    """

    def __init__(self, n, banknotes, money):
        self.n = n
        self.banknotes = banknotes
        self.money = money

    def generate(self):
        """
        Generate a set with a minimal number of banknotes
        :return: a set with a minimal number of banknotes (list)
        """
        # prepare data
        banknote_quantity_max = [int(math.floor(self.money / self.banknotes[i])) for i in range(0, self.n)]
        # model
        mdl = Model(name='MinSetGenerator')
        # decision variables
        mdl.banknote_quantity = {i: mdl.integer_var(lb=0, ub=banknote_quantity_max[i]) for i in range(0, self.n)}
        # decision expressions
        money_amount = mdl.sum(mdl.banknote_quantity[i] * self.banknotes[i] for i in range(0, self.n))
        notes_quantity = mdl.sum(mdl.banknote_quantity[i] for i in range(0, self.n))
        # constraints
        mdl.add_constraint(money_amount == self.money)
        # strategy
        mdl.minimize(notes_quantity)
        # solve model: return quantity of each banknotes and a set with a minimal number of banknotes
        if not mdl.solve():
            print('*** No solution!')
            return None, None
        else:
            return [int(mdl.banknote_quantity[i].solution_value) for i in range(0, self.n)], \
                   [self.banknotes[i] for i in range(0, self.n) if mdl.banknote_quantity[i].solution_value > 0]


class MinSetChecker:
    """
        Optimization model that check whether exists another set with a minimal number of banknotes
        Attributes:
            n: number of banknotes (int)
            banknotes: set of banknotes (list)
            money: amount of money (int)
            banknote_quantity: quantity of each banknotes in set (possible 'a set with a minimal number of banknotes')
        """

    def __init__(self, n, banknotes, money, banknote_quantity):
        self.n = n
        self.banknotes = banknotes
        self.money = money
        self.banknote_quantity = banknote_quantity

    def is_exist_another_solution(self):
        """
        Check whether exists another set with a minimal number of banknotes
        :return: True if it exists, False if not
        """
        # prepare data
        notes_quantity_min = sum(self.banknote_quantity)
        banknote_quantity_max = [int(math.floor(self.money / self.banknotes[i])) for i in range(0, self.n)]
        # model
        mdl = Model(name='MinSetChecker')
        # decision variables
        mdl.banknote_quantity = {i: mdl.integer_var(lb=0, ub=banknote_quantity_max[i]) for i in range(0, self.n)}
        # decision expressions
        money_amount = mdl.sum(mdl.banknote_quantity[i] * self.banknotes[i] for i in range(0, self.n))
        notes_quantity = mdl.sum(mdl.banknote_quantity[i] for i in range(0, self.n))
        # constraints
        mdl.add_constraint(money_amount == self.money)
        mdl.add_constraint(notes_quantity == notes_quantity_min)
        mdl.add_constraint(
            mdl.sum(mdl.banknote_quantity[i] == self.banknote_quantity[i] for i in range(0, self.n)) != self.n
        )
        # solve model: return True if it exists, False if not
        if not mdl.solve():
            return False
        else:
            return True
