import json
import requests
from urllib3.exceptions import InsecureRequestWarning
from jira import JIRA
import logging
from datetime import datetime
import click
import jsonschema
from pathlib import Path

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
logging.basicConfig(format='[%(asctime)s] %(levelname)s - %(message)s',
                    level=logging.INFO)
myts = datetime.now().strftime('%Y_%m_%d')


def savefile(path: Path, basename: str, issues: list):
    def filename(basename) -> str:
        return f'{basename}_{myts}.json'
    with open(path/filename(basename)) as fd:
        json.dump(issues, fd, ensure_ascii=False)


def to_raw(issues):
    return [issue.raw for issue in issues]


def get_issues(jira, jql: str) -> list:
    """Extract issue resulting from `jql`"""
    logging.info(f'retrieve **comments** using jql: "{jql}"')
    issues = jira.search_issues(jql, maxResults=500)
    return to_raw(issues)


def get_comments(jira, jql: str) -> list:
    logging.info(f'retrieve **comments** using jql: "{jql}"')
    comments = jira.search_issues(jql, fields='key,comment', maxResults=500)
    return to_raw(comments)


def validate(config) -> bool:
    conf_schema = """
{
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$ref": "#/definitions/Configuration",
    "definitions": {
        "Configuration": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "endpoint": {
                    "type": "string",
                    "format": "uri",
                    "qt-uri-protocols": [
                        "https"
                    ]
                },
                "jql": {
                    "type": "string"
                }
            },
            "required": [
                "endpoint",
                "jql"
            ],
            "title": "Configuration"
        }
    }
}"""
    schema = json.loads(conf_schema)
    try:
        jsonschema.validate(config, schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        logging.critical("Configuration provided is not correct")
        logging.critical(e)
        return False


@click.command()
@click.argument("config", type=click.File('r'))
@click.argument("path", type=click.Path(exists=True, dir_okay=True))
@click.option('--login', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def cli(config, path, login, password):
    """Dump Jira issue using "config" directive and save result to "path"

    contact:KhalidCK
    """
    savedir = Path(path)
    click.echo(f"Path: {type(path)}")
    config = json.load(config)
    if not validate(config):
        exit()
    jira = JIRA(config["endpoint"], auth=(
        login, password), options={"verify": False})
    issues = get_issues(jira, config['jql'])
    comments = get_comments(jira, config['jql'])
    click.echo(f"save results to {path}")
    savefile(savedir, 'issues', issues)
    savefile(savedir, 'issues', comments)
    return


if __name__ == "__main__":
    cli()
