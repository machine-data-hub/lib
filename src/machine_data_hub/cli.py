import typer
import json
import requests
import datetime
from tabulate import tabulate
from tqdm import tqdm
import rfc6266
import os
import textwrap

app = typer.Typer()
API_URL = "https://machinedatahub.ai/datasets.json"
SILLYSTRING = "ZJBsQTFUy40aKy0tqieJghp_8ZGng8jE27uqBeRD"
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
    names = [
        str(row["id"])
        + " "
        + row["Name"]
        + " ("
        + str(len(row["Datasets"]))
        + " files, "
        + row["FileSize"]
        + ")"
        for row in datasets
    ]
    return names


def dataset_ids(datasets):
    ids = [int(row["id"]) for row in datasets]
    return ids


@app.command("suggest")
def suggest(name: str, link: str, summary: str):
    """Suggest a dataset to be added to the Machine Data Hub by giving a link, name, and summary. """
    org = "PHM-Data-Hub"
    team_slug = "uw-capstone-team"
    discussion_number = 1
    date_time = str(datetime.date.today()) + " " + str(datetime.datetime.now().time())
    body = (
        " ### "
        + name
        + "\n"
        + date_time
        + "\n\n**Summary:** "
        + summary
        + "\n**Link:** "
        + link
        + "\n\nSubmitted from command line interface"
    )
    query_url = f"https://api.github.com/orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments"
    data = {"body": body}
    headers = {"Authorization": f"token {TOKEN}"}
    r = requests.post(query_url, headers=headers, data=json.dumps(data))
    typer.echo(
        f"Thank you! You have suggested a dataset, {name}, from the following link: {link}"
    )


@app.command("download")
def download(id: int, file: int = typer.Argument(None)):
    """Download a dataset by passing in the dataset id and optionally the file number. """
    datasets = get_datasets(API_URL)

    # if dataset id exists
    if id in dataset_ids(datasets):
        # loop through each dataset
        for row in datasets:
            # find the dataset with given id
            if int(row["id"]) == id:

                # make directory in the format of id_DatasetName
                id = row["id"]
                name = row["Name"]
                dest_folder = f"{id}_{name.replace(' ','')}"
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)

                # if optional argument is passed to download specified file
                if not (file is None):
                    # making sure that the file passed exists for the specified dataset
                    file_index = (
                        file - 1
                    )  # converting user input into proper python indexing
                    if file_index > len(row["Datasets"]) or file_index < 0:
                        typer.echo("The dataset you selected does not have that file.")
                    else:
                        # getting download URL
                        url = row["Datasets"][file_index]["URL"]
                        r = requests.get(url, allow_redirects=True, stream=True)

                        # getting individual file's name
                        filename = rfc6266.parse_requests_response(r).filename_unsafe
                        file_path = os.path.join(dest_folder, filename)

                        typer.echo("Downloading file now!")
                        # loading bar code from stack overflow
                        # https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests/37573701#37573701
                        total_size_in_bytes = int(r.headers.get("content-length", 0))
                        block_size = 1024  # 1 Kibibyte
                        progress_bar = tqdm(
                            total=total_size_in_bytes, unit="iB", unit_scale=True
                        )

                        # saving file
                        with open(file_path, "wb") as fid:
                            for data in r.iter_content(block_size):
                                progress_bar.update(len(data))
                                fid.write(data)
                        progress_bar.close()
                # if no file is specified, download all files
                else:
                    urls = [data["URL"] for data in row["Datasets"]]
                    typer.echo("Downloading files now!")
                    for i, url in enumerate(urls):
                        r = requests.get(url, allow_redirects=True, stream=True)
                        filename = rfc6266.parse_requests_response(r).filename_unsafe
                        file_path = os.path.join(dest_folder, filename)
                        total_size_in_bytes = int(r.headers.get("content-length", 0))
                        block_size = 1024  # 1 Kibibyte
                        progress_bar = tqdm(
                            total=total_size_in_bytes, unit="iB", unit_scale=True
                        )
                        with open(file_path, "wb") as fid:
                            for data in r.iter_content(block_size):
                                progress_bar.update(len(data))
                                fid.write(data)
                        progress_bar.close()
    # if dataset id doesnt exist
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the id.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")


@app.command("metadata")
def metadata(id: int):
    """View the metadata for a dataset by passing in the id. """
    datasets = get_datasets(API_URL)
    if id in dataset_ids(datasets):
        for row in datasets:
            if int(row["id"]) == id:
                table = []
                for key in row:
                    if key == "Datasets":
                        set = row["Datasets"]
                        for each in set:
                            set_url = each["URL"]
                            if len(set_url) > 40:
                                sep = "\n"
                                each["URL"] = sep.join(textwrap.wrap(set_url, width=40))
                        info = [
                            key,
                            tabulate(
                                set,
                                headers={
                                    "Name": "Name",
                                    "URL": "URL",
                                    "Likes": "Likes",
                                    "Downloads": "Downloads",
                                    "File Size": "File Size",
                                },
                            ),
                        ]
                        table.append(info)
                    elif (
                        key == "img_link"
                        or key == "Summary"
                        or key == "URL"
                        or key == "Rank"
                    ):
                        pass
                    else:
                        info = [key, row[key]]
                        table.append(info)
                typer.echo(tabulate(table))
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
