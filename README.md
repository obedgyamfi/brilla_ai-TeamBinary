# brilla_ai-TeamBinary
AfricAIED Hackathon
Sure, here is a comprehensive README file for running a Next.js project with Tailwind CSS and a Python Flask server. 

---

# Project Setup and Run Instructions

## Prerequisites

Ensure you have the following installed on your system:
- Node.js
- npm (Node Package Manager)
- Python 3.9 or Python 3.10
- pip (Python Package Installer)

## Project Structure

```
project-root/
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── styles/
│   ├── pages/
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── ...
│   
├── app/
│   ├── venv/
│   ├── requirements.txt
│   ├── database_server.py
│   ├── ...
│
└── README.md
```

## Setting Up the Frontend (Next.js with Tailwind CSS)

1. **Navigate to the `frontend` directory**:
    ```sh
    cd frontend
    ```

2. **Install dependencies**:
    ```sh
    npm install
    ```

3. **Run the development server**:
    ```sh
    npm run dev
    ```

The frontend development server should now be running at `http://localhost:3000`.

## Setting Up the Backend (Python Flask)

1. **Navigate to the `backend` directory**:
    ```sh
    cd app
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:
        ```sh
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required Python packages**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Run the Flask server**:
    ```sh
    python database_server.py
    ```

The backend server should now be running and listening for requests.

## Running Both Servers Simultaneously

1. Open two terminal windows or tabs.
2. In the first terminal, navigate to the `backend` directory and activate the virtual environment:
    ```sh
    cd backend
    source venv/bin/activate  # Use the appropriate command for your OS
    python database_server.py
    ```

3. In the second terminal, navigate to the `frontend` directory:
    ```sh
    cd frontend
    npm run dev
    ```

Now, both the frontend and backend servers should be up and running.

## Notes

- Ensure the Flask server is running before making any API calls from the Next.js frontend.
- For any additional configuration or environment variables, refer to the respective configuration files in the `frontend` and `backend` directories.
- To deactivate the virtual environment, you can run:
    ```sh
    deactivate
    ```

## Troubleshooting

- If you encounter any issues with dependencies, ensure that your versions of Node.js, npm, and Python are compatible with the project requirements.
- Check for any error messages in the console for both the frontend and backend servers. These messages often provide clues on what might be wrong and how to fix it.
- Ensure that ports `3000` (for the Next.js server) and the respective port for your Flask server (commonly `3001` by default) are not being used by other applications.

---
