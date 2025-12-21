import asyncio
import time
from dataclasses import dataclass, field

from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text


@dataclass
class Counters:
    start_time: float = field(default_factory=time.monotonic)

    tasks_total: int = 0
    tasks_processed_total: int = 0
    tasks_failed_total: int = 0

    @property
    def uptime(self) -> float:
        return time.monotonic() - self.start_time

    @property
    def processing_rate(self) -> float:
        if self.uptime == 0:
            return 0.0
        return self.tasks_processed_total / self.uptime


async def worker(metrics: Counters, total: int):
    for i in range(total):
        await asyncio.sleep(0.15)
        metrics.tasks_processed_total += 1
        if i % 6 == 0:
            metrics.tasks_failed_total += 1


def counter_panel(metrics: Counters) -> Panel:
    table = Table.grid(padding=1)
    table.add_column(justify='left')
    table.add_column(justify='right')

    table.add_row(
        'Tasks processed', f'[green]{metrics.tasks_processed_total}[/]'
    )
    table.add_row('Tasks failed', f'[red]{metrics.tasks_failed_total}[/]')
    table.add_row(
        'Processing rate', f'[cyan]{metrics.processing_rate:.2f}/sec[/]'
    )
    table.add_row('Uptime', f'{metrics.uptime:.1f}s')

    return Panel(
        table,
        title='Counters',
        border_style='green',
    )


def status_spinner(metrics: Counters):
    text = (
        f'[bold yellow]'
        f'({metrics.tasks_failed_total} - '
        f'{metrics.tasks_processed_total} / '
        f'{metrics.tasks_total})'
        f'[/]'
    )
    return Align.center(Spinner('dots', text=text))


def make_layout():
    layout = Layout()
    layout.split_column(
        Layout(name='header', size=3),
        Layout(name='body'),
        Layout(name='footer', size=3),
    )
    layout['body'].split_row(
        Layout(name='left'),
        Layout(name='right'),
    )
    return layout


async def dashboard(metrics: Counters):
    layout = make_layout()

    with Live(layout, refresh_per_second=10, screen=True):
        while metrics.tasks_processed_total < metrics.tasks_total:
            layout['header'].update(
                Panel(
                    Text('PROMETHEUS-STYLE METRICS', justify='center'),
                    style='bold blue',
                )
            )

            layout['left'].update(
                Panel(status_spinner(metrics), title='Status')
            )

            layout['right'].update(counter_panel(metrics))

            layout['footer'].update(
                Panel(
                    f'Total tasks: {metrics.tasks_total}',
                    style='bold green',
                )
            )

            await asyncio.sleep(0.1)


async def main():
    metrics = Counters()
    metrics.tasks_total = 60

    await asyncio.gather(
        dashboard(metrics),
        worker(metrics, metrics.tasks_total),
    )


if __name__ == '__main__':
    asyncio.run(main())
