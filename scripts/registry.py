"""Registry: which school years and subjects exist, and which of them already have worksheets.

This is the single source for both the generator and the website (the site reads it through topics.catalog()).
Adding a subject = add it here, write a module with the topic interface (see ARCHITECTURE.md), add its names
to i18n.REG. Nothing in site/index.html has to change.

Years follow the National Curriculum for England (Reception, Year 1 ... Year 11). For Ukrainian families every
year also has the nearest Ukrainian class by age: UK Year 2 (ages 6-7) ~ Ukrainian class 1.
"""

# id, ages, nearest Ukrainian class (0 = preschool)
YEARS = (
    ("R", "4–5", 0), ("Y1", "5–6", 0), ("Y2", "6–7", 1), ("Y3", "7–8", 2), ("Y4", "8–9", 3), ("Y5", "9–10", 4),
    ("Y6", "10–11", 5), ("Y7", "11–12", 6), ("Y8", "12–13", 7), ("Y9", "13–14", 8), ("Y10", "14–15", 9), ("Y11", "15–16", 10),
)
YEAR_IDS = tuple(y for y, _, _ in YEARS)


def years(first, last):
    """Years from first to last, inclusive: years("R", "Y6")."""
    return YEAR_IDS[YEAR_IDS.index(first):YEAR_IDS.index(last) + 1]


# Subjects change with age, like a real school: maths splits into algebra and geometry from Year 8
# (Ukrainian class 7); science splits into physics, chemistry and biology from Year 7.
# "ready": years that already have worksheets. "module": the Python module with the topics of this subject.
# "prefix": topic ids of the subject start with it (maths keeps its old ids r*, y*, v*, so old links still work).
SUBJECTS = (
    {"id": "maths", "years": years("R", "Y7"), "ready": ("R", "Y1", "Y2"), "module": "topics", "prefix": ""},
    {"id": "algebra", "years": years("Y8", "Y11"), "ready": (), "module": None, "prefix": "al"},
    {"id": "geometry", "years": years("Y8", "Y11"), "ready": (), "module": None, "prefix": "gm"},
    {"id": "languages", "years": years("R", "Y11"), "ready": (), "module": None, "prefix": "la"},
    {"id": "nature", "years": years("R", "Y6"), "ready": (), "module": None, "prefix": "nt"},
    {"id": "physics", "years": years("Y7", "Y11"), "ready": (), "module": None, "prefix": "ph"},
    {"id": "chemistry", "years": years("Y7", "Y11"), "ready": (), "module": None, "prefix": "ch"},
    {"id": "biology", "years": years("Y7", "Y11"), "ready": (), "module": None, "prefix": "bi"},
    {"id": "society", "years": years("R", "Y6"), "ready": (), "module": None, "prefix": "so"},
    {"id": "geography", "years": years("Y7", "Y11"), "ready": (), "module": None, "prefix": "ge"},
    {"id": "history", "years": years("Y7", "Y11"), "ready": (), "module": None, "prefix": "hi"},
)
SUBJECT = {s["id"]: s for s in SUBJECTS}
MATHS_ID_START = ("r", "y", "v")  # maths topic ids; prefixes of other subjects must not start with these letters


def subjects_for(year):
    """Subjects taught in a year, in the registry order: [(id, "ready" | "soon")]."""
    return [(s["id"], "ready" if year in s["ready"] else "soon") for s in SUBJECTS if year in s["years"]]


def ready(year, subject):
    return year in SUBJECT[subject]["ready"]


def subject_of_id(tid):
    """The subject a topic id belongs to."""
    for s in SUBJECTS:
        if s["prefix"] and tid.startswith(s["prefix"]):
            return s["id"]
    return "maths"


def subject_of(ids):
    """The one subject of a list of topic ids (a worksheet has exactly one subject)."""
    found = {subject_of_id(t) for t in ids}
    if len(found) != 1:
        raise ValueError("a worksheet has topics of one subject only")
    return found.pop()


def check():
    """Consistency of the registry itself."""
    assert len(set(YEAR_IDS)) == len(YEAR_IDS)
    for s in SUBJECTS:
        assert set(s["ready"]) <= set(s["years"]), s["id"]
        assert not s["ready"] or s["module"], f'{s["id"]}: ready years need a module'
        assert s["id"] == "maths" or (len(s["prefix"]) == 2 and not s["prefix"].startswith(MATHS_ID_START)), s["id"]
    prefixes = [s["prefix"] for s in SUBJECTS if s["prefix"]]
    assert len(prefixes) == len(set(prefixes))
    for y in YEAR_IDS:
        assert subjects_for(y), f"{y}: no subjects"
    return True


if __name__ == "__main__":
    check()
    for y, age, ua in YEARS:
        print(f"{y:4} {age:6} UA {ua or 'preschool':>9}  " + ", ".join(f"{s}{'' if st == 'ready' else '*'}" for s, st in subjects_for(y)))
    print("(* = soon)")
