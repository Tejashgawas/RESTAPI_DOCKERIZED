# Use the official Python image
FROM python:3.11-slim-bookworm


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app


# Copy project files
COPY . /app/



# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the app
CMD ["flask", "run", "--host=0.0.0.0"]

