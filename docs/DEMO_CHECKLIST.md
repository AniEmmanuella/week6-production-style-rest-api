# Project Demonstration Checklist

1. Explain the task-management problem and the API's purpose.
2. Start the server with `uvicorn app.main:app --reload`.
3. Open `/docs` and identify the health and task routes.
4. Demonstrate that task routes require a Bearer token.
5. Create a task and show the generated ID and timestamps.
6. List tasks using pagination.
7. Filter by status, priority and search term.
8. Retrieve, update and delete a task.
9. Submit invalid input and show the 422 validation response.
10. Request a missing task and show the 404 response.
11. Run `pytest` and explain the test coverage.
12. Explain the folder structure, environment configuration and deployment files.
