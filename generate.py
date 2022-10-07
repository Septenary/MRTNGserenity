#!/usr/bin/env python

import argparse
import colorama
import json
import functools
import yaml
from libs.raid import Raid, load_raid
from libs.players import Player, GameClass
from libs.color import colortext
import libs.errorlog as errorlog
import jinja2
import pathlib
import random
import operator
import sys


def parse_cli() -> dict[str, any]:
    parser = argparse.ArgumentParser(
        description="Generate MRT notes for MRTNoteImporter"
    )
    parser.add_argument(
        "--templates",
        type=str,
        default="templates/sharks/WOTLK-Phase1/",
        help="Path to your templates to use.",
    )
    parser.add_argument(
        "--raid",
        type=str,
        default="raid.json",
        help="Path to a Raid-Helper raid export JSON file.",
    )
    parser.add_argument(
        "--assignments",
        type=str,
        default="assignments.yaml",
        help="Path to a Raid-Helper raid export JSON file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="Output file. Will overwrite if it already exists.",
    )
    return parser.parse_args()


def load_raid(raid_json: str) -> Raid:
    new_raid = Raid()
    for player_json in json.loads(raid_json)["raidDrop"]:
        if player_json["name"]:
            player = Player(name=player_json["name"], rh_string=player_json["spec"])
            new_raid.add_player(player)
    return new_raid


def load_assignments(assignments_yaml: str) -> dict[str, any]:
    return yaml.safe_load(assignments_yaml)


def instruct(player: Player | str | list[Player | str], instruction: str):
    if isinstance(player, Player) or isinstance(player, str):
        return f"{{p:{player}}}{{spell:71299}} {instruction}{{/p}}"
    if isinstance(player, list):
        x = ",".join([str(x) for x in player])
        return f"{{p:{x}}}{{spell:71299}} {instruction}{{/p}}"


def recursive_get(d, l):
    """Iterate nested dictionary"""
    return functools.reduce(operator.getitem, l, d)


def first(*players: Player | str | tuple[Player], errors: bool = True) -> Player:
    original_players = players
    if isinstance(players, tuple):
        if isinstance(players[0], list):
            players = players[0]
    for player in players:
        if isinstance(player, str) and raid.getplayer_by_name(player, errors=False):
            return raid.getplayer_by_name(player)
        if isinstance(player, Player):
            return player

    # Bad if we get here
    if errors:
        errorlog.add(
            f"first{original_players} was called, but none of those people are in the raid"
        )
    return "MISSING_PLAYER"


def rand(*players: Player | str | tuple[Player], errors: bool = True) -> Player:
    original_players = players
    if isinstance(players, tuple):
        if isinstance(players[0], list):
            players = players[0]

    ret = first(random.sample(players, k=len(players)), errors=False)
    if ret != "MISSING_PLAYER":
        return ret
    else:
        if errors:
            errorlog.add(
                f"random{players} was called, but none of those people are in the raid"
            )
    return "MISSING_PLAYER"


def assign(ass: str) -> Player:
    if "/" in ass:
        path = ass.split("/")
        r = recursive_get(assignments, path)
        if r.get("name"):
            return raid.getplayer_by_name(r["name"])
        if r.get("class") and not r.get("spec"):
            return raid.getplayers_by_classspec(gameclass=GameClass(r.get("class")))
        if r.get("class") and r.get("spec"):
            return raid.getplayers_by_classspec(
                gameclass=GameClass(r.get("class"), spec=Spec(r.get("spec")))
            )

    else:
        try:
            return raid.getplayer_by_name(ass)
        except KeyError:
            errorlog.add(
                "In assignment {assignment} there is a player called {assignment['name']}, but that player is not in the raid."
            )


def players_by_class(gcs: str):
    return raid.getplayers(gcs)


def players_by_spec(gcs: str, gss: str):
    return raid.getplayers(gcs, gss)


def newline_stripping_loader(filename: str) -> str:
    with open(filename) as f:
        template = f.read()
        template = template.replace("\n", "")
        template = template.replace(r"\n", "\n")
        return template


class Undefined(jinja2.Undefined):
    def __str__(self):
        errorlog.add(
            f"Tried to use {{{ {self._undefined_name} }}}, but that player isn't in the raid."
        )
        return "MISSING_DATA"


def main():
    # Parse CLI.
    args = parse_cli()

    # Load the data on who is in the raid.
    with open(args.raid, "r") as f:
        global raid
        raid = load_raid(f.read())

    # Load the assignments
    with open(args.assignments, "r") as f:
        global assignments
        assignments = load_assignments(f.read())

    # Build the jinja2 environment
    environment = jinja2.Environment(
        loader=jinja2.FunctionLoader(newline_stripping_loader),
        trim_blocks=True,
        line_comment_prefix="#",
        line_statement_prefix=None,
        undefined=Undefined,
    )

    environment.globals["raid"] = raid
    environment.globals["instruct"] = instruct
    environment.globals["colortext"] = colortext
    environment.globals["assignments"] = assignments
    environment.globals["assign"] = assign
    environment.globals["first"] = first
    environment.globals["random"] = rand
    environment.globals["players_by_class"] = players_by_class
    environment.globals["players_by_spec"] = players_by_spec

    for player in raid.players:
        environment.globals[player.name] = player.color_name()

    # Read and render each template (except the header)
    template_files = [
        x for x in pathlib.Path(args.templates).glob("**/*") if x.is_file()
    ]
    if not template_files:
        print(
            f"{colorama.Fore.RED}*** ERROR: No template files found in {args.templates} ***{colorama.Style.RESET_ALL}"
        )
        sys.exit(1)
    for template_file in template_files:
        template = environment.get_template(str(template_file))
        x = template.render(raid=raid)
        print("===========================================")
        print(x)
    errorlog.show()


if __name__ == "__main__":
    main()
