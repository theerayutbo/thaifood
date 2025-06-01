# Saneh Jaan AI - Modern Thai Cuisine

Saneh Jaan AI is a web application for a modern Thai restaurant. It allows users to browse the menu, view ingredients, and interact with an AI-powered assistant for queries and recipe suggestions. The application supports both English and Thai languages.

## Features

*   **Browse Menu & Ingredients:** Users can explore a variety of Thai dishes and quality ingredients offered by the restaurant.
*   **AI Assistant:** Powered by Ollama, the AI assistant can:
    *   Answer general questions about the restaurant (e.g., opening hours).
    *   Provide recipe ideas based on user queries.
    *   Identify menu items mentioned in conversations.
*   **Dual Language Support:** The user interface and AI responses can be switched between English and Thai.
*   **Shopping Cart:** (Planned Feature) Functionality to add items to a cart for ordering.

## Technologies Used

*   **Backend:** Python (Flask framework)
*   **Frontend:** HTML, CSS, JavaScript
*   **AI:** Ollama (specifically tested with `llama3.2` model)
*   **HTTP Requests:** `requests` library in Python for communicating with the Ollama API.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    This project uses Flask and Requests. You can install them using pip:
    ```bash
    pip install Flask requests
    ```
    *(It is recommended to create a `requirements.txt` file with these dependencies for easier setup: `Flask>=2.0`, `requests>=2.20`)*

4.  **Configure Ollama:**
    *   Ensure you have Ollama installed and running. You can download it from [https://ollama.com/](https://ollama.com/).
    *   Pull the desired model if you haven't already (e.g., `ollama pull llama3.2`).
    *   The application expects the Ollama API to be available at `http://localhost:11434/api/generate`. This is configured via `OLLAMA_API_URL` in `app.py`.
    *   The AI model used is set by `OLLAMA_MODEL` in `app.py` (default is `llama3.2`). You can change this to any compatible model you have in Ollama.

5.  **Run the Application:**
    ```bash
    python app.py
    ```
    The application will typically be available at `http://127.0.0.1:5000/`.

## Project Structure

```
.
├── app.py            # Main Flask application logic, routes, and AI interaction
├── README.md         # This file
├── static/           # Static assets
│   ├── css/          # Stylesheets (e.g., style.css)
│   ├── images/       # Product images
│   └── js/           # Client-side JavaScript (e.g., ai_sidebar.js)
└── templates/        # HTML templates
    ├── index.html    # Template for displaying menu/grocery items
    └── layout.html   # Base layout template
```

## How to Use

*   **Navigate:** Use the navigation bar to switch between "Home" (recommended dishes), "Menu" (all dishes), and "Ingredients".
*   **Switch Language:** Click on "ภาษาไทย" or "English" in the navigation bar to change the display language.
*   **AI Assistant:**
    *   Open the AI sidebar (if not already open).
    *   Type your questions about the menu, restaurant, or ask for Thai recipe ideas (e.g., "What are your opening hours?", "Suggest a spicy chicken recipe").
    *   The AI will respond in the currently selected language.
    *   If the AI identifies a menu item in its response that is present on the current page, that item will be briefly highlighted.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is currently unlicensed. Consider adding an MIT License or another open-source license if you plan to share it widely.
