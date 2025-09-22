from models import Base, Child, Parent
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm.session import Session, sessionmaker


def workarea(session: Session):
    adam = Parent(name='Adam')
    jenifer = Child(name='jenifer')
    adam.child = jenifer
    session.add(adam)
    # # ! below code raises error...
    jerry = Parent(name='Jerry')
    jerry.child = jenifer
    session.add(jerry)
    # #
    session.commit()
    #
    for prsn in session.execute(select(Parent)).scalars().all():
        print(prsn.pk, prsn.name)
        child = prsn.child
        if child is None:
            print('[]')
        else:
            print(child.name)
        print('-' * 80)


def main():
    session: Session
    engine: Engine = create_engine('sqlite:///:memory:', echo=False)
    #
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    #
    sessionLocal = sessionmaker(bind=engine)
    session = sessionLocal()
    #
    workarea(session=session)
    #
    session.commit()
    #
    engine.dispose()


if __name__ == '__main__':
    main()
