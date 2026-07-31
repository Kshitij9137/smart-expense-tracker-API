# AI Notes

## Tools Used
[e.g. Claude, ChatGPT — name what you actually used]

## 1. What was AI-generated vs. written by me

- **AI-generated (with my review/edits):** [e.g. FastAPI route structure in src/main.py, 
  Pydantic models in src/models.py, initial pytest test cases in tests/test_api.py]
- **Written/decided by me:** [e.g. the decision to split storage logic into its own 
  module rather than inline in main.py, the case-insensitive category matching, 
  README content and structure]

## 2. What I validated, tested, or changed, and why

- [Specific example, e.g.: "AI's first draft of get_total() didn't round the result — 
  I added round(x, 2) after noticing floating point sums like 19.999999999998 in manual 
  testing via /docs. Currency values should never look like that."]
- [Another specific example, e.g.: "Verified every endpoint manually via /docs before 
  writing automated tests, to make sure I understood what each one actually returned."]
- [Another, e.g.: "Ran the full test suite and the README install steps on a fresh 
  git clone to confirm they work exactly as documented, not just on my machine."]

## 3. AI suggestions I didn't use, and why

- [Specific example, e.g.: "AI suggested adding SQLite for persistence. I chose not to, 
  since the assignment explicitly allows in-memory storage and adding a DB would increase 
  complexity without meeting a stated requirement."]
- [Another, e.g.: "AI suggested a separate route like /expenses/category/{category} for 
  filtering. I used a query parameter (?category=) instead, since filtering is a property 
  of the existing resource, not a new one — more consistent with REST conventions."]