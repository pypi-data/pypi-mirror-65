import click

FRUITCONFIG_NAME = "fruitconfig.py"

FMT_STEPHEADER = "🥝 Step {number}: {name}\n" + "-"* (click.get_terminal_size()[0] - 5)
SHELLCHAR = '$ '