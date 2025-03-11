import argparse
import csv
import uuid
import asyncio
import httpx
import datetime
import time
from config import BFF_HOST, INGESTION_HOST
import subprocess

JSON_HEADER = {"Content-Type": "application/json"}

all_tokens = set()
tokens_with_sync = set()


async def login_and_ingest(client):
    # Login and get token
    print("Login")
    response = await client.get(f"{BFF_HOST}/auth/generate_token", headers=JSON_HEADER)
    provider_id = response.json().get("token")
    all_tokens.add(provider_id)
    print(f"Provider {provider_id} logged in")

    # Set authorization header
    headers = {"Authorization": f"Bearer {provider_id}"}
    headers.update(JSON_HEADER)

    # Call ingestion endpoint
    correlation_id = str(uuid.uuid4())
    result = await client.post(
        f"{BFF_HOST}/ingestion/data-intakes",
        headers=headers,
        json={
            "correlation_id": correlation_id,
            "provider_id": provider_id,
        },
    )
    assert result.status_code == 200
    # Veryfy sync/completed has started
    while True:
        response = await client.get(
            f"{BFF_HOST}/ingestion/data-intakes",
            headers=headers,
            params={"provider_id": provider_id},
        )
        if response.status_code != 200:
            continue
        json_result = response.json()
        if len(json_result) <= 0:
            continue
        if json_result[0]["status"] in ["IN_PROGRESS", "COMPLETED"]:
            tokens_with_sync.add(provider_id)
            return
        await asyncio.sleep(0.5)


async def main(num_users, timeout):
    async with httpx.AsyncClient() as client:
        # Reset ingestion database
        try:
            tasks = [
                asyncio.wait_for(login_and_ingest(client), timeout)
                for _ in range(num_users)
            ]
            await asyncio.gather(*tasks)
        except asyncio.TimeoutError:
            print(f"Timeout of {timeout} seconds reached")

    # Check if all tokens have sync
    print("Users created %d" % len(all_tokens))
    print("Users with sync %d" % len(tokens_with_sync))
    print("Users without sync %d" % (len(all_tokens) - len(tokens_with_sync)))
    # Write to CSV
    csv_title = f"results/{num_users}_{timeout}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    # Create directory if not exists
    subprocess.run(f"mkdir -p results", shell=True, check=True)
    with open(csv_title, mode="w") as file:
        writer = csv.writer(file)
        writer.writerow(["Provider ID", "Has Sync"])
        for token in all_tokens:
            writer.writerow([token, token in tokens_with_sync])
    all_tokens.clear()
    tokens_with_sync.clear()


def execute_docker_commands():
    commands = [
        "docker compose exec ingestion celery -A celery_worker purge -f",
        "docker compose restart ingestion_worker",
        "docker compose exec canonization celery -A celery_worker purge -f",
        "docker compose restart canonization_worker",
    ]
    for command in commands:
        subprocess.run(
            command,
            shell=True,
            check=True,
            cwd="/Users/work/Documents/school/STA-SALUD-TECH",
        )

    # Handle Pulsar topics separately
    try:
        result = subprocess.run(
            "docker compose exec broker /pulsar/bin/pulsar-admin topics list public/default",
            shell=True,
            check=True,
            capture_output=True,
            cwd="/Users/work/Documents/school/STA-SALUD-TECH",
        )
        topics = result.stdout.decode().splitlines()
        for topic in topics:
            subprocess.run(
                f"docker compose exec broker /pulsar/bin/pulsar-admin topics delete {topic}",
                shell=True,
                check=True,
                cwd="/Users/work/Documents/school/STA-SALUD-TECH",
            )
    except subprocess.CalledProcessError as e:
        print(f"Error handling Pulsar topics: {e}")


for users in [1, 10, 50, 100, 200]:
    for i in range(3):
        execute_docker_commands()
        asyncio.run(main(users, 60))
        print(f"Finished {users} users {i+1} times")
