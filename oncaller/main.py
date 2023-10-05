import argparse
import asyncio

from oncaller import api_requests
from oncaller.config import Config
from oncaller.parser import parse_teams_schedule_file


def main():
    config = Config()

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="configs/schedule.yml")
    args = parser.parse_args()

    teams = parse_teams_schedule_file(args.filename)
    asyncio.run(
        api_requests.set_teams_schedule(
            host=config.host,
            username=config.username,
            password=config.password,
            teams=teams.teams,
        )
    )
