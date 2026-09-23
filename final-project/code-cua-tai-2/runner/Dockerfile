FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends g++ && rm -rf /var/lib/apt/lists/* && useradd --create-home --uid 10001 runner
WORKDIR /app
ENV RUNNER_WORKDIR=/workspace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY runner.py .
USER runner
EXPOSE 8010
CMD ["uvicorn", "runner:app", "--host", "0.0.0.0", "--port", "8010"]
