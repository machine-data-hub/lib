import typer

app = typer.Typer()

datasets = {"Combined Cycle Power Plant Data Set": {"Link":"https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip",
                                                "Data Set Characteristics":"Multivariate",
                                                "Associated Tasks":"Regression",
                                                "Number of Instances": 9568,
                                                "Number of Attributes": 4,
                                                "Missing Values?":"N/A",
                                                "Date Donated":"2014-03-26",
                                                "Number of Web Hits":191037}}
suggestions = []
@app.command("suggest")
def hello(link: str):
    suggestion = link
    typer.echo(f"Thank you! You have suggested a dataset from the following link: {link}")

@app.command("dataset")
def dataset(action: str, name: str):
    """You can directly download the full dataset by passing "download" for the action argument.
        If you'd rather view the dataset's metadata, pass "get info" for the action argument.
    """
    if action == "download":
        if name in datasets.keys():
            typer.echo(f"Downloading {name} as zip file")
            typer.launch(datasets.get(name).get("Link"))
            #typer.launch("https://archive.ics.uci.edu/ml/machine-learning-databases/00294/CCPP.zip")
    elif action == "get info":
        info = ""
        for key in datasets.get(name).keys():
            info += key
            info += ": "
            info += str(datasets.get(name).get(key))
            info += "\n"
        typer.echo(info)
        #typer.echo("Taking you to view parent directory")
        #typer.launch("https://archive.ics.uci.edu/ml/machine-learning-databases/")


if __name__ == "__main__":
    app()