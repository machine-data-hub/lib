import typer
import pandas as pd
import requests
import csv

app = typer.Typer()
API_URL = 'https://deploy-preview-24--quirky-meninsky-24e642.netlify.app/datasets.json'

def get_datasets(url):
    response = requests.get(url)
    datasets = response.json()
    return datasets

def dataset_names(datasets):
    names = [row['Name'] for row in datasets]
    return names

@app.command("suggest")
def suggest(link: str):
    with open('/Users/ceciliabarnes/Documents/Capstone/lib/src/data/suggestions.csv', mode='a') as suggestions_file:
        employee_writer = csv.writer(suggestions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([link])
    typer.echo(f"Thank you! You have suggested a dataset from the following link: {link}")

@app.command("download")
def download(name: str):
    """Download a dataset by passing in the name. """
    datasets = get_datasets(API_URL)
    if name in dataset_names(datasets):
        typer.echo(f"Downloading {name} right now!")
        url =  [row["URL"] for row in datasets if row["Name"] == name][0]
        r = requests.get(url, allow_redirects=True)
        # save content with name
        dest = '/Users/ceciliabarnes/Downloads/' + name
        open(dest, 'wb').write(r.content)
    else:
        typer.echo("That dataset doesn't exist or you've made a typo in the name.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")

@app.command("metadata")
def metadata(name: str):
    datasets = get_datasets(API_URL)
    if name in dataset_names(datasets):
        for row in datasets:
            if row['Name'] == name:
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