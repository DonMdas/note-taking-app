# MyNotes - Django Note-Taking Web Application

MyNotes is a web-based application, created by Don and Abhin, built with Django that allows users to securely create, manage, and summarize their personal notes. It features user authentication, a dashboard overview, a note editor, and integration with Google's Gemini API for AI-powered summarization.

## Features

*   **Secure User Authentication:** Register, login, and logout functionality. Passwords are securely hashed.
*   **Multi-User Support:** Each user's notes are private and isolated.
*   **Dashboard Overview:** Displays a list of the user's notes (latest modified first), along with statistics:
    *   Total number of notes.
    *   Number of notes created in the last 7 days.
    *   Number of notes edited in the last 3 days.
*   **Note Management (CRUD):** Create new notes, view/edit existing notes, and delete notes.
*   **AI-Powered Summarization:** Integrates with Google Gemini 2.0 Flash API to generate summaries of note content on demand.
*   **Responsive UI:** Uses Bulma and Bootstrap CSS frameworks for a clean and adaptable user interface.
*   **Simple Navigation:** Easy movement between the dashboard and editor views.

## Technology Stack

*   **Backend:** Python 3.x, Django
*   **Frontend:** HTML5, CSS3 (Bulma, Bootstrap), JavaScript (Vanilla JS for API calls)
*   **Database:** SQLite 3 (Default for development)
*   **AI Service:** Google Gemini API (`google-generativeai` library)
*   **Environment Variables:** `python-dotenv`

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your-repository-url>
    cd mynotes-project # Or your project's root directory name
    ```

2.  **Create and Activate a Virtual Environment:**
    *   **Linux/macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install Dependencies:**
    *(Ensure you have a `requirements.txt` file. If not, create one while the virtual environment is active: `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables:**
    *   Create a file named `.env` in the app directory.
    *   Add your Google Gemini API key to this file:
        ```dotenv
        # .env
        GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```


5.  **Apply Database Migrations:**
    ```bash
    python manage.py migrate
    ```


## Running the Application

1.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the Application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/` (or the address provided by `runserver`).

## Usage

1.  **Register:** Create a new user account via the `/register/` page.
2.  **Login:** Log in with your credentials via the `/login/` page.
3.  **Dashboard:** Upon login, you'll be redirected to the dashboard (`/`). Here you can see your notes and stats, and create a new note.
4.  **Create/Edit Note:**
    *   Click "New Note" (on dashboard or editor page) or "Edit" on an existing note card to go to the editor (`/editor/?docid=...`).
    *   Enter/modify the title and content.
    *   Click "Save Note" to persist changes.
    *   Click "Summarize" to generate key points using the Gemini API. The summary will appear in the "Key Points" section and will be saved with the note.
    *   Click "Delete" (requires confirmation) to remove the note.
5.  **Logout:** Click the "Logout" button to end your session.

