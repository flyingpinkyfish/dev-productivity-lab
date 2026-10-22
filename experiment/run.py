"""Randomized task runner for the AI-allowed vs AI-off experiment."""

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

PLAN = Path(__file__).parent / "plan.json"

TASKS = [
    "/reverse?text= returns the text reversed",
    "/palindrome?text= returns true or false",
    "/max?a=&b= returns the larger integer",
    "/min?a=&b= returns the smaller integer",
    "/square?n= returns n times n",
    "/is_even?n= returns true or false",
    "/upper?text= returns the text in capitals",
    "/lower?text= returns the text in lowercase",
    "/length?text= returns the number of characters",
    "/vowels?text= returns the number of vowels",
    "/abs?n= returns the absolute value",
    "/cube?n= returns n times n times n",
    "/concat?a=&b= returns the two texts joined",
    "/first_char?text= returns the first character",
    "/double?n= returns n times 2",
    "/negate?n= returns minus n",
]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load():
    return json.loads(PLAN.read_text())


def save(plan):
    PLAN.write_text(json.dumps(plan, indent=2))


def init():
    if PLAN.exists():
        sys.exit("plan.json already exists; not overwriting it")
    tasks = TASKS[:]
    random.shuffle(tasks)
    groups = ["AI-allowed", "AI-off"] * (len(tasks) // 2)
    random.shuffle(groups)
    plan = []
    for i, (task, group) in enumerate(zip(tasks, groups)):
        plan.append(
            {
                "n": i + 1,
                "task": task,
                "group": group,
                "predicted_minutes": None,
                "start": None,
                "end": None,
                "felt_speed": None,
            }
        )
    save(plan)
    print(f"Created a plan with {len(plan)} tasks. Do not open plan.json.")


def start():
    plan = load()
    if any(p["start"] and not p["end"] for p in plan):
        sys.exit("A task is still open. Run finish first.")
    todo = [p for p in plan if not p["start"]]
    if not todo:
        sys.exit("All tasks are done.")
    item = todo[0]
    print(f"Task {item['n']} of {len(plan)}: add {item['task']}, with a test")
    print(f"Group: {item['group']}")
    item["predicted_minutes"] = int(input("Predicted minutes to finish: "))
    item["start"] = now()
    save(plan)
    print("Clock started.")


def finish():
    plan = load()
    open_items = [p for p in plan if p["start"] and not p["end"]]
    if not open_items:
        sys.exit("No open task. Run start first.")
    item = open_items[0]
    item["end"] = now()
    item["felt_speed"] = int(input("How fast did it feel, 1 (slow) to 5 (fast): "))
    save(plan)
    begin = datetime.fromisoformat(item["start"])
    end = datetime.fromisoformat(item["end"])
    minutes = (end - begin).total_seconds() / 60
    print(f"Task {item['n']} took {minutes:.0f} minutes.")


def status():
    plan = load()
    done = [p for p in plan if p["end"]]
    print(f"{len(done)} of {len(plan)} tasks finished.")


COMMANDS = {"init": init, "start": start, "finish": finish, "status": status}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        sys.exit("usage: python experiment/run.py [init|start|finish|status]")
    COMMANDS[sys.argv[1]]()
