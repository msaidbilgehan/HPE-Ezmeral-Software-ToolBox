FROM python:3.9-slim-buster
ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST="0.0.0.0"
ENV PORT=5010

EXPOSE ${PORT}

RUN ls -la
CMD ["python",  "-u", "flask_app.py"]
