from rich.console import Console
from rich.markdown import Markdown


def main():
    console = Console()
    #
    md_title = """
# Hi
## How Are You
### How Have you been
#### How many child do you have?
##### h5
###### h6
    """
    console.print(Markdown(md_title))

    md_table = """
| Name | Age | Street |
| :-: | -: | :- |
| Don Banks| 22| 1878 Lahna Park|
| Shane Price| 37| 893 Anain Center|
| Carlos Rice| 30| 1079 Setu Place|
| Theodore Romero| 29| 1710 Uzun Court|
| Russell Beck| 28| 1865 Pujuho Loop|
    """
    console.print(Markdown(md_table))
    #
    md_code = """
```python
async def main():
    pass
```
"""
    console.print(Markdown(md_code))
    md_code = """
## Javascript Code
```javascript
let a=25,
    b=30;

console.log(10);
console.log(a+b);
```
"""
    console.print(Markdown(md_code))
    md_code = """
> http://tigwael.sr/aluocu
>
> http://owi.sr/vinjo
>> Hello
>>> Google _chrome_ is not **evil** ~~think so~~
---
<mark>lorem</mark>

---
### Images

![Lorem](./assets/image/pngwing.com - Copy.png)

---
<zav@ebaki.kg>
- Pearl Alvarez - 136 Pacpe Key - Germany.
- Vernon Johnson - 167 Uzawid Pike - Albania.
- Noah Holmes - 1014 Igoed Parkway - New Zealand.
- Isaiah Paul - 1973 Tuluw View - Sudan.
- Eddie Castillo - 1608 Ebafup Manor - Caribbean Netherlands.
- Rebecca McDonald - 1155 Enupu River - Vanuatu.

1. Pearl Alvarez - 136 Pacpe Key - Germany.
1. Vernon Johnson - 167 Uzawid Pike - Albania.
1. Noah Holmes - 1014 Igoed Parkway - New Zealand.
   1. po\
lina
1. Isaiah Paul - 1973 Tuluw View - Sudan.
1. Eddie Castillo - 1608 Ebafup Manor - Caribbean Netherlands.
1. Rebecca McDonald - 1155 Enupu River - Vanuatu.


determine neighbor rule beyond gravity opinion interest stand price grow lead every concerned stream street chart kitchen dirty iron vast film log poetry stay
"""

    console.print(Markdown(md_code))
    console.print("[#ff00ff] Helllo [/#ff00ff]")
    console.print("Visit my [link=https://www.willmcgugan.com]blog[/link]!")
    pass


if __name__ == "__main__":
    main()
    pass
