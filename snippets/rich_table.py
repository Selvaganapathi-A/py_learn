import faker
from rich import print
from rich.console import Console
from rich.padding import Padding
from rich.prompt import Prompt
from rich.table import Table


def main():
    test = Padding("Hello", 5)
    print(test)
    table_title = Prompt.ask("Enter Table Title:-")
    table = Table(title=table_title)
    table.add_column("Name", style="blue", justify="right")
    table.add_column(
        "Contact",
        style="#ff4444",
        justify="center",
        header_style="#ff00ff",
    )
    table.add_column("Country", style="blue", justify="center")
    table.add_row(
        "Harriet Bridges", "(500) 422-1867", "Antigua & Barbuda"
    )
    table.add_row(
        "Sara Keller", "(824) 699-3363", "São Tomé and Príncipe"
    )
    table.add_row("Rosie Miller", "(657) 597-5913", "Russia")
    table.add_row("Marion Miles", "(771) 842-7593", "Peru")
    table.add_row("Isaac Rios", "(725) 472-6791", "Zimbabwe")
    table.add_row("Albert Roberson", "(480) 755-6643", "Ghana")

    console = Console()
    console.print(table)

    pass


if __name__ == "__main__":
    # main()
    fake = faker.Faker()

    print(dir(fake))
    table = Table()
    for x in range(20):
        table.add_row(
            f"{x+1: >3}",
            fake.name_female(),
            fake.email(),
            fake.street_address(),
            fake.street_name(),
            fake.city(),
            fake.state(),
        )
    print(table)

    pass
#                       Student Details
# ┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃            Name ┃    Contact     ┃        Country        ┃
# ┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━┩
# │ Harriet Bridges │ (500) 422-1867 │   Antigua & Barbuda   │
# │     Sara Keller │ (824) 699-3363 │ São Tomé and Príncipe │
# │    Rosie Miller │ (657) 597-5913 │        Russia         │
# │    Marion Miles │ (771) 842-7593 │         Peru          │
# │      Isaac Rios │ (725) 472-6791 │       Zimbabwe        │
# │ Albert Roberson │ (480) 755-6643 │         Ghana         │
# └─────────────────┴────────────────┴───────────────────────┘
