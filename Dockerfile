FROM python:3.10-slim


# Install gcc
RUN apt-get update -y \
  && apt-get install -y python3-dev \
  gcc \
  libc-dev \
  libffi-dev

WORKDIR /app

# RUN git clone https://github.com/streamlit/streamlit-example.git .

# RUN pip3 install -r requirements.txt

COPY Pipfile .

RUN  pip install pipenv && pipenv install --deploy --ignore-pipfile

COPY . .

ARG OPENAI_API_KEY
ARG PINECONE_API_KEY

EXPOSE 8501

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS false"]