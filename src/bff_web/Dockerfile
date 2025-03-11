FROM python:3.10
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
ENV PYTHONPATH=/app
EXPOSE 8006