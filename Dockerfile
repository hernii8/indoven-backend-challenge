FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive 
SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    software-properties-common \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository -y ppa:deadsnakes/ppa 
RUN apt-get install -y python3.10

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3.10 -
ENV PATH="~/.local/bin/:$PATH"

# Set working directory
WORKDIR /idoven-backend-challenge

# Copy project files
COPY . .

# Install project dependencies
ENV POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME='/usr/local'
RUN  poetry install --no-interaction --no-ansi

EXPOSE 8000

# Run! 🚀
CMD ["python3.10", "server.py"]
