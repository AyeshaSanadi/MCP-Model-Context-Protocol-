# Interview Tracker MCP

An MCP (Model Context Protocol) server built with FastMCP and SQLite to help track interview experiences across different companies.

The server allows you to:

- Store company application details
- Track interview rounds
- Record interview questions
- Save interview feedback and improvement areas
- Track interview outcomes
- Generate company interview summaries

---

## Features

### Company Management

- Add company details
- List all companies
- Search company information
- Update company status
- View selected companies
- View rejected companies
- Get company interview summary

### Interview Management

- Add interview rounds
- Track round-wise interview status
- Store questions asked during interviews
- Record improvement areas and feedback
- View all interview rounds for a company
- Update interview round details

---

## Database Schema

### CompanyDetails

| Column         | Description                                |
| -------------- | ------------------------------------------ |
| company_id     | Unique company identifier                  |
| company_name   | Company name                               |
| position       | Applied position                           |
| overall_status | Pending, Selected, Rejected, OfferReceived |
| created_at     | Record creation timestamp                  |
| total_rounds   | Total interview rounds completed           |

### InterviewRounds

| Column           | Description                             |
| ---------------- | --------------------------------------- |
| interview_id     | Unique interview identifier             |
| company_id       | Foreign key reference to CompanyDetails |
| round_number     | Interview round number                  |
| interview_date   | Interview date                          |
| interview_status | Pending, Selected, Rejected             |
| questions_asked  | Questions asked during interview        |
| need_improvement | Feedback and improvement areas          |

---

## Example Workflow

### Step 1: Add Company

Company: Google

Position: Software Engineer

Status: Pending

### Step 2: Add Interview Round

Round Number: 1

Interview Date: 2026-06-15

Status: Selected

Questions Asked:

- Explain Python decorators
- What is multithreading?
- Difference between process and thread

Need Improvement:

- Improve system design communication
- Practice behavioral questions

### Step 3: Update Status

Company Status:

- Pending
- Selected
- Rejected
- OfferReceived

---

## Available MCP Tools

### Company Tools

#### add_company_details

Adds a new company application.

#### list_companies

Returns all tracked companies.

#### search_company_info

Returns information for a specific company.

#### update_company_status

Updates the overall application status.

#### show_selected_company

Lists all selected companies.

#### show_rejected_company

Lists all rejected companies.

#### get_company_summary

Returns:

- Company name
- Position
- Overall status
- Total interview rounds

---

### Interview Tools

#### add_interview_round

Adds a new interview round.

#### list_interview_details_of_particular_company

Returns all interview rounds for a company.

#### update_interview_details

Updates:

- Interview status
- Improvement notes

---

## Technology Stack

- Python 3.12+
- FastMCP
- SQLite
- UV Package Manager

---

## Run Locally

### Create Virtual Environment

```bash
uv venv
```

### Install Dependencies

```bash
uv add fastmcp
```

### Start MCP Server

```bash
uv run fastmcp run main.py
```

---

## Sample Use Cases

- Track job applications
- Store interview experiences
- Review previously asked interview questions
- Monitor interview progress
- Identify recurring skill gaps
- Build a personal interview knowledge base

---

## Future Enhancements

- Search questions across companies
- Interview analytics dashboard
- Question categorization (DSA, System Design, SQL, Behavioral)
- Export interview history to CSV/PDF
- AI-generated interview preparation suggestions
- Company-wise success statistics

---

## Project Goal

Interview Tracker MCP acts as a personal interview journal and knowledge repository, helping candidates learn from past interviews, track progress, and improve preparation for future opportunities.
