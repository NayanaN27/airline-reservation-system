import os
import pathlib
import pymysql

ROOT = pathlib.Path(__file__).resolve().parents[1]

def run_sql_file(cur, path: pathlib.Path):
    sql = path.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    for stmt in statements:
        cur.execute(stmt)

def main():
    host = os.getenv("TEST_DB_HOST", "localhost")
    user = os.getenv("TEST_DB_USER", "airuser")
    password = os.getenv("TEST_DB_PASSWORD", "StrongPassword123!")
    db_name = os.getenv("TEST_DB_NAME", "air")

    air_sql = ROOT / "air.sql"
    seed_sql = ROOT / "seed.sql"

    if not air_sql.exists():
        raise SystemExit(f"Missing {air_sql}")
    if not seed_sql.exists():
        raise SystemExit(f"Missing {seed_sql}")

    conn = pymysql.connect(host=host, user=user, password=password, autocommit=True)
    try:
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS `{db_name}`")
            cur.execute(f"CREATE DATABASE `{db_name}` DEFAULT CHARACTER SET latin1")
            cur.execute(f"USE `{db_name}`")
            run_sql_file(cur, air_sql)
            run_sql_file(cur, seed_sql)
    finally:
        conn.close()

    print(f"Reset + seeded test database: {db_name}")

if __name__ == "__main__":
    main()