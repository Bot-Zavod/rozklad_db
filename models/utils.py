def truncate_db(engine):
    """ delete all table data (but keep tables) """

    print("\nStarting cleaning database\n")

    con = engine.connect()
    trans = con.begin()
    # sorted by foreing keys in reverse
    for table in reversed(Base.metadata.sorted_tables):
        print(f"Cleaning '{table}' table")
        con.execute(table.delete())
    trans.commit()

    print("\nCleaning database finished\n\n")


def migrate_db_cloud():
    """ transfers table data from SQLite to PostrgeSQL """

    engine_lite = create_engine(sqlite_uri)
    engine_postgres = create_engine(postgres_uri)

    # Base.metadata.drop_all(engine_postgres)  # deletes all tables and data
    truncate_db(engine_postgres)
    # Base.metadata.create_all(engine_postgres)

    conn_lite = engine_lite.connect()
    conn_cloud = engine_postgres.connect()

    tables = Base.metadata.sorted_tables
    pbar = progressbar.ProgressBar()

    print(f"Transfering database to cloud")

    for table in pbar(tables):
        data = [dict(row) for row in conn_lite.execute(select(table.c))]
        conn_cloud.execute(table.insert().values(data))