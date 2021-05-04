import typer
import json
import requests
import datetime

app = typer.Typer()
API_URL = "https://machinedatahub.ai/datasets.json"
SILLYSTRING = 'ZJBsQTFUy40aKy0tqieJghp_8ZGng8jE27uqBeRD'
TOKEN = SILLYSTRING[20:] + SILLYSTRING[0:20]


def get_datasets(url):
    try:
        with requests.get(url) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise typer.click.ClickException(message)


def dataset_names(datasets):
    list_data = []
    for row in datasets:
        id = str(row["id"])
        name = row["Name"]
        num = str(len(row["Datasets"]))
        sizes = [file["File Size"] for file in row["Datasets"]]
        output = id + " " + name + " (" + num + " files, "
        x = ', '.join(sizes)
        output += x
        output += ")"
        list_data.append(output)

    #names = [str(row["id"]) + " " + row["Name"] + " (" + str(len(row["Datasets"])) + " files,)" for row in datasets]
    return list_data

def dataset_ids(datasets):
    ids = [int(row['id']) for row in datasets]
    return ids


@app.command("suggest")
def suggest(name: str, link: str, summary: str):
    """Suggest a dataset to be added to the Machine Data Hub by giving a link, name, and summary. """
    org = "PHM-Data-Hub"
    team_slug = "uw-capstone-team"
    discussion_number = 1
    date_time = str(datetime.date().today()) + " " + str(datetime.now())
    body = " ### " + name + "\n" + date_time + "\n\n**Summary:** " + summary + "\n**Link:** " + link
    query_url = f"https://api.github.com/orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments"
    data = {
        "body": body
    }
    headers = {'Authorization': f'token {TOKEN}'}
    r = requests.post(query_url, headers=headers, data=json.dumps(data))
    typer.echo(r.json())
    typer.echo(
        f"Thank you! You have suggested a dataset, {name}, from the following link: {link}"
    )


@app.command("download")
def download(id: int, file: int = typer.Argument(None)):
    """Download a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if id in dataset_ids(datasets):
        for row in datasets:
            if int(row["id"]) == id:
                name = row["Name"] # saving name of dataset

                # if optional argument is passed
                if file:
                    # making sure that the file passed exists for the specified dataset
                    if file > len(row["Datasets"]):
                        typer.echo("The dataset you selected does not have that file.")
                    else:
                        url = row["Datasets"][file]["URL"]
                        r = requests.get(url, allow_redirects=True)
                        with open(f"{name}", "wb") as fid:
                            fid.write(r.content)

                # if no file is specified, download all files
                else:
                    urls = [data["URL"] for data in row["Datasets"]]
                    typer.echo("Downloading files now!")
                    for url in urls:
                        r = requests.get(url, allow_redirects=True)
                        with open(f"{name}", "wb") as fid:
                            fid.write(r.content)
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the id.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")


@app.command("metadata")
def metadata(id: int):
    """View the metadata for a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if id in dataset_ids(datasets):
        for row in datasets:
            if int(row["id"]) == id:
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