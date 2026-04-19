FROM python:3.14
WORKDIR /usr/local/alugvps-server

# Application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY src /usr/local/alugvps-server/

# Run in the directory
WORKDIR /usr/local/alugvps-server

CMD ["python3", "alugvps-server.py"]
