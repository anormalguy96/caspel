from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT current_user, current_database()")
    )

    print(result.one())