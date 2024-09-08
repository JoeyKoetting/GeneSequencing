###########################################
# KEY   Array [i][j]
#
#       String 1
#
#   S   j j j j j j j j j
#   t   i
#   r   i
#   i   i
#   n   i
#   g   i
#   2   i
#       i

from enum import Enum


###########################################
# Cell
# Stores data for each cell in array
###########################################
class Cell:

    def __init__(self, parent, transition_type, cost):
        self.parent = parent
        self.transition_type = transition_type
        self.cost = cost


###########################################
# Transition
# Stores different transitions
###########################################
class Transition(Enum):
    UP = 0
    LEFT = 1
    DIAGONAL = 2


###########################################
# Sequence
# Sequences 2 strings
#
# Time Complexity: Depends on user input
# if banded see banded_algorithm complexity
# if not see unrestricted_algorithm complexity
# Space Complexity: Depends on user input
# if banded see banded_algorithm complexity
# if not see unrestricted_algorithm complexity
###########################################
class Sequence:

    def __init__(self, string1, string2, banded):
        self.string1 = string1
        self.string1_len = len(string1)
        self.string2 = string2
        self.string2_len = len(string2)
        self.array = []
        if not banded:
            self.unrestricted_prep_array()
            self.unrestricted_algorithm()
            self.score = self.get_score()
        else:
            # We do not allow more than 3 insertions/ deletion
            if self.string1_len - self.string2_len <= 4:
                self.banded_prep_array()
                self.banded_algorithm()
                self.score = self.get_score()
            else:
                self.score = float('inf')

    ###########################################
    # def unrestricted_prep_array
    # Preps array by adding first row
    #
    # Time Complexity: O(n) Creates n cells
    # Space Complexity: O(n) Stores n cells
    ###########################################
    def unrestricted_prep_array(self):
        # add first row to array
        self.array.append([])

        # temp cell
        tmp_cell = Cell(None, None, 0)

        # add first cell to array
        self.array[0].append(tmp_cell)

        # add remaining cells to row
        for j in range(1, self.string1_len + 1):
            tmp_cell = Cell(tmp_cell, Transition.LEFT, j * 5)
            self.array[0].append(tmp_cell)

    ###########################################
    # def unrestricted_algorithm
    # Sequences 2 strings
    #
    # Time Complexity: O(n * m) For each letter in string 1, traverse string 2
    # Space Complexity: O(n * m) Makes and stores things in array of size n * m
    ###########################################
    def unrestricted_algorithm(self):

        # for each row (string 2)
        for i in range(1, self.string2_len + 1):

            # add another row to array
            self.array.append([])

            for j in range(1, self.string1_len + 1 - (i - 1)):

                # diagonal_index    = [i - 1]   [j - 1]
                # up_index          = [i - 1]   [j]
                # left_index        = [i]       [j - 1]

                # get up cost
                up_cost = self.array[i - 1][j].cost + 5

                # get left cost
                if len(self.array[i]) > 0:
                    left_cost = self.array[i][-1].cost + 5
                else:
                    left_cost = float("inf")

                if self.string1[j - 1 + (i - 1)] == self.string2[i - 1]:
                    strings_match = True
                else:
                    strings_match = False

                if strings_match:
                    # strings are the same, cost: -3
                    diagonal_cost = self.array[i - 1][j - 1].cost - 3
                else:
                    # strings are not the same, cost: +1
                    diagonal_cost = self.array[i - 1][j - 1].cost + 1

                # stores smallest parent
                if diagonal_cost <= up_cost and diagonal_cost <= left_cost:
                    if strings_match:
                        self.array[i].append(Cell(self.array[i - 1][j - 1],
                                                  Transition.DIAGONAL,
                                                  diagonal_cost))
                    else:
                        self.array[i].append(Cell(self.array[i - 1][j - 1],
                                                  Transition.DIAGONAL,
                                                  diagonal_cost))
                elif up_cost <= left_cost:
                    self.array[i].append(Cell(self.array[i - 1][j],
                                              Transition.UP,
                                              up_cost))
                else:
                    self.array[i].append(Cell(self.array[i][-1],
                                              Transition.LEFT,
                                              left_cost))

    ###########################################
    # def banded_prep_array
    # Preps array by adding first row
    #
    # Time Complexity: O(k) Creates k cells, k = 4
    # Space Complexity: O(k) Stores k cells in list, k = 4
    ###########################################
    def banded_prep_array(self):
        # add first row to array
        self.array.append([])

        # temp cell
        tmp_cell = Cell(None, None, 0)

        # add first cell to array
        self.array[0].append(tmp_cell)

        # add remaining cells to row
        for j in range(1, 4):
            tmp_cell = Cell(tmp_cell, Transition.LEFT, j * 5)
            self.array[0].append(tmp_cell)

    ###########################################
    # def banded_algorithm
    # Sequences 2 strings
    #
    # Time Complexity: O(n * k) For each letter in string 1, visit 4 times, k = 4
    # Space Complexity: O(n * k) Makes and stores things in array of size n with 4 cells, k = 4
    ###########################################
    def banded_algorithm(self):

        # for each row (string 2)
        for i in range(1, self.string2_len + 1):

            # add another row to array
            self.array.append([])

            # for each column (string 1)
            for j in range(1, 5):

                if self.string1_len - i < 3 and j == 4:
                    continue
                if self.string1_len - i < 2 and j == 3:
                    continue
                if self.string1_len - i < 1 and j == 2:
                    continue
                if self.string1_len - i < 0 and j == 1:
                    continue

                # diagonal_index    = [i - 1]   [j - 1]
                # up_index          = [i - 1]   [j]
                # left_index        = [i]       [j - 1]

                # get up cost
                if j < 4:
                    up_cost = self.array[i - 1][j].cost + 5
                else:
                    up_cost = float("inf")

                # get left cost
                if len(self.array[i]) > 0:
                    left_cost = self.array[i][-1].cost + 5
                else:
                    left_cost = float("inf")

                if self.string1[j - 1 + (i - 1)] == self.string2[i - 1]:
                    strings_match = True
                else:
                    strings_match = False

                # get diagonal cost
                if strings_match:
                    # strings are the same, cost: -3
                    diagonal_cost = self.array[i - 1][j - 1].cost - 3
                else:
                    # strings are not the same, cost: +1
                    diagonal_cost = self.array[i - 1][j - 1].cost + 1

                # stores smallest parent
                if diagonal_cost <= up_cost and diagonal_cost <= left_cost:
                    if strings_match:
                        self.array[i].append(Cell(self.array[i - 1][j - 1],
                                                  Transition.DIAGONAL,
                                                  diagonal_cost))
                    else:
                        self.array[i].append(Cell(self.array[i - 1][j - 1],
                                                  Transition.DIAGONAL,
                                                  diagonal_cost))
                elif up_cost <= left_cost:
                    self.array[i].append(Cell(self.array[i - 1][j],
                                              Transition.UP,
                                              up_cost))
                else:
                    self.array[i].append(Cell(self.array[i][-1],
                                              Transition.LEFT,
                                              left_cost))

    ###########################################
    # def get_smallest_combination
    # returns smallest combination
    #
    # Time Complexity: O(n) visit n nodes and make a string
    # Space Complexity: O(n) saves a string at about n long
    ###########################################
    def get_combo_string(self):

        if self.score == float('inf'):
            return ["No Alignment Possible", "No Alignment Possible"]

        combo_string_a = ""
        combo_string_b = ""

        tmp_cell = self.array[self.string2_len][-1]
        string1_index = self.string1_len - 1
        string2_index = self.string2_len - 1

        while tmp_cell is not None:

            if tmp_cell.transition_type == Transition.UP:
                combo_string_a = "-" + combo_string_a
                combo_string_b = self.string2[string2_index] + combo_string_b
                string2_index -= 1

            elif tmp_cell.transition_type == Transition.LEFT:
                combo_string_a = self.string1[string1_index] + combo_string_a
                combo_string_b = "-" + combo_string_b
                string1_index -= 1

            elif tmp_cell.transition_type == Transition.DIAGONAL:
                combo_string_a = self.string1[string1_index] + combo_string_a
                combo_string_b = self.string2[string2_index] + combo_string_b
                string1_index -= 1
                string2_index -= 1

            tmp_cell = tmp_cell.parent

        return [combo_string_b[:100], combo_string_a[:100]]

    ###########################################
    # def get_score
    # returns the score
    #
    # Time Complexity: O(1) Just returns the score
    # Space Complexity: Not really applicable
    ###########################################
    def get_score(self):
        return self.array[self.string2_len][-1].cost
