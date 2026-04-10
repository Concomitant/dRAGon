# dRAGon - Proposed TODOs

## Bugs

### 1. Hardcoded index directory ignores config value
**Files:** `dragon/search.py:51`, `dragon/search.py:59`
**Severity:** High

`create_in("indexdir", schema)` and `open_dir("indexdir")` use a hardcoded `"indexdir"` string, even though `config["index_directory"]` is already used on line 42 to check whether the directory exists. If the config value is anything other than `"indexdir"`, the index will be created/opened from the wrong path.

```python
# Line 51 — should be:
ix = create_in(config["index_directory"], schema)

# Line 59 — should be:
ix = open_dir(config["index_directory"])
```

### 2. Duplicate instruction block in RAG prompt
**File:** `dragon/webapi.py:22-38`
**Severity:** Medium

The prompt template contains the same instruction paragraph twice ("Examine the following snippets..."). This wastes tokens on every LLM call and may confuse the model. The duplicate block (lines 33-37) should be removed.

### 3. `.gitignore` references wrong config path
**File:** `.gitignore:2`
**Severity:** Low

The entry `dRAGon/config/config.yml` uses a capital-D `dRAGon` but the actual directory on disk is lowercase `dragon`. This means the config file is **not** being ignored on case-sensitive filesystems (Linux). Should be `dragon/config/config.yml`.

### 4. README typos
**File:** `README.md:11,16`
**Severity:** Low

- Line 11: "stll" should be "still"
- Line 16: "net" should be "next"

---

## Code Quality

### 5. Remove debug print statements — use logging instead
**Files:** `dragon/search.py:16`, `dragon/search.py:20-21`
**Severity:** High

There are bare `print()` calls used for debugging (one even has a `# TODO: Remove` comment). These should be replaced with Python's `logging` module so output levels can be controlled in production vs. development.

### 6. Module-level side effects in `search.py`
**File:** `dragon/search.py:29-59`
**Severity:** Medium

Indexing (reading files, chunking, writing to Whoosh) happens at **import time** as top-level module code. This means:
- Importing `search` for testing triggers real I/O
- Errors during indexing crash the entire import with no recovery
- The index cannot be rebuilt without restarting the process

This logic should be wrapped in a function (e.g., `initialize_index()`) called explicitly at startup.

### 7. Empty `core.py` placeholder
**File:** `dragon/core.py`
**Severity:** Low

This file is completely empty. Either remove it or add the intended functionality.

### 8. Generic endpoint function name
**File:** `dragon/webapi.py:50`
**Severity:** Low

`read_item` is a leftover FastAPI tutorial name. Rename to something descriptive like `query_rulebook`.

---

## Missing Functionality

### 9. No tests
**Severity:** High

There are zero test files in the repository. At minimum, add:
- Unit tests for `search_rulebook()` (mocking the Whoosh index)
- Unit tests for the RAG chain (mocking the LLM)
- Integration test for the `/api/query` endpoint (using FastAPI's `TestClient`)

### 10. No example config file
**Severity:** Medium

`dragon/config/config.yml` is gitignored (as it should be — it may contain API keys), but there is no `config.yml.example` or `config.yml.template` showing required keys. New contributors have to read the source to figure out what config keys exist (`index_directory`, `rulebook_path`, `rpg_title`, `rpg_author`, and presumably `OPENAI_API_KEY`).

### 11. No input validation on queries
**File:** `dragon/webapi.py:50-53`
**Severity:** Medium

Empty or whitespace-only queries are passed straight through to Whoosh and the LLM. Add validation to reject trivially empty queries with a clear 400 response.

### 12. No error handling on the API endpoint
**File:** `dragon/webapi.py:50-53`
**Severity:** Medium

If the LLM call or search fails (network error, rate limit, bad index), the user gets a raw 500 Internal Server Error. Add try/except with meaningful error responses.

### 13. No Dockerfile or deployment configuration
**Severity:** Medium

There is no Dockerfile, `docker-compose.yml`, or any deployment configuration. For reproducibility and the stated "autodragon" long-term goals, containerization would help.

### 14. No CI/CD pipeline
**Severity:** Medium

No GitHub Actions, no linting, no automated test runs. Adding a basic CI workflow (lint + test) would prevent regressions.

---

## Configuration & Dependencies

### 15. Hardcoded magic numbers should be configurable
**Files:** `dragon/search.py:31-32`, `dragon/webapi.py:17`
**Severity:** Medium

These values are embedded directly in the code and would benefit from being in `config.yml`:
- `chunk_size=300` (search.py:31)
- `chunk_overlap=50` (search.py:32)
- `temperature=0.7` (webapi.py:17)

### 16. Pinned dependencies are stale
**File:** `requirements.txt`
**Severity:** Low

All dependencies are pinned to early-2024 versions. Notable: `langchain==0.2.5` and `openai==1.34.0` are several major versions behind. Consider updating, or at minimum add a `Dependabot` or `Renovate` config to track updates.

---

## Summary

| #  | Title                                      | Severity | Type          |
|----|--------------------------------------------|----------|---------------|
| 1  | Hardcoded index directory ignores config   | High     | Bug           |
| 2  | Duplicate instruction in RAG prompt        | Medium   | Bug           |
| 3  | `.gitignore` references wrong path         | Low      | Bug           |
| 4  | README typos                               | Low      | Bug           |
| 5  | Debug prints — use logging                 | High     | Code Quality  |
| 6  | Module-level side effects in search.py     | Medium   | Code Quality  |
| 7  | Empty `core.py` placeholder                | Low      | Code Quality  |
| 8  | Generic endpoint function name             | Low      | Code Quality  |
| 9  | No tests                                   | High     | Missing       |
| 10 | No example config file                     | Medium   | Missing       |
| 11 | No input validation on queries             | Medium   | Missing       |
| 12 | No error handling on API endpoint          | Medium   | Missing       |
| 13 | No Dockerfile or deployment config         | Medium   | Missing       |
| 14 | No CI/CD pipeline                          | Medium   | Missing       |
| 15 | Hardcoded magic numbers                    | Medium   | Config        |
| 16 | Pinned dependencies are stale              | Low      | Config        |
