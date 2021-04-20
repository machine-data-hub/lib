import typer
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
    names = [str(row["id"]) + " " + row["Name"] + " (" + str(len(row["Datasets"])) + " files)" for row in datasets]
    return names

def dataset_ids(datasets):
    ids = [int(row['id']) for row in datasets]
    return ids


@app.command("suggest")
def suggest(link: str = typer.Option(..., prompt="Please enter the link to the dataset you want to suggest"),
            name: str = typer.Option(..., prompt="Please enter a name for the dataset at the link you provided"),
            summary: str = typer.Option(..., prompt="Please enter a short summary describing the dataset"),):
    """Suggest a dataset to be added to the Machine Data Hub by giving a link, name, and summary. """
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
def download(id: int, file: int = typer.Argument(None)):
    """Download a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if id in dataset_ids(datasets):
        for row in datasets:
            url = ""
            if int(row["id"]) == id:
                name = row["Name"] # saving name of dataset

                # if optional argument is passed
                if file:
                    # making sure that the file passed exists for the specified dataset
                    if file > len(row["Datasets"]):
                        typer.echo("The dataset you selected does not have that file.")
                    else:
                        url = row["Datasets"][file]["URL"]

                # if no file is specified, download first file
                else:
                    url = row["Datasets"][0]["URL"]
                if url != "":
                    typer.echo("Downloading files now!")
                    r = requests.get(url, allow_redirects=True)
                    with open(f"{name}", "wb") as fid:
                        fid.write(r.content)
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the id.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")


@app.command("metadata")
def metadata(name: str):
    """View the metadata for a dataset by passing in the name. """
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


@app.command("list")
def list():
    """View list of all datasets available. """
    all = ""
    datasets = get_datasets(API_URL)
    for name in dataset_names(datasets):
        all += name
        all += "\n"
    typer.echo(all)


def main():
    app()