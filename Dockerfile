FROM python:3.11-slim

# Set the working directory to the container root
WORKDIR /code

# Copy just the backend requirements first to leverage Docker cache
COPY ./backend/requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire backend source code to the container
COPY ./backend /code/backend

# Set huggingface spaces standard port
EXPOSE 7860

# Switch the working directory into backend so Jinja2 templates resolve correctly
WORKDIR /code/backend

# Run the FastAPI server natively on 0.0.0.0 and port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
