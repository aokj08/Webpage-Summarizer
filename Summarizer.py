import sys

import requests
from openai import OpenAI
from Common import tokenize_text, detokenize_text, get_text_from_url, download, split_text

client = OpenAI()

# The amount of token allocated to read the webpage
MAX_TOKENS_READ = 4000

# The amount of token allocated to generate response
MAX_TOKENS_WRITE = 100

PREPROMPT = "Summarize this webpage: \n\n"

# The amount of token allocated for preprompt
PREPROMPT_TOKENS = len(tokenize_text(PREPROMPT))

# Total amount of token needed
TOKEN_BUDGET = MAX_TOKENS_READ - MAX_TOKENS_WRITE - PREPROMPT_TOKENS


def response(prompt: str, max_tokens=TOKEN_BUDGET):
    prompt = PREPROMPT + prompt
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return chat_completion.choices[0].message.content


def summarize(text_):
    # Tokenize the text
    tokenized = tokenize_text(text_)

    # Split text
    splited = split_text(tokenized, TOKEN_BUDGET)

    # Convert each chunk of tokens back into text and ask LLM to summarize it.
    # With the result generated, we feed it back to LLM to further summarize.
    if len(splited) > 1:
        summaries = []
        for i, chunk in enumerate(splited):
            chunk_text = detokenize_text(chunk)
            summaries.append(summarize(chunk_text))
            print(i, summaries[-1])
        summaries = " ".join(summaries)
    else:
        summaries = text
    return response(summaries)


# Get the url of the website trying to summarize
url = sys.argv[1]

# download the html from the url
html = download(url)

# Now convert the page into text
text = get_text_from_url(html)

# Output result
print(summarize(text))


