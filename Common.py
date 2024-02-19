from bs4 import BeautifulSoup
import requests
import tiktoken
import dotenv

dotenv.load_dotenv()

# Defining the model of tokenizer
enc = tiktoken.get_encoding('cl100k_base')
enc = tiktoken.encoding_for_model('gpt-3.5-turbo')


def get_text_from_url(html_):
    soup = BeautifulSoup(html_.text, "html.parser")
    return soup.get_text()


def download(url_: str):
    # Setting user agent as something else in the header prevent websites from block access
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    return requests.get(url_, headers=headers)


def tokenize_text(text_: str):
    return enc.encode(text_)


def detokenize_text(text_: str):
    return enc.decode(text_)


def split_text(tokenized_, budget):
    # Every time we reach budget, we create a new chunk
    split = []
    for i in range(0, len(tokenized_), budget):
        split.append(tokenized_[i:i+budget])

    # To prevent the problem of disconnectedness, we pad the last chunk with its previous chunk if the last chunk is
    # not full
    if len(split[-1]) < budget and len(split) > 1:
        # Calculate how much left
        remaining = budget - len(split[-1])
        # Reconstruct last chunk
        split[-1] = split[-2][-remaining:] + split[-1]
    return split

