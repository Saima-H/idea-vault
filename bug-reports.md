# Bug Reports - Idea Vault

## Bug 1: App fails silently when the backend server is offline
**ID:** BUG-01
**Severity:** High
**Priority:** P1
**Environment:** Windows 11, Chrome Browser, Next.js (localhost:3000)
**Steps to Reproduce:**
1. Make sure the FastAPI backend is stopped (Ctrl+C in the backend terminal).
2. Open the frontend UI at `http://localhost:3000`.
3. Try to add a new idea by typing text and clicking "Save Idea".
4. Open the browser DevTools (F12) -> Console tab.
**Expected Result:** The UI should show a user-friendly error message like "Cannot connect to server. Please try again later."
**Actual Result:** The page silently fails. The idea does not appear, the form does not clear, and the only indication of failure is a red `TypeError: Failed to fetch` inside the browser console.
**Screenshot:** [Insert a screenshot of the browser console showing the error]

<img width="1279" height="679" alt="image" src="https://github.com/user-attachments/assets/759bd852-47ab-4b60-81bc-bc12fbb555f1" />

---

## Bug 2: API allows submission of empty spaces
**ID:** BUG-02
**Severity:** Medium
**Priority:** P2
**Environment:** Postman / FastAPI Backend
**Steps to Reproduce:**
1. Open Postman.
2. Send a `POST` request to `http://127.0.0.1:8000/ideas`.
3. Set the body to raw JSON: `{"content": "   "}` (just spaces).
4. Click Send.
**Expected Result:** The API should reject the request with a `422 Unprocessable Entity` because the content is effectively empty.
**Actual Result:** The API returns `200 OK` and saves an idea with just blank spaces. This clutters the database with empty rows.
**Screenshot:** [Insert a screenshot of Postman returning 200 OK for spaces]
<img width="1278" height="673" alt="image" src="https://github.com/user-attachments/assets/300d00c0-ca41-4afc-b31b-854943ec2082" />

---

## Bug 3: Invalid URL crashes the Pydantic validation
**ID:** BUG-03
**Severity:** Medium
**Priority:** P2
**Environment:** FastAPI Backend (Swagger UI)
**Steps to Reproduce:**
1. Go to `http://127.0.0.1:8000/docs`.
2. Open `POST /ideas` and click "Try it out".
3. Enter the body: `{"content": "Test", "url": "not-a-real-url"}`.
4. Click Execute.
**Expected Result:** The API should either save it as a string or return a clean validation error.
**Actual Result:** If we upgrade to a strict Pydantic URL type later, this will crash. Currently, the API blindly accepts "not-a-real-url" and saves it. When the frontend tries to render the link, it prepends the localhost domain (e.g., `http://localhost:3000/not-a-real-url`), creating a broken link.
**Screenshot:** [Insert a screenshot of the broken link in the UI]
<img width="1278" height="673" alt="image" src="https://github.com/user-attachments/assets/51d43188-11bf-4fec-a4bd-abeb54c95e1f" />
<img width="640" height="319" alt="image" src="https://github.com/user-attachments/assets/3a5f9728-f11d-4311-be50-7fb391e43240" />

---

## Bug 4: Smart Tags generate duplicates in edge cases
**ID:** BUG-04
**Severity:** Low
**Priority:** P3
**Environment:** FastAPI Backend (main.py Mock NLP logic)
**Steps to Reproduce:**
1. Add an idea with the text: "Build an app to build apps". 
2. Look at the generated tags.
**Expected Result:** The tags should be unique (e.g., `#side-project`).
**Actual Result:** Because the mock NLP checks `if "app" in text` and `if "build" in text`, the word "build" triggers the `side-project` tag, and "app" *also* triggers the `side-project` tag. (Note: This is prevented by the current `generated_tags` list logic, but if the logic is refactored to append blindly, it will generate duplicate `#side-project` tags).
**Screenshot:** [Insert screenshot if applicable]
<img width="631" height="320" alt="image" src="https://github.com/user-attachments/assets/47930c18-b6cd-4e25-98b6-73a3e416cb3f" />
<img width="1278" height="632" alt="image" src="https://github.com/user-attachments/assets/5808e645-da8b-4590-a61c-0c94c3bda8c5" />

If you look at your original main.py code, it actually had this line:

python
tags_string = ", ".join(generated_tags[:3])
Because generated_tags was a Python List, and you only appended "side-project" once (the if statements run sequentially, but "build" and "app" just add to the same if block, they don't add it twice), it naturally didn't duplicate the tag.

So you are right—it wasn't actually a bug in the code! However, in QA, you still document edge cases like this to prove to the reviewer that you tested it and verified it works. You can update your bug-reports.md to say: "Tested: Duplicate tags did not generate as the logic correctly only appends once per keyword category."



---

## Bug 5: CORS error when accessing from a different port
**ID:** BUG-05
**Severity:** Critical
**Priority:** P0
**Environment:** Next.js Frontend (Port 3000) & FastAPI Backend (Port 8000)
**Steps to Reproduce:**
1. Run the frontend on port 3000.
2. Run the backend on port 8000.
3. Try to fetch data from the frontend without CORS middleware.
**Expected Result:** The frontend should fetch the data and display it.
**Actual Result:** The browser blocks the request with a CORS policy error: `Access to fetch at 'http://127.0.0.1:8000/ideas' from origin 'http://localhost:3000' has been blocked by CORS policy`. 
**Fix Applied:** We imported `CORSMiddleware` in `main.py` and added `allow_origins=["http://localhost:3000"]`. (Documented in AI_JOURNAL.md).
**Screenshot:** [Insert a screenshot of the CORS error in the Chrome console]
