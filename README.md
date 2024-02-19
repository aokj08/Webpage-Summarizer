# **Webpage Summarizer**
### **Project Description**
As a person who doesn't want to spend too much time on reading long paragraphs
and articles, I thought about utilizing technologies such as the LLM to help
me with reading in order to accelerate my learning.
That is why I decided to learn how to build a webpage summarizer. The program 
will take a URL entered by the user and summarize it by calling ChatGPT API. 

### **How it works**
1) The program first downloads the the content of the provided URL with 
python requests library. By specifying a browser-like user-agent header, 
the program is less likely to be flagged as a data-scraping bot by the 
website.

2) After successful download, the content is then converted into plain
text with the help of a library function call from the BeautifulSoup 
library.

3) The text is then tokenized in preparation for "chunkifying" process.
Here, a OpenAI tokenizer library is used, namely tiktoken. 

4) "Chunkifying" is a crucial step as there are token limitations for
almost all LLM and we want to be able to summarize webpage that consist
of a lot of text as well. So, after performing the chunkifying algorithm,
which is by spliting the text into specified-sized groups, the LLM is asked
to summarize each chunk individually and eventually providing the executive
summary out of all the summaries generated previously.


