from rich import print
from rich.markdown import Markdown
from rich.pretty import pprint, pretty_repr

__all__ = [
    'pprint',
    'pretty_repr',
]
pprint(__all__)


def super_print(arg: list[dict[str, str]]):
    md = ''
    title = '| ' + ' | '.join(('name', 'country', 'email')) + ' | '
    title += '\n| ' + ' | '.join(('-', '-', '-')) + ' | '
    md += title.title()
    for item in arg:
        md += f"\n| {item.get('name')} | {item.get('contact')} | {item.get('country')} | "
    print(Markdown(md))


users = [
    {
        'name': 'Minerva Watson',
        'country': 'Ireland',
        'contact': 'kujrobte@epasafil.ao',
    },
    {
        'name': 'Dean Boone',
        'country': 'Botswana',
        'contact': 'elgicdip@micerfir.bo',
    },
    {
        'name': 'Helen Lawson',
        'country': 'St. Vincent & Grenadines',
        'contact': 'hapoowi@favrap.bt',
    },
    {
        'name': 'Bertha Reeves',
        'country': 'Grenada',
        'contact': 'bihab@buwiv.dm',
    },
    {'name': 'Sam Waters', 'country': 'Morocco', 'contact': 'robusat@givo.bz'},
]
print(pretty_repr(users))
pprint(users)
print(users)
print(Markdown('# Contact Details'))
print('(463) 751-3964')
print('(706) 964-8424')
print('(926) 974-2765')
print('(468) 997-4314')
print('(668) 905-9855')
print('(251) 652-7147')
print('(443) 771-3964')
super_print(users)
print('[red]Hello[/red] Mark! [blue]Maintenance mode Initiated.[/blue]')
