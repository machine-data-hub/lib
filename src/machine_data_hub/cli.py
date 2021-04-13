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
    #names = []
    #for row in datasets:
    #    dataset_links = row["Datasets"]
    #    if len(dataset_links) > 1: # if there's more than 1 download link
    #        for i in range(len(dataset_links)):
    #            names.append(row["Name"] + " " + str(i + 1))
    #    else:
    #        names.append(row["Name"])
    names = [row["Name"] for row in datasets]
    return names


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
def download(name: str):
    """Download a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if name in dataset_names(datasets):
        for row in datasets:
            if row["Name"] == name:
                dataset_links = row["Datasets"]
        num_datasets = len(dataset_links)
        if num_datasets > 1:
            response = input("This dataset has " + str(num_datasets) + " different files. Do you want to download them all? (y/n) ")
            if response == "y":
                for i, each in enumerate(dataset_links):
                    typer.echo(f"Downloading {name} file {i} right now!")
                    url = each["URL"]
                    r = requests.get(url, allow_redirects=True)
                    # save content with name
                    with open(f"{name}", "wb") as fid:
                        fid.write(r.content)
            elif response == "n":
                data_to_download = input("Enter a list of integers from 0-" + str(num_datasets - 1) + " to download those files. ")
                data_to_download = data_to_download.strip("[]").split(",")
                typer.echo("Downloading files now!")
                for each in data_to_download:
                    url = dataset_links[int(each)]["URL"]
                    r = requests.get(url, allow_redirects=True)
                    with open(f"{name} {each}", "wb") as fid:
                        fid.write(r.content)
            else:
                typer.echo("Please type y for yes or n for no.")
                url = dataset_links[0]["URL"]
                r = requests.get(url, allow_redirects=True)
                with open(f"{name}", "wb") as fid:
                    fid.write(r.content)
        else:
            typer.echo("Downloading files now!")
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the name.")
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