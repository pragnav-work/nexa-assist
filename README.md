# NexaAssist — AI Enterprise Employee Assistant

NexaAssist is an Agentic AI-powered enterprise employee assistant designed to help employees access company policies, retrieve employee-specific information, and perform supported workplace actions through a conversational interface.

The project combines LLM-based intent classification, RAG (Retrieval-Augmented Generation), MCP-style enterprise tools, deterministic validation, and human confirmation to provide a practical and safe employee-assistance workflow.

🎯 Project Objective

Employees often need information about company policies, leave, expenses, IT assets, office locations, and other workplace services.

NexaAssist provides a single conversational interface where employees can ask questions such as:

"How many WFH days can I take?"

"What is the reimbursement policy for meals?"

"How many leave days do I have?"

"Show me my leave requests."

"What assets are assigned to me?"

"Where is the Chennai office located?"

"I want earned leave from 2026-09-15 to 2026-09-17."

The assistant determines the type of request, selects the appropriate processing path, retrieves the required information, validates sensitive actions, and responds through the Streamlit interface.

🏢 Fictional Organization

Field

Details

Company

NexaCore Technologies Pvt. Ltd.

Assistant

NexaAssist

Data

Fictional company policies and mock employee data

Note: The organization, employees, policies, and enterprise data used in this project are fictional and are intended for demonstration purposes only.

✨ Key Features

1. 🧠 Agentic Request Routing

NexaAssist uses an LLM-based intent classifier to understand employee requests and determine the appropriate action.

Supported intents include:

Company policy queries

Employee information

Leave balance

Leave requests

Leave submission

Employee expenses

Expense status

Expense submission

Assigned IT assets

Office locations

Unknown or unsupported requests

The request is then routed to either the RAG knowledge system or enterprise tools.

2. 📚 Retrieval-Augmented Generation (RAG)

Company policies are stored as PDF documents and processed through a RAG pipeline.

Current policy documents include:

Leave Policy

Reimbursement Policy

Travel Policy

Work From Home Policy

RAG Pipeline

Load policy documents
        ↓
Extract document content
        ↓
Split content into chunks
        ↓
Generate embeddings
        ↓
Store vectors in FAISS
        ↓
Retrieve relevant chunks
        ↓
Generate answer
        ↓
Display answer + citations

This helps the assistant answer policy questions using organizational knowledge rather than relying only on the language model's general knowledge.

3. 🔧 MCP Enterprise Tools

NexaAssist integrates enterprise-style tools backed by mock CSV data.

Employee Tools

Retrieve employee information

Leave Tools

Retrieve leave balance

Retrieve leave requests

Submit leave requests

Expense Tools

Retrieve employee expenses

Check expense status

Submit employee expenses

IT Tools

Retrieve assigned IT assets

Office Tools

Retrieve office location information

These tools simulate how an enterprise assistant could interact with internal systems.

4. 🛡️ Employee Identity Protection

Employee identity is controlled by the application session, not by the language model.

The Streamlit application provides an employee selector for the demonstration.

For example, if the current session belongs to NC1001 and the user asks:

How many leave days does NC1002 have?

NexaAssist rejects the request instead of retrieving another employee's information.

This ensures that the LLM cannot override the employee identity established by the application.

5. ✅ Deterministic Validation

Sensitive employee actions are validated using deterministic Python validation logic rather than relying on the LLM to make safety decisions.

Validation includes:

Employee identity matching

Required fields

Valid leave type

Valid date ranges

Past-date prevention

Leave balance checks

Positive expense amounts

Required expense descriptions

Explicit action confirmation

6. 🙋 Human-in-the-Loop Confirmation

State-changing actions require explicit employee confirmation.

For example, a leave request follows this workflow:

Employee requests leave
        ↓
Leave details extracted
        ↓
Leave balance retrieved
        ↓
Request validated
        ↓
Confirmation displayed
        ↓
     ┌─────────┐
     │ Confirm │
     └────┬────┘
          ↓
     MCP action
          ↓
      CSV updated

The employee can choose:

✅ Confirm — The action is executed.

❌ Cancel — The action is cancelled and no data is changed.

This prevents unintended state-changing operations.

🖥️ User Interface

NexaAssist uses Streamlit to provide a conversational employee-assistant interface.

The UI provides:

Employee session selection

Chat interface

Conversation history

Structured MCP responses

Leave balance cards

Assigned asset cards

Leave request cards

RAG source citations

Activity log

Action confirmation controls

The application maintains conversation state during the active Streamlit session.

🏗️ System Architecture

                 ┌──────────────────────┐
                 │     Streamlit UI     │
                 │   Employee Session   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   NexaAssist Agent   │
                 │                      │
                 │ Intent Classification│
                 │ Request Routing      │
                 └──────────┬───────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
     ┌─────────────────┐        ┌──────────────────┐
     │       RAG       │        │   Enterprise     │
     │  Knowledge Base │        │   Tools / MCP    │
     └────────┬────────┘        └─────────┬────────┘
              │                           │
              ▼                           ▼
     ┌─────────────────┐        ┌──────────────────┐
     │ Company Policy  │        │  Mock CSV Data   │
     │   PDFs + FAISS  │        │  Employee Data   │
     └─────────────────┘        └─────────┬────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  Deterministic   │
                                │    Validation    │
                                └─────────┬────────┘
                                          │
                                          ▼
                                ┌──────────────────┐
                                │      Human       │
                                │   Confirmation   │
                                └─────────┬────────┘
                                          │
                                    Confirm
                                          │
                                          ▼
                                ┌──────────────────┐
                                │  State-Changing  │
                                │    MCP Action    │
                                └──────────────────┘

📁 Project Structure

```text
nexa-assist/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── documents/
│   │   ├── leave_policy.pdf
│   │   ├── reimbursement_policy.pdf
│   │   ├── travel_policy.pdf
│   │   └── wfh_policy.pdf
│   │
│   └── seed/
│       ├── employees.csv
│       ├── expense_records.csv
│       ├── it_assets.csv
│       ├── leave_balance.csv
│       ├── leave_requests.csv
│       └── office_locations.csv
│
├── notebooks/
│   └── RAG_Pipeline.ipynb
│
├── src/
│   ├── agents/
│   │   ├── intent_classifier.py
│   │   ├── office_assistant.py
│   │   ├── prompts.py
│   │   └── router.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   ├── mcp/
│   │   └── server.py
│   │
│   ├── models/
│   │   ├── classification.py
│   │   ├── intents.py
│   │   ├── routes.py
│   │   └── state.py
│   │
│   ├── rag/
│   │   ├── build_index.py
│   │   ├── chunker.py
│   │   ├── citation.py
│   │   ├── config.py
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── pipeline.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── tools/
│   │   ├── csv_utils.py
│   │   ├── employee_tools.py
│   │   ├── expense_tools.py
│   │   ├── it_tools.py
│   │   ├── leave_tools.py
│   │   ├── office_tools.py
│   │   └── tool_dispatcher.py
│   │
│   └── validation/
│       └── validator.py
│
├── tests/
│   ├── test_validation.py
│   ├── test_end_to_end.py
│   ├── test_mcp_tools.py
│   ├── test_rag_pipeline.py
│   └── ...
│
├── create_seed_data.py
├── requirements.txt
├── .env.example
└── README.md
```

⚙️ Technology Stack

Component

Technology

User Interface

Streamlit

LLM

Google Gemini

Programming Language

Python

RAG

FAISS + Sentence Transformers

Embeddings

all-MiniLM-L6-v2

Enterprise Data

CSV

Tool Layer

MCP-style enterprise tools

Validation

Deterministic Python

Testing

Pytest

Version Control

Git + GitHub

🚀 Getting Started

1. Clone the Repository

git clone https://github.com/pragnav-work/nexa-assist.git
cd nexa-assist

2. Create a Virtual Environment

python -m venv .venv

Linux / macOS

source .venv/bin/activate

Windows

.venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Gemini API Key

Create a .env file:

GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

Important: Do not commit the .env file to GitHub. The repository provides .env.example as a template.

5. Build the RAG Index

Run:

python -m src.rag.build_index

This creates the local policy vector index used by the RAG pipeline. The generated vector store is ignored by Git.

6. Run the Application

streamlit run app/streamlit_app.py

The application will open in the browser.

💬 Example Queries

Policy / RAG

Example queries:

How many WFH days can I take?

What is the reimbursement policy for meals?

Expected behavior:

User Query
    ↓
Intent Classification
    ↓
RAG Route
    ↓
Policy Retrieval
    ↓
Answer + Citation

Employee Information / MCP

Example queries:

How many leave days do I have?

Show me my leave requests.

What assets are assigned to me?

Expected behavior:

User Query
    ↓
Intent Classification
    ↓
MCP Route
    ↓
Employee-specific CSV Data
    ↓
Formatted Response

Security Validation

With employee NC1001 selected:

Query:

How many leave days does NC1002 have?

Expected behavior:

Request rejected.

I can only provide employee-specific information for the employee currently selected in this session.

Leave Request

Query:

I want earned leave from 2026-09-15 to 2026-09-17.

Expected workflow:

Leave Request
    ↓
Extract Leave Details
    ↓
Retrieve Balance
    ↓
Validate Request
    ↓
Confirmation Required
    ↓
User Confirms
    ↓
Submit Through MCP Tool

🧪 Testing

NexaAssist includes automated tests for individual components and end-to-end workflows.

Run all tests:

pytest -q

The test suite covers areas including:

RAG document loading

Chunking

Embeddings

Retrieval

Citations

MCP tools

Tool dispatcher

Validation

Employee identity protection

Leave validation

Human confirmation

End-to-end workflows

Example Safety Scenarios

The test suite includes scenarios such as:

Preventing access to another employee's information

Rejecting leave requests exceeding available balance

Rejecting past-dated leave

Rejecting invalid date ranges

Requiring leave type

Requiring explicit confirmation before state-changing actions

🔐 Safety and Guardrails

NexaAssist follows several safety principles.

Application-Controlled Identity

The employee identity comes from the application session and cannot be selected by the LLM.

Deterministic Validation

Critical validation rules are implemented in Python.

Human Confirmation

State-changing actions require explicit confirmation.

No Hallucination for Unknown Policies

If the required organizational policy cannot be found, the assistant should avoid inventing policy information.

No Chain-of-Thought Exposure

The application displays only high-level activity information such as:

Request received
Intent identified
Route selected
Retrieved relevant company policy
Validated request
Confirmation required

Internal reasoning is not exposed to the employee.

📊 Data Model

The project uses CSV files as lightweight mock enterprise data sources.

Employee Data

employees.csv

Contains employee information used by the assistant.

Leave Data

leave_balance.csv

leave_requests.csv

Used for leave balance retrieval, leave request history, and leave submission.

Expense Data

expense_records.csv

Used for employee expense information and expense operations.

IT Assets

it_assets.csv

Used to retrieve assigned employee assets.

Office Locations

office_locations.csv

Used to retrieve office location information.

🔄 Example End-to-End Flow

A typical state-changing request follows this process:

Employee
    │
    ▼
Streamlit UI
    │
    ▼
Intent Classifier
    │
    ▼
Request Router
    │
    ▼
Leave Request Handler
    │
    ├── Retrieve Leave Balance
    ├── Validate Employee Identity
    ├── Validate Leave Type
    ├── Validate Dates
    └── Validate Leave Balance
    │
    ▼
Human Confirmation
    │
    ├── Cancel ──► No Change
    │
    └── Confirm
          │
          ▼
      MCP Tool
          │
          ▼
      CSV Data Update
          │
          ▼
      Response to Employee

👥 Team Contributions

NexaAssist was developed as a collaborative four-member capstone project.

Contributor

Responsibility

Person 1

Agent orchestration and intent routing

Person 2

RAG pipeline and policy knowledge retrieval

Person 3

MCP tools and enterprise data operations

Person 4

Streamlit UI, validation, safety guardrails, and end-to-end testing

The project uses feature branches and an integration branch to support parallel development.

🌿 Git Workflow

The team follows a feature-branch workflow:

main
 │
 └── integration
      │
      ├── feature/agent-orchestration
      ├── feature/rag-knowledge
      ├── feature/mcp-tools
      └── feature/ui-validation

Contributors develop independently on feature branches and merge completed work into integration before the final release to main.

🔮 Future Improvements

Potential future enhancements include:

Persistent conversation history

Database-backed enterprise systems

More enterprise actions

Richer multi-step workflows

Improved tool discovery

Authentication integration

Enterprise SSO integration

Role-based access controls

Audit logging

Production-grade MCP server deployment

More comprehensive policy coverage

Improved observability and monitoring

⚠️ Disclaimer

NexaAssist is an academic/capstone demonstration project.

The company, employees, policies, and enterprise data used in the application are fictional or mock data created for demonstration purposes.

The system should not be used as a production enterprise HR, finance, IT, or policy-management system without appropriate security, authentication, authorization, auditing, and infrastructure controls.

📌 Project Status

Status: Capstone Project — Functional Prototype

NexaAssist currently demonstrates:

Agentic request routing

RAG-based policy retrieval

Employee-specific enterprise tools

CSV-backed mock enterprise operations

Deterministic validation

Employee identity protection

Human-in-the-loop confirmation

Streamlit conversational UI

Automated testing
