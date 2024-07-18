Here's the README file for your Flask application:

```markdown
# Flask File Upload and Optimization

This Flask application allows users to upload Python files, optimize their content using an `optimize` function, and return the optimized file along with logging and cost information.

## Setup and Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the Code Directory**

   Make sure the `code` directory exists in the root of the project. The application will store uploaded files and optimized files here.

## Running the Application

1. **Start the Flask Application**

   ```bash
   python app.py
   ```

   The application will run on `http://127.0.0.1:5000` by default.

## Usage

### Upload and Optimize a File

Send a POST request to `/upload` with a `.py` file:

```bash
curl -X POST -F 'file=@path/to/your/file.py' http://127.0.0.1:5000/upload -o optimized.py
```

### Response

- The optimized file will be downloaded.
- The response headers will include logging and cost information:

  - `logging_session_id`: The ID of the logging session.
  - `total_tokens`: The total number of tokens used across all sessions.
  - `total_cost`: The total cost across all sessions.
  - `session_tokens`: The number of tokens used in the current session.
  - `session_cost`: The cost of the current session.

## Code Overview

### `app.py`

- Handles file upload, optimization, and response construction.
- Routes:
  - `POST /upload`: Upload and optimize a Python file.

### `main.py`

- Contains the `optimize` function which initiates the optimization process using agents.

### `autogen_logs.py`

- Contains functions for logging and calculating costs associated with the optimization process.

### Logging and Cost Calculation

- The application uses `autogen.runtime_logging` to log optimization sessions.
- The `calculate_costs` function fetches log data from an SQLite database and calculates token usage and costs.

### Example Usage of `calculate_costs`

```python
# Example usage of the calculate_costs function
session_id = "your_session_id_here"
(total_tokens, total_cost), (session_tokens, session_cost) = calculate_costs(session_id)

if total_tokens is not None:
    print(f"Total tokens for all sessions: {total_tokens}, total cost: {total_cost}")
    print(f"Total tokens for session {session_id}: {session_tokens}, cost: {session_cost}")
```

## Requirements

Ensure you have the following Python packages installed:

- Flask
- pandas
- sqlite3

Install these dependencies using the following command:

```bash
pip install Flask pandas
```

## Notes

- Make sure to adjust the `optimize` function in `main.py` according to your specific needs.
- Ensure the `code` directory is writable by the application.
- Update the `<repository-url>` in the setup instructions with the actual URL of your repository.
```

This README file provides a comprehensive guide to setting up, running, and using your Flask application, along with a brief overview of the code and its functionalities. Adjust the `<repository-url>` with the actual URL of your repository.
