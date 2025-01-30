# EscapeExpress Level Generator using LLMs

Generates a full train of wagons and passengers for the EscapeExpress game using a single theme.
Should be much better than the current hackathon level...

## Usage
Put your Mistral API KEY in the env var (os.getenv("MISTRAL_API_KEY")) or in a .env file.

### Backend
```python
from generate import generate_train

# contains the dict objects not the json strings
names, player_details, wagons = generate_train(<player_input>, <wagon_count2-10>)
```

### Test the Gradio App
```bash
pip install -r requirements.txt
python app.py
```