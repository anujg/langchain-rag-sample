# LangChain Based RAG

This is a web application which is using a Pinecone as a vectorsotre and answers questions using the documents uploaded via the web UI.
Please note that, to keep things simple, the documents are not saved in the backend, but just used temporarily.

## Tech Stack

Client: Streamlit

Server Side: LangChain 🦜🔗

Vectorstore: Pinecone 🌲

LLM: OpenAI

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PINECONE_API_KEY`
`OPENAI_API_KEY`

## Run Locally

Install dependencies

```bash
  pipenv install
```

Start the flask server

```bash
  streamlit run main.py
```

## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```
