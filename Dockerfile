FROM python:3.10-slim


# Install gcc
RUN apt-get update -y \
  && apt-get install -y python3-dev \
  gcc \
  libc-dev \
  libffi-dev

WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy the pyproject.toml (and possibly poetry.lock) file to the container
COPY pyproject.toml /app/

# Install dependencies via poetry
RUN poetry config virtualenvs.create false \
  && poetry install

# Copy the rest of your application's code
COPY . /app/

ARG OPENAI_API_KEY
ARG PINECONE_API_KEY

EXPOSE 8080

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD streamlit run main.py --server.port=8080 --browser.serverAddress="0.0.0.0"