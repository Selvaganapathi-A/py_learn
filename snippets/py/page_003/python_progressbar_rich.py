import time

from rich.progress import Progress


with Progress(refresh_per_second=50) as progress:
    task1 = progress.add_task("[red]Downloading...", total=100)
    task2 = progress.add_task("[green]Processing...", total=100)
    task3 = progress.add_task("[cyan]Cooking...", total=100)
    task4 = progress.add_task("[magenta]Baking...", total=100)

    while not progress.finished:
        progress.update(task1, advance=0.3)
        progress.update(task2, advance=0.5)
        progress.update(task3, advance=0.7)
        progress.update(task4, advance=0.9)
        time.sleep(0.02)
