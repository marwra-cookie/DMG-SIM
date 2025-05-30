from . import *
from .launcher import project_root
import json
import random
import os


spellbook = {"direct": [], "passive": []}


def load_spells():
    """ """
    spell_types = list(spellbook.keys())
    json_path = os.path.join(project_root, "database", "spells.json")

    with open(json_path, "r") as file:
        data = json.load(file)
        for g in spell_types:
            for spell in data[g]:

                for stat in spell["stats"]:
                    if stat == "effect":
                        for base in spell["stats"]["effect"]:
                            match base:
                                case "attack":
                                    spell["stats"]["effect"]["attack"] = AttackBase(
                                        spell["stats"]["effect"]["attack"]
                                    )
                                case "spell":
                                    spell["stats"]["effect"]["spell"] = SpellBase(
                                        spell["stats"]["effect"]["spell"]
                                    )
                                case "healing":
                                    spell["stats"]["effect"]["healing"] = HealingBase(
                                        spell["stats"]["effect"]["healing"]
                                    )
                    else:
                        match stat:
                            case "scaling":
                                spell["stats"][stat] = Scaling(spell["stats"][stat])
                            case "cost":
                                spell["stats"][stat] = Cost(spell["stats"][stat])
                            case "rounds":
                                spell["stats"][stat] = Rounds(spell["stats"][stat])
                            case "gain":
                                spell["stats"][stat] = Gain(spell["stats"][stat])
                match g:
                    case "direct":
                        spellbook[g].append(Direct(**spell))
                    case "passive":
                        spellbook[g].append(Passive(**spell))


def get_last_spell_id() -> int:
    """

    :return:
    """
    i = 0

    for category in spellbook:
        for spell in spellbook[category]:
            if spell.id > i:
                i = spell.id

    return i


def get_spell_name(name) -> Spell:
    """

    :param name:
    :return:
    """
    for category in spellbook:
        for spell in spellbook[category]:
            if spell.info["name"] == name:
                return spell
    return None


def get_spell_id(i) -> Spell:
    """

    :param i:
    :return:
    """
    for category in spellbook:
        for spell in spellbook[category]:
            if spell.info["id"] == i:
                return spell
    return None
