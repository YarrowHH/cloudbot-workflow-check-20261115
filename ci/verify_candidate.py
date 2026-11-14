import importlib.util
from pathlib import Path

module_path = Path(__file__).resolve().parents[1] / "src" / "status_summary.py"
spec = importlib.util.spec_from_file_location("status_summary", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cases = [([], {"total": 0, "passed": 0, "failed": 0, "pending": 0}),
         (["passed", "failed", "passed", "pending"], {"total": 4, "passed": 2, "failed": 1, "pending": 1}),
         (["pending"], {"total": 1, "passed": 0, "failed": 0, "pending": 1})]
for items, expected in cases:
    before = list(items)
    actual = module.summarize(items)
    assert actual == expected, (items, actual, expected)
    assert items == before, "Input was mutated"
for invalid in [["unknown"], [1], [None], ["passed", "FAILED"], [[]], [{}], None, "passed", 3, {}]:
    try:
        module.summarize(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid status accepted")
print("Synthetic status-summary contract verified")
