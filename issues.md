# Static analysis issue table

The source locations below refer to the assigned repository's original
`dairy_collection.py` (the exact baseline is preserved in `baseline/`).
Findings were confirmed by inspecting the source. The original handout asks
students to run the tools, but contains no separate issue-code rubric.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection | High security (Bandit B605) | 31 | `os.system` concatenates a farmer-controlled value into a shell command. | Remove shell execution and print a plain message. |
| Weak MD5 digest | High security (Bandit B324) | 16 | MD5 is unsuitable for security-sensitive identifiers and flagged by Bandit. | Use SHA-256 for the stable demonstration token. |
| SQL injection | Medium security (Bandit B608) | 11 | Farmer and day values are interpolated into SQL text. Quotes can break the query or alter its meaning. | Use SQLite placeholders and bound parameters. |
| Empty-ledger crash | Bug | 26 | `max()` raises `ValueError` when there are no milk records. | Return `None` when the query has no rows. |
| SQL data loss on quoted names | Bug | 11 | A valid farmer name containing an apostrophe can break the interpolated insert. | Parameterized insertion preserves the literal name. |
| Missing-day total is not explicitly handled | Bug | 21 | Empty results happen to sum to zero, but the code does not express that case in SQL. | Use `COALESCE(SUM(...), 0)` and keep the formatted zero result. |
| Public functions use mixed-case names and lack contracts | Maintainability | 10-36 | Names are not idiomatic snake_case and inputs/outputs are undocumented. | Rename functions and add docstrings and type annotations. |
| Main executes on import | Maintainability | 39-47 | Importing the module unexpectedly writes sample data and prints output. | Add the standard `if __name__ == "__main__"` guard. |
| Equality check against `None` | Style | 36 | `fat == None` is not the recommended identity check. | Use `fat is None`. |
| Unused import | Style | 2 | `json` is imported but never used. | Remove the import. |

The final source addresses all rows above. The final before/after analyzer
outputs are in `reports/before/` and `reports/after/`.
