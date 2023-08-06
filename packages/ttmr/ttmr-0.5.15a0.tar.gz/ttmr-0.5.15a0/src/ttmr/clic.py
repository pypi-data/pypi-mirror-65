import typer


app = typer.Typer()


@app.command()
def current():
    pass

@app.command()
def start():
    pass


@app.command()
def stop():
    pass


@app.command()
def view():
    pass


@app.command()
def summary(day: bool = False, week: bool = False):
    print("calling summary...")
    print(f"day: {day}")
    print(f"week: {week}")


@app.command()
def weekly():
    pass


@app.command()
def new():
    pass


@app.command()
def list():
    pass


def main():
    app()

