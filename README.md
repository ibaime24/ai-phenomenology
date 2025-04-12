# AI Phenomenologist

This project implements an AI Phenomenologist that analyzes text passages and reflects on its own uncertainties during interpretation.

## Setup

### Automatic Setup (Recommended)

1. Clone this repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
   This will:
   - Create a virtual environment
   - Install dependencies
   - Create a .env file from the template

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Edit `.env` and add your OpenAI API key

### Manual Setup

If you prefer to set up manually:

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
5. Edit `.env` and add your OpenAI API key

## Usage

Make sure your virtual environment is activated:
```bash
source venv/bin/activate
```

Then run the script:
```bash
python main.py
```

The program will prompt you to enter a text passage. It will then:
1. Analyze the passage and provide an initial description
2. Identify any uncertain interpretations (based on token probabilities)
3. Reflect on those uncertainties if any are found

## Configuration

You can modify the following parameters in `main.py`:
- `model`: The OpenAI model to use
- `logprob_threshold`: The confidence threshold for identifying uncertain tokens
- `max_tokens`: Maximum length of generated responses

## Deactivating the Virtual Environment

When you're done, you can deactivate the virtual environment:
```bash
deactivate
``` 