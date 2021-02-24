import typer
import pandas as pd
import requests
import csv
import pathlib

app = typer.Typer()
API_URL = "https://machinedatahub.ai/datasets.json"
SUGGESTION_FILE = pathlib.Path(".") / "src" / "data" / "suggestions.csv" 


def get_datasets(url):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise typer.click.ClickException(message)


def dataset_names(datasets):
    names = [row["Name"] for row in datasets]
    return names


@app.command("suggest")
def suggest(link: str = typer.Option(..., prompt="Please enter the link to the dataset you want to suggest"),
            name: str = typer.Option(..., prompt="Please enter a name for the dataset at the link you provided"),
            summary: str = typer.Option(..., prompt="Please enter a short summary describing the dataset"),):
    typer.echo(f"{SUGGESTION_FILE}")
    with open(SUGGESTION_FILE, mode="a") as suggestions_file:
        employee_writer = csv.writer(
            suggestions_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        employee_writer.writerow([name, summary, link])
    typer.echo(
        f"Thank you! You have suggested a dataset, {name}, from the following link: {link}"
    )


@app.command("download")
def download(name: str):
    """Download a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if name in dataset_names(datasets):
        typer.echo(f"Downloading {name} right now!")
        url = [row["URL"] for row in datasets if row["Name"] == name][0]
        r = requests.get(url, allow_redirects=True)
        # save content with name
        with open(f"{name}", "wb") as fid:
            fid.write(r.content)
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the name.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")


@app.command("metadata")
def metadata(name: str):
    datasets = get_datasets(API_URL)
    if name in dataset_names(datasets):
        for row in datasets:
            if row["Name"] == name:
                for key in row:
                    info = key + ": " + str(row[key])
                    typer.echo(info)
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the name.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")


@app.command("see-all-datasets")
def list():
    all = ""
    datasets = get_datasets(API_URL)
    for name in dataset_names(datasets):
        all += name
        all += "\n"
    typer.echo(all)


def main():
    app()