"""Check equal parity marginals beside revealing linked first/last-five views.

This finite exhibit enumerates all six-bit words. It makes no claim about
real-world populations or linkage systems.
"""

from collections import Counter
from itertools import product
import random


_WIDTH = 6


def _parity(word: str) -> int:
    return sum(bit == "1" for bit in word) % 2


def check_linked_views() -> dict[str, int]:
    """Return focused counts, raising if the six-bit construction disagrees."""
    words = ["".join(bits) for bits in product("01", repeat=_WIDTH)]
    classes = {
        parity: [word for word in words if _parity(word) == parity]
        for parity in (0, 1)
    }
    assert len(classes[0]) == len(classes[1]) == 32

    all_patterns = {
        "".join(bits) for bits in product("01", repeat=_WIDTH - 1)
    }
    histogram_cells = 0
    histogram_differences = 0
    views = {
        "first five": lambda word: word[:5],
        "last five": lambda word: word[1:],
    }

    for project in views.values():
        histograms = {
            parity: Counter(project(word) for word in class_words)
            for parity, class_words in classes.items()
        }
        for pattern in all_patterns:
            histogram_cells += 1
            even_count = histograms[0][pattern]
            odd_count = histograms[1][pattern]
            histogram_differences += even_count != odd_count
            assert even_count == odd_count == 1

    shuffled_words = words.copy()
    random.Random(90421).shuffle(shuffled_words)
    sample_ids = {
        word: f"sample-{index:02d}"
        for index, word in enumerate(shuffled_words)
    }

    linked_rows = 0
    exact_reconstructions = 0
    parity_errors = 0
    joint_supports: dict[int, set[tuple[str, str]]] = {0: set(), 1: set()}

    for parity, class_words in classes.items():
        first_view = {
            sample_ids[word]: word[:5]
            for word in class_words
        }
        last_view = {
            sample_ids[word]: word[1:]
            for word in class_words
        }
        original_by_id = {
            sample_ids[word]: word
            for word in class_words
        }
        for sample_id, first_five in first_view.items():
            last_five = last_view[sample_id]
            linked_rows += 1
            assert first_five[1:] == last_five[:-1]
            recovered = first_five + last_five[-1]
            original = original_by_id[sample_id]
            exact_reconstructions += recovered == original
            parity_errors += _parity(recovered) != parity
            assert recovered == original
            assert _parity(recovered) == parity
            joint_supports[parity].add((first_five, last_five))

    joint_support_overlap = len(joint_supports[0] & joint_supports[1])
    assert histogram_cells == 64
    assert histogram_differences == 0
    assert linked_rows == exact_reconstructions == 64
    assert parity_errors == 0
    assert joint_support_overlap == 0

    return {
        "assignments": len(words),
        "even_class": len(classes[0]),
        "odd_class": len(classes[1]),
        "single_view_histogram_cells": histogram_cells,
        "histogram_differences": histogram_differences,
        "linked_rows": linked_rows,
        "exact_reconstructions": exact_reconstructions,
        "parity_errors": parity_errors,
        "joint_support_overlap": joint_support_overlap,
    }


def main() -> None:
    counts = check_linked_views()
    print(
        f"N={_WIDTH} assignments={counts['assignments']} "
        f"parity classes={counts['even_class']},{counts['odd_class']}"
    )
    print(
        "single-view histogram cells="
        f"{counts['single_view_histogram_cells']} "
        f"differences={counts['histogram_differences']}"
    )
    print(
        f"linked rows={counts['linked_rows']} "
        f"exact reconstructions={counts['exact_reconstructions']} "
        f"parity errors={counts['parity_errors']}"
    )
    print(f"linked-pair support overlap={counts['joint_support_overlap']}")


if __name__ == "__main__":
    main()
