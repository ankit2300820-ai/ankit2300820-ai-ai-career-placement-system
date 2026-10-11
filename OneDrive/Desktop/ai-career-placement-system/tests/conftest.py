import os, tempfile
# use an isolated temporary SQLite database for tests (set before src.config is imported)
os.environ["DB_BACKEND"] = "sqlite"
os.environ["SQLITE_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")
