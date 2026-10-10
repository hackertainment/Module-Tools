from typing import Iterable, Optional

class ImmutableNumberList:
    # We accept any `Iterable[int]` here, so can construct with a list, a set, or anything else that can be iterated.
    def __init__(self, elements: Iterable[int]):
        # We copy the elements so that if someone mutates the passed in elements list, our copy won't be mutated.
        self.elements = [element for element in elements]

    def first(self) -> Optional[int]:
        if not self.elements:
            return None
        return self.elements[0]

    def last(self) -> Optional[int]:
        if not self.elements:
            return None
        return self.elements[-1]

    def length(self) -> int:
        return len(self.elements)

    def largest(self) -> Optional[int]:
        # To find the largest element, we need to go through the entire list (which may take some time).
        if not self.elements:
            return None
        largest = self.elements[0]
        for element in self.elements:
            if element > largest:
                largest = element
        return largest


# A SortedImmutableNumberList is the same as an ImmutableNumberList,
# but it changes some aspects.
class SortedImmutableNumberList(ImmutableNumberList):
    def __init__(self, elements: Iterable[int]):
        # We do extra work here when constructing the list,
        # to make sure the elements are sorted.
        # This takes more time than the ImmutableNumberList version would.
        super().__init__(sorted(elements))

    # This method overrides (replaces) the method with the same name on the super-class.
    def largest(self) -> Optional[int]:
        # Because we know the elements were already sorted in the constructor,
        # we can implement finding the largest number faster.
        # We don't need to look through every element - we know the largest element is at the end.
        # Because we did extra work one time before (in the constructor),
        # we can avoid re-doing that work every time someone calls `largest()`.
        return self.last()

    def max_gap_between_values(self) -> Optional[int]:
        if not self.elements:
            return None
        previous_element = None
        max_gap = -1
        for element in self.elements:
            if previous_element is not None:
                gap = element - previous_element
                if gap > max_gap:
                    max_gap = gap
            previous_element = element
        return max_gap


values = SortedImmutableNumberList([1, 19, 7, 13, 4])
print(values.largest())
print(values.max_gap_between_values())

unsorted_values = ImmutableNumberList([1, 19, 7, 13, 4])
print(unsorted_values.largest())
print(unsorted_values.max_gap_between_values())  # This doesn't work - the superclass doesn't define this method.


# TASK 15
# Try using this code and make sure you understand how it works and what it does
#
# Answer the following questions, writing your answers in the file, before checking the answers.
#
# Q1: If you know in advance you need to frequently access the largest item of the list, which class will be more efficient and why?
#     `SortedImmutableNumberList` because we need to go through the entire list (which may take some time) to find the largest element in `ImmutableNumberList` version.
# Q2: If you know in advance you will be initialising many of them repeatedly, which class will be more efficient and why?
#     `ImmutableNumberList` because no extra work to make sure the elements are sorted when constructing the list which takes less time than the `SortedImmutableNumberList` version would.
