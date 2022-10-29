from fractions import Fraction
import click
from rich.console import Console
from rich.table import Table
import math


def get_interval_numbers(interval: str):
    a = float(interval.split(',')[0].split('[')[1])
    b = float(interval.split(',')[1].split(']')[0])
    return a, b


def get_parsed_function(function: str):
    return lambda x: eval(function)


def middle_point(a, b) -> float:
    return (a+b)/2


def percentage_error(current, previous) -> float:
    return abs(((current-previous)/current)*100)


def set_table(func: str):
    table = Table(title=f'Bisection Method: {func}')

    table.add_column("Iteration", justify="center", style="cyan")
    table.add_column("Interval", justify="center", style="cyan")
    table.add_column("a", justify="center", style="cyan")
    table.add_column("a Sign", justify="center", style="cyan")
    table.add_column("b", justify="center", style="cyan")
    table.add_column("b Sign", justify="center", style="cyan")
    table.add_column("Middle Point", justify="center", style="cyan")
    table.add_column("Middle Point Sign", justify="center", style="cyan")
    table.add_column("Percentage Error", justify="center", style="cyan")
    return table


def get_number_sign(n: float) -> str:
    return '+' if n >= 0 else '-'


def add_row(table: Table, iteration: int, a: float, b: float, middle_point: float, error: float, func):
    table.add_row(str(iteration), f'[{Fraction(a)},{Fraction(b)}]', str(Fraction(a)), get_number_sign(func(a)), str(
        Fraction(b)), get_number_sign(func(b)), str(Fraction(middle_point)), get_number_sign(func(middle_point)), f'{round(error, 2)}%')


@click.command()
@click.option('--interval', help='function interval', type=str, required=True)
@click.option('--function', help='function to do the calculus', type=str, required=True)
@click.option('--error', help='error', type=float, required=True)
def run(interval: str, function: str, error: float):
    console = Console()
    a, b = get_interval_numbers(interval)

    fun = get_parsed_function(function)

    table = set_table(function)

    current_error = 100

    previous_mid_point = 0

    iteration = 1

    # While current is higher to allowed error
    while current_error > error:
        current_mid_point = middle_point(a, b)

        current_error = percentage_error(current_mid_point, previous_mid_point)

        add_row(table, iteration, a, b, current_mid_point, current_error, fun)

        if fun(current_mid_point) < 0:
            a = current_mid_point
        else:
            b = current_mid_point
        previous_mid_point = current_mid_point
        iteration += 1

    console.print(table)


if __name__ == '__main__':
    run()
