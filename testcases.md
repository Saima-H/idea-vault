# Test Cases for Idea Vault

## 1. UI & Form Validation
| ID | Test Scenario | Steps to Reproduce | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC-01 | Submit a valid text-only idea | 1. Go to UI<br>2. Enter "Build a habit tracker" in textbox<br>3. Click Save | Idea appears in list. Tags auto-generate. Form clears. | High |
| TC-02 | Submit text + valid URL | 1. Enter "My Github"<br>2. Enter `https://github.com`<br>3. Click Save | Idea appears. URL is clickable and opens in new tab. | High |
| TC-03 | Submit completely empty form | 1. Leave textbox blank<br>2. Click Save | "Save Idea" button does nothing. HTML5 validation blocks it. | High |
| TC-04 | Submit an idea with only spaces | 1. Enter "   " (spaces)<br>2. Click Save | Form does not submit (treated as empty). | Medium |
| TC-05 | Submit invalid URL format | 1. Enter content<br>2. Enter "justtext" in URL field<br>3. Click Save | Browser validation blocks submission, asking for a valid URL. | High |
| TC-06 | Submit extremely long text | 1. Enter 5,000 characters<br>2. Click Save | Idea saves successfully. UI text wraps correctly (no overflow). | Medium |
| TC-07 | Submit XSS script injection | 1. Enter `<script>alert('hack')</script>`<br>2. Click Save | App displays the text safely. Does NOT execute the script. | Critical |
| TC-08 | Submit emojis | 1. Enter "🚀 Build an app 🔥"<br>2. Click Save | Emojis save and display correctly. | Low |
| TC-09 | Submit special characters | 1. Enter "!@#$%^&*()"<br>2. Click Save | Text saves and displays without breaking the DB. | Medium |
| TC-10 | Check form reset behavior | 1. Submit a valid idea<br>2. Watch the form after submission | Both content and URL fields should become empty. | Medium |

## 2. Smart Tag Generation (Mock NLP)
| ID | Test Scenario | Steps to Reproduce | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC-11 | Generate tag for "app" | 1. Enter "I want to build an app"<br>2. Click Save | Tag `#side-project` appears under the idea. | High |
| TC-12 | Generate tag for "health" | 1. Enter "Go to the gym"<br>2. Click Save | Tag `#health` appears under the idea. | High |
| TC-13 | Generate tag for "code" | 1. Enter "Learn Python code"<br>2. Click Save | Tag `#coding` appears under the idea. | High |
| TC-14 | Generate tag for "reading" | 1. Enter "Read a book"<br>2. Click Save | Tag `#reading` appears under the idea. | High |
| TC-15 | Generate tag for "startup" | 1. Enter "AI startup idea"<br>2. Click Save | Tag `#business` appears under the idea. | High |
| TC-16 | Multiple keywords matched | 1. Enter "Build a health app"<br>2. Click Save | Multiple tags appear: `#side-project`, `#health`. | High |
| TC-17 | No keywords matched | 1. Enter "Random thought"<br>2. Click Save | Default tag `#random-thought` appears. | Medium |
| TC-18 | More than 3 keywords | 1. Enter "Build an app with Python for a health startup"<br>2. Click Save | Only the first 3 generated tags are saved and displayed. | Medium |
| TC-19 | Case insensitivity | 1. Enter "BUILD AN APP"<br>2. Click Save | Tags should still generate (ignoring uppercase). | Medium |
| TC-20 | Tag UI design | 1. Create an idea with tags<br>2. Look at the tags | Tags should have a blue background, rounded corners, and `#` prefix. | Low |

## 3. Dashboard & UI Rendering
| ID | Test Scenario | Steps to Reproduce | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC-21 | Empty state display | 1. Delete all ideas (or start fresh)<br>2. Look at dashboard | "No ideas yet. Add one above!" is displayed. | Medium |
| TC-22 | Idea count updates | 1. Note the current idea count<br>2. Add a new idea | The count in the heading "Your Ideas (X)" increments by 1. | Medium |
| TC-23 | List rendering performance | 1. Add 20+ ideas<br>2. Scroll through the page | Page should not lag. All ideas render in a vertical list. | High |
| TC-24 | URL link behavior | 1. Click a saved URL | Opens the link in a new browser tab. Dashboard stays open. | Medium |
| TC-25 | Responsive mobile view | 1. Open DevTools<br>2. Toggle mobile view (iPhone 12) | Form and idea cards stack vertically. No horizontal scrolling. | High |

## 4. Backend API Testing (Postman)
| ID | Test Scenario | Steps to Reproduce | Expected Result | Priority |
| :--- | :--- | :--- | :--- | :--- |
| TC-26 | GET all ideas | 1. Send `GET http://127.0.0.1:8000/ideas` | Returns `200 OK` and a JSON array of ideas. | High |
| TC-27 | POST valid idea | 1. Send `POST` with valid JSON body | Returns `200 OK`. Idea is saved to DB. | High |
| TC-28 | POST missing content | 1. Send `POST` with `{"url": "test.com"}` | Returns `422 Unprocessable Entity` (content is required). | High |
| TC-29 | POST wrong data type | 1. Send `POST` with `{"content": 123}` (number) | Returns `422 Unprocessable Entity` (expects string). | Medium |
| TC-30 | POST as form-data | 1. Send `POST` but change body to `form-data` | Returns `422 Unprocessable Entity` (API expects JSON). | Medium |
