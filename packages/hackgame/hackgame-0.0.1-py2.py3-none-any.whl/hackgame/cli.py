import re
import shelve
import webbrowser
from datetime import datetime, timezone

import attr
import click
import inquirer
import pyfiglet
import ruamel.yaml
from click import ClickException
from tabulate import tabulate

from hackgame import api, STATE_FILE, docs, auth
from hackgame.api import HACKGAME_SERVER
from hackgame.models import World, AccessToken, Account, Player, Network, \
    Connection, Program, Ice, ActionResult


@attr.s(auto_attribs=True)
class ClickObj(object):
    state: dict
    client: api.HackgameClient
    nesting: int = 0


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS, help=docs.HACKGAME_HELP)
@click.pass_context
@click.option(
    "--state-file", type=click.STRING,
    default=str(STATE_FILE), help=docs.STATE_FILE_HELP
)
def cli(context, state_file):
    if context.obj is None:
        try:
            shelf = shelve.open(state_file)
        except OSError as e:
            if e.errno == 35:
                raise click.ClickException(
                    "hackgame is currently running in another process"
                )
            else:
                raise
        player_token = shelf.get("player_token", None)
        game_token = shelf.get("game_token", None)
        client = api.HackgameClient(
            player_token=player_token, token=game_token
        )
        context.obj = ClickObj(state=shelf, client=client)
    else:
        context.obj.nesting += 1


@cli.resultcallback()
@click.pass_context
def process_result(context, result, **kwargs):
    if context.obj.nesting == 0:
        context.obj.state.close()
    else:
        context.obj.nesting -= 1


@cli.command()
@click.pass_context
def login(context):
    """Authenticate with the Hackgame Server"""
    state = context.obj.state
    webbrowser.open(f"{HACKGAME_SERVER}/players/_cli_authentication/")
    _token = auth.wait_for_token_reply()
    state["player_token"] = _token
    click.echo("connected.")


@cli.command()
@click.pass_context
def shell(context):
    """Interactive Hackgame Shell"""
    click.echo(pyfiglet.Figlet(font="slant").renderText("hackgame"))

    click.echo("Type 'exit' to finish")
    click.echo()

    loop = True
    while loop:
        _messages = context.invoke(messages)
        user_input = click.prompt(prompt_suffix="$ ", text="")
        if user_input in ["quit", "exit"]:
            loop = False
        else:
            try:
                cli.main(
                    args=re.split(r'\s+', user_input.strip()),
                    standalone_mode=False,
                    obj=context.obj,
                )
            except click.UsageError as e:
                click.echo(str(e))
            except Exception as e:
                print(e)

    click.echo()
    click.echo("shutting down...")


class ObjectTypeParamType(click.ParamType):
    name = "object_type"

    def convert(self, value, param, ctx):
        lookup = {
            "account": Account,
            "player": Player,
            "token": AccessToken,
            "world": World,
            "network": Network,
            "connection": Connection,
            "program": Program,
            "ice": Ice,
        }
        try:
            return lookup[value]
        except KeyError:

            error_message = f"expected name of an object type, got {value}"
            objs = "\n".join([f"\t{name}" for name in lookup])
            error_help = f"valid OBJECT_TYPEs are:"
            self.fail(
                f"{error_message}\n\n{error_help}\n{objs}",
                param,
                ctx,
            )


class KeyValueParamType(click.ParamType):
    name = "key_value"

    def convert(self, value, param, ctx):
        try:
            key, value = value.split("=")
            return key, value
        except ValueError:
            error_message = f"expected key/value pair separated " \
                            f"by =, got {value}"
            self.fail(
                error_message,
                param,
                ctx,
            )


OBJECT_TYPE = ObjectTypeParamType()
KEY_VALUE = KeyValueParamType()


def _output(object_type, objects, output_format):
    click.echo()
    if output_format == "yaml":
        for obj in objects:
            click.echo(ruamel.yaml.safe_dump(
                attr.asdict(obj), default_flow_style=False
            ))
    elif output_format == "table":
        click.echo(tabulate(
            headers=object_type.headers(),
            tabular_data=[r.as_row() for r in objects]
        ))
    click.echo()


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.argument("public_uuid", type=click.STRING, default=None, required=False)
@click.option("--output", "-o", type=click.Choice(["table", "yaml"]), default="table")
@click.pass_context
def get(context, object_type, public_uuid, output):
    """
    Get public info about Objects in Hackgame
    """
    client = context.obj.client
    if public_uuid is not None:
        results = [client[object_type].get(public_uuid)]
    else:
        results = client[object_type].list()

    _output(object_type, results, output)


def create_account_flow(client: api.HackgameClient):
    handle = click.prompt("handle")
    networks = client.networks.list()

    questions = [
        inquirer.List(
            "network",
            message="Select a starting network",
            choices=[n.handle for n in networks],
        ),
    ]

    answers = inquirer.prompt(questions)
    network = [n for n in networks if n.handle == answers["network"]][0]
    return handle, network.public_uuid


def create_connection_flow(client: api.HackgameClient):
    handle = click.prompt("handle")
    target = click.prompt("target")
    return handle, target


def _echo_action_result(action_result: ActionResult):
    click.echo(f"success: {action_result.success} status_code: {action_result.status_code}")
    for message in action_result.messages:
        click.echo(message)
    for error in action_result.errors:
        click.echo(error.message)
    click.echo()


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.argument("public_uuid", type=click.STRING, default=None, required=False)
@click.argument("data", type=KEY_VALUE, nargs=-1)
@click.pass_context
def post(context, object_type, public_uuid, data):
    """Send requests to Objects"""
    client = context.obj.client
    _data = {k: v for k, v in data}
    action_result = client[object_type].post(public_uuid, _data)
    _echo_action_result(action_result)


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.argument("public_uuid", type=click.STRING, default=None, required=False)
@click.argument("data", type=KEY_VALUE, nargs=-1)
@click.pass_context
def transfer(context, object_type, public_uuid, data):
    """Send things"""
    client = context.obj.client
    _data = {k: v for k, v in data}
    action_result = client[object_type].transfer(public_uuid, _data)
    _echo_action_result(action_result)


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.option("--output", "-o", type=click.Choice(["table", "yaml"]), default="table")
@click.pass_context
def create(context, object_type, output):
    """Create new Objects"""
    client = context.obj.client
    if object_type == Account:
        handle, network_uuid = create_account_flow(client)
        obj = client[object_type].create(data={
            "handle": handle,
            "router": network_uuid
        })
    elif object_type == Connection:
        handle, target = create_connection_flow(client)
        obj = client[object_type].create(data={
            "handle": handle,
            "target": target,
        })
    else:
        raise ClickException("not yet implemented")

    _output(object_type, [obj], output)


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.argument("public_uuid", type=click.STRING)
@click.pass_context
def proxy(context, object_type, public_uuid):
    """Change the Object your Token allows you to act as"""
    client = context.obj.client
    action_result = client[object_type].proxy(public_uuid)
    _echo_action_result(action_result)


@cli.command()
@click.argument("object_type", type=OBJECT_TYPE)
@click.argument("public_uuid", type=click.STRING)
@click.pass_context
def use(context, object_type, public_uuid):
    """Configure your current token"""
    state = context.obj.state
    client = context.obj.client
    if not issubclass(object_type, AccessToken):
        raise ValueError("must be a token")

    token_obj = client.tokens.get(public_uuid=public_uuid)
    if token_obj:
        click.echo(f"using token {token_obj.handle}")
    else:
        raise ClickException(f"couldn't find token {public_uuid}")
    state["game_token"] = public_uuid


@cli.command()
@click.pass_context
def status(context):
    client = context.obj.client
    token = context.obj.state.get("game_token", None)
    if token is None:
        click.echo("you haven't set a token via `use`")
    else:
        token_obj = client.tokens.get(public_uuid=token)
        _output(AccessToken, [token_obj], output_format="yaml")


@cli.command()
@click.pass_context
def messages(context):
    """Receive any messages you are waiting for"""
    client = context.obj.client
    state = context.obj.state

    messages_after = state.get("messages_after", None)

    now = datetime.now(timezone.utc)
    _messages = client.messages(after=messages_after)
    [click.echo(m) for m in _messages]
    state["messages_after"] = now

    return _messages


@cli.command()
@click.pass_context
def help(context):
    """Get information about commands and what they do"""
    click.echo(cli.get_help(ctx=context))


for command in [get, proxy, use, create]:
    command.short_help = command.help
    command.help += docs.OBJECT_TYPE_HELP


if __name__ == '__main__':
    cli()
