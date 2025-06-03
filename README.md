# swiggy-assignment-genai
Personal AI assistant

## Setup

1. **Clone the repository**
   ```sh
   git clone git@github.com:AbhishekRP2002/swiggy-assignment-genai.git
   cd swiggy-assignment-genai
   ```

2. **Install dependencies**
   - Recommended to use [Poetry](https://python-poetry.org/):
     ```sh
     poetry install
     ```
   - Or use pip (if you prefer):
     ```sh
     pip install -r requirements.txt
     ```

3. **Set your OpenAI API key**
   - Copy `.env.example` to `.env` and add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-open-ai-api-key-here
     ```

---

## Running the FastAPI Interface

Start the FastAPI server:
```sh
poetry run python api.py
```
Or, if using pip:
```sh
python api.py
```
or
```sh
fastapi run api.py
```

The API will be available at: [http://localhost:8000](http://localhost:8000)

### Sample `curl` Request

```sh
curl -X 'POST' \
  'http://0.0.0.0:8000/process-query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Book me a table for two at an Italian restaurant tomorrow night"
}'
```

---

## Running the Streamlit Interface

Start the Streamlit app:
```sh
poetry run streamlit run app.py
```
Or, if using pip:
```sh
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501)

---

## Project Structure

- `api.py` — FastAPI backend interface
- `app.py` — Streamlit frontend interface
- `src/agent.py` — Core logic and agent code
- `src/utils.py` — Utility functions
- `src/prompts.py` — Prompt templates holder
- `.env.example` — Example environment variables

---