"""Exhaustively compare parity classes through every proper coordinate view."""

from collections import Counter
from itertools import combinations, product


N = 6
words = list(product((0, 1), repeat=N))
even_words = [word for word in words if sum(word) % 2 == 0]
odd_words = [word for word in words if sum(word) % 2 == 1]

assert len(words) == 2**N
assert len(even_words) == len(odd_words) == 2 ** (N - 1)

proper_coordinate_subsets = 0
histogram_cells_compared = 0
projection_differences = 0

for visible_count in range(N):
    patterns = tuple(product((0, 1), repeat=visible_count))
    expected_count = 2 ** (N - visible_count - 1)

    for visible_coordinates in combinations(range(N), visible_count):
        proper_coordinate_subsets += 1
        even_projection = Counter(
            tuple(word[i] for i in visible_coordinates) for word in even_words
        )
        odd_projection = Counter(
            tuple(word[i] for i in visible_coordinates) for word in odd_words
        )
        expected = {pattern: expected_count for pattern in patterns}
        histogram_cells_compared += len(expected)
        projection_differences += sum(
            even_projection[pattern] != odd_projection[pattern]
            for pattern in expected
        )
        assert even_projection == expected
        assert odd_projection == expected

even_full = Counter(even_words)
odd_full = Counter(odd_words)
full_assignment_differences = sum(
    even_full[word] != odd_full[word] for word in words
)
assert proper_coordinate_subsets == 2**N - 1
assert histogram_cells_compared == 665
assert projection_differences == 0
assert full_assignment_differences == 2**N

print(f"N={N} assignments={len(words)}")
print(f"parity classes: even={len(even_words)} odd={len(odd_words)}")
print(f"proper coordinate subsets checked={proper_coordinate_subsets}")
print(
    f"projected histogram cells compared={histogram_cells_compared} "
    f"differences={projection_differences}"
)
print(
    f"full-assignment cells compared={len(words)} "
    f"differences={full_assignment_differences}"
)
