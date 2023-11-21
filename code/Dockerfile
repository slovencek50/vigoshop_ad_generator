# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the OpenAI API key
ENV OPENAI_API_KEY=


# Copy the current directory contents into the container at /app
COPY . /app/
EXPOSE 5000
# Run app.py when the container launches
CMD ["python", "app.py"]
