FROM python:3.12
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
EXPOSE 8001
