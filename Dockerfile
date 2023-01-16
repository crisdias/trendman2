FROM python:3.8

# Create a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required libraries
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Set the entrypoint
ENTRYPOINT ["python", "-u", "bot.py"]
