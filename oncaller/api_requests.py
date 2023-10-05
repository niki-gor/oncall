import asyncio
import logging
from datetime import timedelta

import httpx

from oncaller.models import Team

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def send_many(f):
    async def wrapper(client: httpx.AsyncClient, teams: list[Team]):
        coroutines = []
        for team in teams:
            coroutines.extend(f(client, team))
        responses = await asyncio.gather(*coroutines)
        for response in responses:
            logger.info(
                f"{response.request.url} {response.status_code} {response.content}"
            )

    return wrapper


@send_many
def create_teams(client: httpx.AsyncClient, team: Team):
    return [client.post("/teams", data=team.model_dump_json(exclude="users"))]


@send_many
def create_team_rosters(client: httpx.AsyncClient, team: Team):
    roster_name = team.name
    return [client.post(f"/teams/{team.name}/rosters", json={"name": roster_name})]


@send_many
def create_users(client: httpx.AsyncClient, team: Team):
    return [client.post("/users", json={"name": user.name}) for user in team.users]


@send_many
def update_users(client: httpx.AsyncClient, team: Team):
    return [
        client.put(
            f"/users/{user.name}",
            json={
                "name": user.name,
                "full_name": user.full_name,
                "contacts": {
                    "call": user.phone_number,
                    "email": user.email,
                    "sms": user.phone_number,
                },
            },
        )
        for user in team.users
    ]


@send_many
def add_users_to_rosters(client: httpx.AsyncClient, team: Team):
    roster_name = team.name
    return [
        client.post(
            f"/teams/{team.name}/rosters/{roster_name}/users",
            json={"name": user.name},
        )
        for user in team.users
    ]


@send_many
def create_events(client: httpx.AsyncClient, team: Team):
    result = []
    for user in team.users:
        for duty in user.duty:
            request = client.post(
                "/events",
                json={
                    "team": team.name,
                    "user": user.name,
                    "role": duty.role,
                    "start": duty.date,
                    "end": duty.date + int(timedelta(days=1).total_seconds()),
                },
            )
            result.append(request)
    return result


def login(host: str, username: str, password: str) -> httpx.AsyncClient:
    content = f"username={username}&password={password}"
    response = httpx.post(f"{host}/login", content=content)
    cookies = {"oncall-auth": response.cookies["oncall-auth"]}
    headers = {"X-Csrf-Token": response.json()["csrf_token"]}
    return httpx.AsyncClient(headers=headers, cookies=cookies)


async def set_teams_schedule(
    host: str, username: str, password: str, teams: list[Team]
):
    client = login(host, username, password)
    client.base_url = f"{host}/api/v0"
    async with client:
        await create_teams(client, teams)
        await create_team_rosters(client, teams)
        await create_users(client, teams)
        await update_users(client, teams)
        await add_users_to_rosters(client, teams)
        await create_events(client, teams)
