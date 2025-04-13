############################################
# PHENOMENOLOGIST (Chat + logprobs)
# Using the OpenAI API to analyze text with confidence scores
# One-shot file: all logic is in main.py
############################################

import os
from math import exp
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

############################################
# 1) Instantiate your custom OpenAI client
############################################
# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=api_key)

############################################
# 2) The get_completion helper function
############################################
def get_completion(
    messages,
    model="gpt-4o-mini",
    max_tokens=16000,
    temperature=0.7,
    stop=None,
    seed=123,
    tools=None,
    logprobs=None,            # set to True or False
    top_logprobs=None         # integer 0-5
):
    """
    Wrapper around client.chat.completions.create(...) that returns
    a 'completion' object with:
      - completion.choices[0].message.content (model's text response)
      - completion.choices[0].logprobs.content (token-level data, if logprobs=True)
    """
    params = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stop": stop,
        "seed": seed,
        "logprobs": logprobs,
        "top_logprobs": top_logprobs,
    }
    if tools:
        params["tools"] = tools

    completion = client.chat.completions.create(**params)
    return completion


############################################
# 3) The "AI Phenomenologist" pipeline
############################################

def run_phenomenologist(
    text_passage: str,
    model="gpt-4o-mini",
    logprob_threshold=-1.0
):
    """
    Steps:
      1) Send initial prompt describing the text, collect tokens + logprobs
      2) Identify uncertain tokens (below logprob_threshold)
      3) If any, build a meta-prompt to reflect on them
      4) Get second reflection response
    """

    # Step A: Construct the first prompt
    initial_prompt = f"""You are perceiving this text passage for the first time.
Describe what it's like to read it.

TEXT PASSAGE:
\"\"\"
{text_passage}
\"\"\""""

    # Make the call with logprobs=True so we get token-level data
    response_init = get_completion(
        messages=[{"role": "user", "content": initial_prompt}],
        model=model,
        logprobs=True,
        top_logprobs=2
    )

    # The model's descriptive text
    initial_text = response_init.choices[0].message.content.strip()

    # The token-by-token logprob data (list of objects)
    token_data = response_init.choices[0].logprobs.content

    print("=== Initial Description ===")
    print(initial_text)
    print()

    # Step B: Find uncertain tokens
    uncertain_tokens = []
    for tinfo in token_data:
        lp = tinfo.logprob
        tok = tinfo.token
        # If below threshold, we consider it "uncertain"
        if lp is not None and lp < logprob_threshold:
            uncertain_tokens.append((tok, lp))

    if uncertain_tokens:
        print("Uncertain Tokens (lowest confidence):")
        for tok, lp in uncertain_tokens:
            prob_pct = round(exp(lp) * 100, 2)
            print(f"  '{tok}' -> logprob={lp:.4f} (~{prob_pct}%)")
        print()
    else:
        print("No tokens found below the confidence threshold.")
        return  # or you could keep going, but there's nothing to reflect upon

    # Step C: Build meta-prompt for reflection
    tokens_str = " ".join([t for (t, _) in uncertain_tokens])
    reflection_prompt = f"""
You used some low-confidence tokens: "{tokens_str}".
Explain what made these details uncertain or ambiguous,
and reflect on your process of interpretation.

ORIGINAL TEXT PASSAGE:
{text_passage}
"""

    # Step D: Get reflection response
    reflection_resp = get_completion(
        messages=[{"role": "user", "content": reflection_prompt}],
        model=model,
        logprobs=True,
        top_logprobs=2
    )

    reflection_text = reflection_resp.choices[0].message.content.strip()

    print("=== Reflection on Uncertain Tokens ===")
    print(reflection_text)


############################################
# 4) Main Usage: Prompt user for input
############################################
if __name__ == "__main__":
    # Prompt the user to enter a short text passage
    user_text = input("Enter a short text passage: ").strip()

    # Run the AI Phenomenologist with user input
    run_phenomenologist(
        text_passage=user_text,
        model="gpt-4o-mini",    
        logprob_threshold=-1.0
    )
