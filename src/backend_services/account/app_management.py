import typer

from account.common.utils.seed_db import seed_db as insert_db_data

from utils.app_services.account import db_settings, db_url_obj

app = typer.Typer()


@app.command()
def seed_db():
    insert_db_data(db_url_obj, db_settings)


if __name__ == "__main__":
    app()
