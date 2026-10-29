"""Basic offline tests. Run: python smoke_test.py"""
from engine import LEVELS, demo_lesson, validate_lesson, adapt_level
for level in range(3):
    lesson = validate_lesson(demo_lesson("Linked Lists", level))
    assert len(lesson["quiz"]) == 5
    print("Valid:", LEVELS[level], "-", lesson["title"])
assert adapt_level(1, 1, 5)[0] == 0
assert adapt_level(1, 4, 5)[0] == 1
assert adapt_level(1, 5, 5)[0] == 2
assert adapt_level(0, 0, 5)[0] == 0
assert adapt_level(2, 5, 5)[0] == 2
print("All tests passed.")
