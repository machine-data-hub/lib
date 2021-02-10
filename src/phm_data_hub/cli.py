import typer
import pandas as pd
import requests
import csv

app = typer.Typer()

datasets = pd.read_csv('/Users/ceciliabarnes/Documents/Capstone/lib/src/data/datasets.csv')
#print(datasets.head())

@app.command("suggest")
def suggest(link: str):
    with open('/Users/ceciliabarnes/Documents/Capstone/lib/src/data/suggestions.csv', mode='a') as suggestions_file:
        employee_writer = csv.writer(suggestions_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        employee_writer.writerow([link])
    typer.echo(f"Thank you! You have suggested a dataset from the following link: {link}")

@app.command("download")
def download(name: str):
    """Download a dataset by passing in the name. """
    if name in datasets.values:
        typer.echo(f"Downloading {name} right now!")
        row = datasets[datasets['Name'] == name]
        url = row['Link to download'].values.tolist()[0]
        r = requests.get(url, allow_redirects=True)
        print("success in retrieving html")
        # save content with name
        open(name, 'wb').write(r.content)
    else:
        typer.echo("That dataset doesn't exist or you've made a type in the name.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")

@app.command("metadata")
def metadata(name: str):
    if name in datasets.values:
        row = datasets[datasets['Name'] == name]
        info = ""
        for col in datasets.columns:
            info += col
            info += ": "
            info += str(row[col][0])
            info += "\n"
        typer.echo(info)
    else:
        typer.echo("That dataset doesn't exist or you've made a type in the name.")
        typer.echo("Use the 'see all datasets' command to view the available datasets.")

@app.command("see-all-datasets")
def list():
    all = ""
    for name in datasets["Name"]:
        all += name
        all += "\n"
    typer.echo(all)

if __name__ == "__main__":
    app()