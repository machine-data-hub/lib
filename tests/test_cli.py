from typer.testing import CliRunner

# TUTORIAL FROM TYPER
from src.phm_data_hub.cli import app, datasets

#The first parameter to runner.invoke() is a Typer app.
#The second parameter is a list of str, with all the text you would pass in the command line, right as you would pass it:
def test_download():
    runner = CliRunner()
    result = runner.invoke(app, ["download", "Appliances Energy Prediction Data Set"])
    assert result.exit_code == 0
    # this is the slow testing of every dataset
    #for name in datasets['Name']:
        #runner = CliRunner()
        #result = runner.invoke(app, ["download", name])
        #assert result.exit_code == 0
        #assert f"Downloading {name} right now!" in result.stdout

def test_metadata():
    for name in datasets['Name']:
        runner = CliRunner()
        #result = runner.invoke(app, ["download", name])
        result = runner.invoke(app, ["download", "Appliances Energy Prediction Data Set"])
        assert result.exit_code == 0
        #assert f"Downloading {name} right now!" in result.stdout

def test_suggest():
    runner = CliRunner()
    result = runner.invoke(app, ["suggest", "www.google.com"])
    assert result.exit_code == 0

def test_list():
    runner = CliRunner()
    result = runner.invoke(app, ["see-all-datasets"])
    assert result.exit_code == 0