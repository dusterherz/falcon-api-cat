if __name__ == "__main__":
    from sqlalchemy import create_engine
    from models.config import Base

    engine = create_engine(
        'postgresql://postgres:catsareawesome@localhost:4321/postgres')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
