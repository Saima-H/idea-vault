\# 💡 Idea Vault



A personal app to save ideas and links, auto-tag them, and filter by tag.



\## Tech Stack

\- Backend: FastAPI (Python)

\- Frontend: Next.js (React)

\- Database: SQLite (dev) → PostgreSQL (prod)

\- AI: Mock NLP for tag generation



\## Status

🚧 Day 1 — Project setup



\## Architecture



```mermaid

flowchart LR

&#x20;   User(\[👤 User]) --> FE\["Next.js :3000"]

&#x20;   FE --> CORS{{CORS Middleware}}

&#x20;   CORS --> BE\["FastAPI :8000"]

&#x20;   BE --> DB\[("Database")]

&#x20;   BE --> AI\[🤖 Smart Tags]

&#x20;   AI --> BE

&#x20;   DB --> BE

&#x20;   BE --> CORS

&#x20;   CORS --> FE

&#x20;   FE --> User
```
