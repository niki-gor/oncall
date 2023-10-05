from oncaller.models import Teams
import yaml


def parse_teams_schedule_file(filename: str) -> Teams:
    with open(filename, 'r') as f:
        teams_dict = yaml.safe_load(f)
    return Teams.model_validate(teams_dict)
