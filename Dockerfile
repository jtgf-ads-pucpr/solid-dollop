FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir "fastapi[standard]" && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]