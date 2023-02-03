FROM python:3.7.9-slim

WORKDIR /app

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

EXPOSE 3030

CMD ["python", "DDos.py"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]

