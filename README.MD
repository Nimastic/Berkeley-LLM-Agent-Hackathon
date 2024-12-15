# MentorBot: Your AI-Powered Coding Study Companion

## Overview
MentorBot is a web-based intelligent tutoring assistant that leverages a Large Language Model (LLM) to help students learn programming concepts more effectively. It supports contextual Q&A, integrates retrieval-augmented generation from curated course materials, and allows users to run code snippets to see results in real-time, fostering interactive learning experiences.

## Key Features:

- **Contextual Q&A:** Provides factually grounded answers using retrieval-augmented generation from embedded course materials.
- **Code Execution:** Allows users to paste Python code snippets and see the output instantly.
- **Personalized Learning:** Helps learners understand algorithms, data science principles, and coding best practices at their own pace.

## Project Directory Structure
```bash
MentorBot/
  README.md                     # This README file
  backend/
    main.py                     # Backend server code (FastAPI)
    requirements.txt            # Python dependencies
    .env                        # Environment variables (e.g., OPENAI_API_KEY)
    data/
      sample_course_material.txt # Embedded course content
    embeddings/
      # Vector database files created at runtime
    venv/                       # Optional virtual environment directory
  frontend/
    package.json                # Frontend package configuration
    src/
      index.js                  # React entry point
      App.js                    # Main App component
      ChatBubble.js             # UI component for chat messages
      ChatInput.js              # UI component for user input
    public/
      index.html                # Frontend HTML template
    node_modules/               # Installed Node.js dependencies
```

**Note:**
- `venv/` and `node_modules/` directories are typically local and not pushed to version control.
- Adjust paths if you have a different structure.

## Installation Instructions

### Pre-requisites
- Python 3.9+
- Node.js 16+
- An OpenAI API Key (if using OpenAI models)
- (Optional) A virtual environment tool like `venv` or `conda` for Python dependency management

### Backend Setup

Navigate to the backend directory:
```bash
cd MentorBot/backend
```

Create and activate a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install Python dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Set your environment variables:

Create or edit `.env` file in `backend/`:
```makefile
OPENAI_API_KEY=your-openai-api-key-here
```
Alternatively, set `OPENAI_API_KEY` as an environment variable in your shell.

Run the backend server:
```bash
uvicorn main:app --reload
```
If successful, the server will be accessible at `http://localhost:8000`.

### Frontend Setup

Open a new terminal (keeping the backend running in another window).

Navigate to the frontend directory:
```bash
cd MentorBot/frontend
```

Install Node.js dependencies:
```bash
npm install
```

Start the frontend development server:
```bash
npm start
```
This will open `http://localhost:3000` in your browser.

## Verifying Installation

With the backend running on `http://localhost:8000` and the frontend on `http://localhost:3000`, open `http://localhost:3000` in your browser.

You should see the MentorBot interface. Ask a question or paste Python code. MentorBot should respond with context-driven answers and/or code execution results.

## User Guide

1. **Asking Questions:**
   - Type your question into the text box at the bottom of the page. For example:
     - “Explain how bubble sort works.”
     - “What is 1+1?”
   - Press Send, and MentorBot will respond using context from the embedded course materials. If relevant info isn’t found, it may rely on general knowledge.

2. **Running Code Snippets:**
   - Below the question input, there’s another text box for code snippets. Paste a Python code snippet there:
     ```python
     print("Hello World")
     ```
   - Press Send. MentorBot will execute the code and return the output alongside its explanation.

3. **Learning Use Cases:**
   - **Reinforce Concepts:** Ask conceptual questions like “How does recursion work?” or “What’s the complexity of merge sort?”
   - **Debug Code:** Paste a piece of Python code that errors out and ask MentorBot for hints on what went wrong.
   - **Explore Algorithms:** Request explanations for data structures, machine learning basics, or data science concepts.

4. **Limitations and Tips:**
   - MentorBot’s responses depend on the provided course materials. For certain advanced queries not covered in the documents, it may rely on general reasoning or may say it doesn’t know.
   - Code execution is limited to Python code snippets and may not handle large or complex scripts. It’s meant for quick demonstrations, not production workloads.
   - If you encounter network errors, ensure both backend and frontend servers are running and check CORS settings.

## Troubleshooting

### Frontend “Failed to fetch” Error:
- Ensure the backend is running. Check that you’re accessing `http://localhost:3000` in the browser and that the backend server runs on `http://localhost:8000`.
- Consider matching domains (use `localhost` instead of `127.0.0.1`) or updating CORS settings in `main.py`.

### Backend Errors on Startup:
- Check dependencies and ensure your `OPENAI_API_KEY` is set. Update your `requirements.txt` or re-install dependencies if version conflicts arise.

## Contributing
We welcome contributions! To contribute:

1. Fork this repository.
2. Create a new branch for your changes.
3. Submit a pull request with a clear description of what you improved or fixed.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
