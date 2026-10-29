"""Demo lessons and the rule-based adaptation algorithm for AdaptLearn AI."""

LEVELS = ["Beginner", "Intermediate", "Advanced"]


def adapt_level(current_level: int, correct: int, total: int) -> tuple[int, str]:
    """Move down at <=40%, up at 100%, otherwise continue practicing.

    With five quiz questions: 0-2 correct -> simpler; 3-4 -> same; 5 -> harder.
    The level is capped to the supported Beginner/Intermediate/Advanced range.
    """
    if total <= 0 or not 0 <= correct <= total:
        raise ValueError("Invalid quiz score")
    if correct / total <= 0.40:
        return max(0, current_level - 1), "You need more practice. Let's simplify the next explanation."
    if correct == total:
        return min(2, current_level + 1), "Excellent! Let's try a more challenging lesson."
    return current_level, "Good progress. Let's practice this level with fresh examples."


def _q(question, choices, answer, explanation):
    return {"question": question, "options": choices, "correct_index": answer, "explanation": explanation}


DEMO = {
    0: {
        "title": "Linked Lists — Beginner",
        "overview": "A linked list stores items in separate nodes. Each node contains data and a link (reference) to the next node. Think of it as a treasure hunt: each clue tells you where the next clue is.",
        "key_points": [
            "Each node contains data and a pointer/reference to the next node.",
            "The first node is called the head.",
            "The last node's next reference is NULL (or None in Python).",
            "Unlike arrays, nodes do not need to be next to one another in memory.",
        ],
        "worked_example": "Imagine three nodes: 10 → 20 → 30 → NULL. The head points to 10. Follow each arrow to visit all nodes.",
        "quiz": [
            _q("What does a linked-list node contain?", ["Only an index", "Data and a reference", "Only a value", "A row and column"], 1, "A node stores data plus a link to another node."),
            _q("What is the first node called?", ["Tail", "Root", "Head", "Leaf"], 2, "Head refers to the first node."),
            _q("What does the last node point to in a singly linked list?", ["Head", "NULL/None", "Middle node", "The array"], 1, "The last node has no successor."),
            _q("Do linked-list nodes need contiguous memory locations?", ["Always", "Only in Python", "No", "Only in C"], 2, "References connect nodes stored at different memory addresses."),
            _q("Which shows a three-node singly linked list?", ["10, 20, 30 inside one cell", "10 → 20 → 30 → NULL", "10 ↔ 20 ↔ 30 → 10", "10 + 20 + 30"], 1, "Arrows show the next-node links."),
        ],
    },
    1: {
        "title": "Linked Lists — Intermediate",
        "overview": "Singly linked lists support traversal, insertion, and deletion by changing node references. To insert after a given node, link the new node to its successor before linking the current node to the new node.",
        "key_points": [
            "To insert at the head: new.next = head, then head = new.",
            "To delete the head: head = head.next, after handling an empty list.",
            "To find a value: visit nodes one by one until a match or NULL.",
            "Search is O(n); insertion at the known head is O(1).",
        ],
        "worked_example": "Insert 15 after 10 in 10 → 20 → 30: set new(15).next to 20; then set 10.next to 15. Result: 10 → 15 → 20 → 30.",
        "quiz": [
            _q("What is the time complexity of searching an unsorted singly linked list?", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2, "In the worst case every node is visited."),
            _q("Which assignment should happen first when inserting after node p?", ["p.next = new", "new.next = p.next", "head = NULL", "delete p"], 1, "Set new.next first to preserve the remainder of the list."),
            _q("Which operation is O(1) when the head pointer is known?", ["Searching all nodes", "Insert at head", "Find the tail", "Sort the list"], 1, "Inserting at head modifies a constant number of references."),
            _q("To delete the first node of a nonempty list, what is the updated head?", ["head.next", "NULL always", "head.next.next always", "Previous node"], 0, "Move the head to the second node."),
            _q("Which pointer must be checked before accessing head.next?", ["Tail", "Head for NULL", "Integer length", "Array index"], 1, "If head is NULL, accessing head.next is invalid."),
        ],
    },
    2: {
        "title": "Linked Lists — Advanced",
        "overview": "Advanced linked-list problems often involve two-pointer techniques, invariant preservation, and edge cases. Favor O(1) extra memory where possible and explain pointer operations precisely.",
        "key_points": [
            "Floyd's tortoise-and-hare algorithm detects cycles in O(n) time and O(1) space.",
            "Reversing a singly linked list iteratively uses prev, current, and next pointers.",
            "A dummy node simplifies deletion and insertion near the head.",
            "For every pointer update, preserve access to the remaining nodes before overwriting a link.",
        ],
        "worked_example": "Reverse 1 → 2 → 3 → NULL: for each node, store next, point current.next to prev, then advance prev and current. Final head is 3: 3 → 2 → 1 → NULL.",
        "quiz": [
            _q("What is the extra space complexity of Floyd's cycle-detection algorithm?", ["O(n)", "O(log n)", "O(1)", "O(n²)"], 2, "Only two pointers are used."),
            _q("Which pointers are typically used for in-place iterative reversal?", ["left and right indexes", "prev, curr, next", "parent and child", "root and leaf"], 1, "Three references preserve and reverse links safely."),
            _q("What is the main purpose of a dummy/sentinel head?", ["Double the list length", "Simplify head-related edge cases", "Make searches O(1)", "Detect cycles automatically"], 1, "A dummy node provides a uniform predecessor for updates."),
            _q("Why save curr.next before reversal updates?", ["To sort the nodes", "To avoid losing the rest of the list", "To allocate an array", "To detect duplicates"], 1, "Overwriting curr.next otherwise loses access to subsequent nodes."),
            _q("What is the worst-case time complexity for reversing n nodes?", ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2, "Each node is processed once."),
        ],
    },
}


def demo_lesson(topic: str, level: int) -> dict:
    if topic.strip().casefold() not in {"linked lists", "linked list", "singly linked list", "singly linked lists"}:
        raise ValueError("Offline demo is available for Linked Lists only. Choose 'Linked Lists' or enable the Gemini API.")
    return DEMO[level]


def validate_lesson(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("The AI returned an invalid lesson structure")
    for key in ["title", "overview", "worked_example"]:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"Missing lesson field: {key}")
    if not isinstance(data.get("key_points"), list) or not (2 <= len(data["key_points"]) <= 8):
        raise ValueError("Expected 2–8 key points")
    if not isinstance(data.get("quiz"), list) or len(data["quiz"]) != 5:
        raise ValueError("Expected exactly five quiz questions")
    for i, q in enumerate(data["quiz"]):
        if (not isinstance(q, dict) or not isinstance(q.get("question"), str)
                or not isinstance(q.get("options"), list) or len(q["options"]) != 4
                or any(not isinstance(x, str) or not x.strip() for x in q["options"])
                or type(q.get("correct_index")) is not int
                or not 0 <= q["correct_index"] <= 3
                or not isinstance(q.get("explanation"), str)):
            raise ValueError(f"Invalid generated quiz question #{i+1}")
    return data
