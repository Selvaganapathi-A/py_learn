from models import Association, Base, Child, Parent
from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm.session import Session, sessionmaker


def workarea(session: Session):
    # * Create Parent Objects
    billy = Parent(first_name='Billy', last_name='M')
    tom = Parent(first_name='Tom', last_name='Holland')
    laurel = Parent(first_name='Laurel', last_name='Jack')
    brittany = Parent(first_name='Brittany', last_name='Bethrolis')
    daisy = Parent(first_name='Daisy', last_name='Haze')
    #
    # * Create Child Objects
    ashley = Child(first_name='Ashley', last_name='Billy')
    james = Child(first_name='James', last_name='Tom')
    miranda = Child(first_name='Miranda', last_name='Daisy')
    #
    # * Add Child Objects to Parents
    association = Association()
    association.child = ashley
    billy.children.add(association)
    #
    association = Association()
    association.child = ashley
    laurel.children.add(association)
    #
    association = Association()
    association.child = james
    billy.children.add(association)
    #
    association = Association()
    association.child = james
    daisy.children.add(association)
    #
    association = Association()
    association.child = miranda
    tom.children.add(association)
    #
    association = Association()
    association.child = miranda
    brittany.children.add(association)
    #
    session.add(billy)
    session.add(tom)
    session.add(laurel)
    session.add(brittany)
    session.add(daisy)
    session.commit()
    #
    # * Parent Child Relationship
    result = (
        session.execute(
            select(Parent).order_by(Parent.last_name, Parent.first_name)
        )
        .scalars()
        .all()
    )
    for parent in result:
        print(parent.first_name + '-' + parent.last_name)
        for child in parent.children:
            print('->>' + child.child.first_name + ' ' + child.child.last_name)
    print('-' * 80)
    #
    # * Child Parent Relationship
    result = session.execute(select(Child)).scalars().all()
    for child in result:
        print(child.first_name + ' ' + child.last_name)
        for parent in child.parents:
            print(
                '  =>',
                parent.parent.first_name + ' ' + parent.parent.last_name,
            )


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
