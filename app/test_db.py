from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "DATABASE_URL"  # copy from your .env or config

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_query():
    session = SessionLocal()
    try:
        sql = "SELECT * FROM employees LIMIT 1"
        result = session.execute(text(sql))
        row = result.fetchone()
        print("DB test query result:", row)
    except Exception as e:
        print("DB connection or query error:", e)
    finally:
        session.close()

if __name__ == "__main__":
    test_query()
