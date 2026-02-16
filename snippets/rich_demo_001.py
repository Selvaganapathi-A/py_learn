from collections.abc import Sequence
from typing import cast

from rich import print, style, table
from rich.markdown import Markdown
from rich.pretty import pprint, pretty_repr

__all__ = [
    "pprint",
    "pretty_repr",
]
pprint(__all__)


def table_output(title: str, headings: Sequence[str], rows: Sequence[Sequence[str]]):
    _t = table.Table(
        title=title,
        expand=True,
        *headings,
        style=style.Style(color="blue"),
        show_edge=True,
        show_lines=False,
    )
    for row in rows:
        _t.add_row(*row, style=style.Style(color="black"))
    return _t


def super_print(arg: list[dict[str, str]]):
    md = ""
    title = "| " + " | ".join(("name", "country", "email")) + " | "
    title += "\n| " + " | ".join(("-", "-", "-")) + " | "
    md += title.title()
    for item in arg:
        md += f"\n| {item.get('name')} | {item.get('contact')} | {item.get('country')} | "
    print(Markdown(md))


users: list[dict[str, str]] = [
    {
        "name": "Minerva Watson",
        "country": "Ireland",
        "contact": "kujrobte@epasafil.ao",
    },
    {
        "name": "Dean Boone",
        "country": "Botswana",
        "contact": "elgicdip@micerfir.bo",
    },
    {
        "name": "Helen Lawson",
        "country": "St. Vincent & Grenadines",
        "contact": "hapoowi@favrap.bt",
    },
    {
        "name": "Bertha Reeves",
        "country": "Grenada",
        "contact": "bihab@buwiv.dm",
    },
    {
        "name": "Sam Waters",
        "country": "Morocco",
        "contact": "robusat@givo.bz",
    },
]
print(pretty_repr(users))
pprint(users)
print(users)
contacts = """(744) 312-2153
(285) 232-7560
(875) 809-5711
(221) 788-6980
(245) 854-6286
(555) 378-6910
(970) 815-5619
(558) 563-1500
(389) 253-5158
(330) 713-5970
(250) 768-3166
(903) 952-8544
(437) 670-2103
(920) 213-6729
(649) 365-1202
(933) 241-3252
(467) 338-8228
(387) 241-6468
(280) 950-5987
(302) 293-4019
(440) 853-2356
(943) 968-6162"""

print(Markdown("# Contact Details"))
for contact in contacts.splitlines():
    print("📞", contact)
print()
super_print(users)
print("[red]Hello[/red] Mark! [blue]Maintenance mode Initiated.[/blue]")
print()
print(
    table_output(
        "Users",
        headings=("name", "country", "contact"),
        rows=[cast(Sequence[str], user.values()) for user in users],
    )
)
