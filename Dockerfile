# Use an official Python runtime as the base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /application

# Copy the requirements file

COPY . .

RUN ls -la /application

COPY requirements.txt .

RUN pip install -r requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt
# RUN pip install --no-cache-dir --prefer-binary --ignore-installed -r requirements.txt

# Set the command to run the application
CMD ["python3", "main.py"]
