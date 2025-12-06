import typer

from account.common.utils.seed_db import seed_db as insert_account_db_data

app = typer.Typer()


@app.command()
def seed_db():
    insert_account_db_data()


@app.command()
def dummy_data():
    print("Dummy Data")


if __name__ == "__main__":
    app()
