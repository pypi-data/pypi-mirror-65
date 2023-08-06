import json
import io

import crayons
import click
from yaspin import yaspin


def print_debug(message):
    ctx = click.get_current_context()

    if ctx.obj['DEBUG']:
        debug_msg = f"({crayons.blue('DEBUG', bold=True)}) {message}"
        spinner = ctx.obj.get('SPINNER', None)
        if spinner is not None:
            spinner.write(debug_msg)
        else:
            click.echo(debug_msg)


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def spinner_ok_message(spinner, message):
    spinner.text = message
    spinner.ok("✅")


def spinner_ko_message(spinner, message):
    spinner.text = message
    spinner.fail("💥")


def get_spinner(text):
    new_spinner = yaspin(color="blue", text=text)
    ctx = click.get_current_context()
    ctx.obj['SPINNER'] = new_spinner
    return new_spinner


def copy_kubeconfig(source, destination):
    with open(source, "r") as source_file:
        with open(destination, "w") as destination_file:
            destination_file.write(source_file.read())


def get_indentation(level):
    return " " * 4 * level


def parse_json_output(contents):
    if isinstance(contents, str):
        contents = io.StringIO(contents)
    contents.seek(0)
    parsed_file = [line.rstrip('\n').lstrip(" ") for line in contents.readlines()]
    fixed_content = "".join(parsed_file).replace("}{", "},{")
    return json.loads(f'[{fixed_content}]')
