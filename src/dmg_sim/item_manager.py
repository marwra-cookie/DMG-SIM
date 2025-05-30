from . import *
from .launcher import project_root
import json
import random
import os


armory = {
    "accessory": [],
    "armor": [],
    "boots": [],
    "helm": [],
    "weapon": [],
}


def compare_items(item1, item2) -> str:
    """

    :param item1:
    :param item2:
    :return:
    """
    stats1 = item1.stats
    stats2 = item2.stats

    msg = []

    for stat in stats1:
        msg.append([f"{stat.capitalize()}: {stats1[stat].get_value_color()}", f""])
    for i, stat in enumerate(stats2):
        if i < len(stats1):
            msg[i][1] = f"{stat.capitalize()}: {stats2[stat].get_value_color()}"
        else:
            msg.append([f"", f"{stat.capitalize()}: {stats2[stat].get_value_color()}"])

    msg.insert(0, ["Current:", "Dropped:"])
    msg.insert(
        1,
        [
            f"({item1.info["level"]}) {item1.info["name"]}",
            f"({item2.info["level"]}) {item2.info["name"]}",
        ],
    )

    msg = tabulate(
        msg,
        headers="firstrow",
    )

    return msg


def create_random_item(level):
    """

    :param level:
    :return:
    """
    item_types = list(armory.keys())

    slots = len(item_types) - 1
    slot = item_types[random.randint(0, slots)]

    item = create_item(slot, level)

    return item


def create_item(slot, level):
    """

    :param slot:
    :param level:
    :return:
    """
    match slot:
        case "helm":
            helm = Helm(**set_item_stats(slot, level))
            armory["helm"].append(helm)

            save_item("helm", helm)
            return helm
        case "armor":
            armor = Armor(**set_item_stats(slot, level))
            armory["armor"].append(armor)

            save_item("armor", armor)
            return armor
        case "boots":
            boots = Boots(**set_item_stats(slot, level))
            armory["boots"].append(boots)

            save_item("boots", boots)
            return boots
        case "accessory":
            accessory = Accessory(**set_item_stats(slot, level))
            armory["accessory"].append(accessory)

            save_item("accessory", accessory)
            return accessory
        case "weapon":
            weapon = Weapon(**set_item_stats(slot, level))
            armory["weapon"].append(weapon)

            save_item("weapon", weapon)
            return weapon
    return None


def set_item_stats(slot, level) -> dict:
    """

    :param slot:
    :param level:
    :return:
    """
    json_path = os.path.join(project_root, "database", "randomize.json")

    with open(json_path, "r") as file:
        data = json.load(file)
        tier_names = data[slot]
        size = len(tier_names[str(level)])
        name = tier_names[str(level)][random.randint(0, size - 1)]

    match slot:
        case "helm":
            quality = [6, 5, 4, 3, 2]

            base_stats = {
                "health": None,
                "defense": None,
                "resistance": None,
                "attackPower": None,
                "spellPower": None,
                "healingPower": None,
                "energy": None,
                "momentum": None,
            }

            quantity = quality[level - 1]

            while quantity > 0:
                stat = random.randrange(len(base_stats))
                base_stats.pop(stat)
                quantity -= 1

            name = set_identity(name, base_stats)

            stats = {
                "info": {"id": get_last_item_id() + 1, "name": name, "level": level},
                "stats": {},
            }

            for stat in base_stats:
                stats["stats"][stat] = set_stat(stat, level)

            return stats

        case "armor":
            quality = [4, 4, 3, 2, 1]
            base_stats = {
                "health": None,
                "defense": None,
                "resistance": None,
                "dodge": None,
                "parry": None,
                "regeneration": None,
            }

            quantity = quality[level - 1]

            while quantity > 0:
                stat = random.randrange(len(base_stats))
                base_stats.pop(stat)
                quantity -= 1

            name = set_identity(name, base_stats)

            stats = {
                "info": {"id": get_last_item_id() + 1, "name": name, "level": level},
                "stats": {},
            }

            for stat in base_stats:
                stats["stats"][stat] = set_stat(stat, level)

            return stats

        case "boots":
            quality = [2, 2, 1, 1, 0]
            base_stats = {
                "dodge": None,
                "energy": None,
                "momentum": None,
            }

            quantity = quality[level - 1]

            while quantity > 0:
                stat = random.randrange(len(base_stats))
                base_stats.pop(stat)
                quantity -= 1

            name = set_identity(name, base_stats)

            stats = {
                "info": {"id": get_last_item_id() + 1, "name": name, "level": level},
                "stats": {},
            }

            for stat in base_stats:
                stats["stats"][stat] = set_stat(stat, level)

            return stats

        case "accessory":
            quality = [7, 6, 5, 4, 3]
            base_stats = {
                "attackPower": None,
                "spellPower": None,
                "healingPower": None,
                "criticalChance": None,
                "criticalDamage": None,
                "armorPenetration": None,
                "spellPenetration": None,
                "energy": None,
                "momentum": None,
                "health": None,
                "defense": None,
                "resistance": None,
                "dodge": None,
                "parry": None,
                "regeneration": None,
            }

            quantity = quality[level - 1]

            while quantity > 0:
                stat = random.randrange(len(base_stats))
                base_stats.pop(stat)
                quantity -= 1

            stats = {
                "info": {"id": get_last_item_id() + 1, "name": name, "level": level},
                "stats": {},
            }

            for stat in base_stats:
                nr = set_stat(stat, level)
                if int(nr) >= 2:
                    nr = int(nr / 3)

                if nr > 0:
                    stats["stats"][stat] = set_stat(stat, level)

            return stats

        case "weapon":
            weapon_types = [
                "Sword",
                "Dagger",
                "Mace",
                "Axe",
                "Bow",
                "Crossbow",
                "Staff",
                "Scythe",
                "Wand",
            ]

            size = len(weapon_types) - 1
            weapon = weapon_types[random.randint(0, size)]

            base_stats = set_weapon_stats(weapon)

            quality = [4, 3, 2, 1, 0]
            quantity = quality[level - 1]

            while quantity > 0:
                stat = random.randrange(len(base_stats))
                base_stats.pop(stat)
                quantity -= 1

            name = set_identity(f"{name} {weapon}", base_stats)

            stats = {
                "info": {"id": get_last_item_id() + 1, "name": name, "level": level},
                "stats": {},
            }

            for stat in base_stats:
                stats["stats"][stat] = set_stat(stat, level)

            return stats
    return {}


def set_stat(name, level):
    """

    :param name:
    :param level:
    :return:
    """
    match name:
        case "attackPower":
            return AttackPower(set_attack_power(level))
        case "spellPower":
            return SpellPower(set_spell_power(level))
        case "healingPower":
            return HealingPower(set_healing_power(level))
        case "criticalChance":
            return CriticalChance(set_critical_chance(level))
        case "criticalDamage":
            return CriticalDamage(set_critical_damage(level))
        case "armorPenetration":
            return ArmorPenetration(set_armor_penetration(level))
        case "spellPenetration":
            return SpellPenetration(set_spell_penetration(level))
        case "energy":
            return Energy(set_energy())
        case "momentum":
            return Momentum(set_momentum(level))
        case "health":
            return Health(set_health(level))
        case "defense":
            return Defense(set_defense(level))
        case "resistance":
            return Resistance(set_resistance(level))
        case "dodge":
            return Dodge(set_dodge(level))
        case "parry":
            return Parry(set_parry(level))
        case "regeneration":
            return Regeneration(set_regeneration(level))
    return None


def set_weapon_stats(name) -> list:
    """

    :param name:
    :return:
    """
    match name:
        case "Sword":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalChance": None,
                "energy": None,
                "parry": None,
            }

            return base_stats
        case "Dagger":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalDamage": None,
                "momentum": None,
                "parry": None,
            }

            return base_stats
        case "Mace":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalDamage": None,
                "energy": None,
                "parry": None,
            }

            return base_stats

        case "Axe":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalDamage": None,
                "energy": None,
                "parry": None,
            }

            return base_stats

        case "Bow":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalChance": None,
                "energy": None,
                "momentum": None,
            }

            return base_stats
        case "Crossbow":
            base_stats = {
                "attackPower": None,
                "armorPenetration": None,
                "criticalDamage": None,
                "energy": None,
                "momentum": None,
            }

            return base_stats
        case "Staff":
            base_stats = {
                "spellPower": None,
                "healingPower": None,
                "spellPenetration": None,
                "criticalDamage": None,
                "energy": None,
            }

            return base_stats
        case "Scythe":
            base_stats = {
                "spellPower": None,
                "healingPower": None,
                "spellPenetration": None,
                "criticalDamage": None,
                "energy": None,
                "parry": None,
            }

            return base_stats
        case "Wand":
            base_stats = {
                "spellPower": None,
                "healingPower": None,
                "spellPenetration": None,
                "criticalChance": None,
                "momentum": None,
            }

            return base_stats
    return []


def set_identity(name, stats):
    """

    :param name:
    :param stats:
    :return:
    """
    json_path = os.path.join(project_root, "database", "randomize.json")

    with open(json_path, "r") as file:
        data = json.load(file)
        identities = data["identity"]

    for stat in stats:
        name += identities[stat]
        break

    return name


def set_attack_power(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 20) * level

    return stat


def set_spell_power(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 20) * level

    return stat


def set_healing_power(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 20) * level

    return stat


def set_armor_penetration(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_spell_penetration(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_critical_chance(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_critical_damage(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_health(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 200) * level

    return stat


def set_defense(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 20) * level

    return stat


def set_resistance(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 20) * level

    return stat


def set_parry(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_dodge(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_regeneration(level) -> float:
    """

    :param level:
    :return:
    """
    stat = (random.randint(1, 5) * level) / 100

    return stat


def set_energy() -> int:
    """

    :return:
    """
    stat = random.randint(1, 4)

    return stat


def set_momentum(level) -> int:
    """

    :param level:
    :return:
    """
    stat = random.randint(1, 10) * level

    return stat


def save_item(slot, item):
    """

    :param slot:
    :param item:
    """
    json_path = os.path.join(project_root, "database", "items.json")

    with open(json_path, "r") as file:
        data = json.load(file)
        data[slot].append(item.__dict__)
        file.seek(0)
        json.dump(data, file, indent=4)


def load_items():
    """ """
    item_types = list(armory.keys())

    json_path = os.path.join(project_root, "database", "items.json")

    with open(json_path, "r") as file:
        data = json.load(file)

        for g in item_types:
            for item in data[g]:

                for stat in item["stats"]:
                    match stat:
                        case "attackPower":
                            item["stats"][stat] = AttackPower(item["stats"][stat])
                        case "spellPower":
                            item["stats"][stat] = SpellPower(item["stats"][stat])
                        case "healingPower":
                            item["stats"][stat] = HealingPower(item["stats"][stat])
                        case "criticalChance":
                            item["stats"][stat] = CriticalChance(item["stats"][stat])
                        case "criticalDamage":
                            item["stats"][stat] = CriticalDamage(item["stats"][stat])
                        case "armorPenetration":
                            item["stats"][stat] = ArmorPenetration(item["stats"][stat])
                        case "spellPenetration":
                            item["stats"][stat] = SpellPenetration(item["stats"][stat])
                        case "energy":
                            item["stats"][stat] = Energy(item["stats"][stat])
                        case "momentum":
                            item["stats"][stat] = Momentum(item["stats"][stat])
                        case "health":
                            item["stats"][stat] = Health(item["stats"][stat])
                        case "defense":
                            item["stats"][stat] = Defense(item["stats"][stat])
                        case "resistance":
                            item["stats"][stat] = Resistance(item["stats"][stat])
                        case "dodge":
                            item["stats"][stat] = Dodge(item["stats"][stat])
                        case "parry":
                            item["stats"][stat] = Parry(item["stats"][stat])
                        case "regeneration":
                            item["stats"][stat] = Regeneration(item["stats"][stat])
                match g:
                    case "accessory":
                        armory[g].append(Accessory(**item))
                    case "armor":
                        armory[g].append(Armor(**item))
                    case "boots":
                        armory[g].append(Boots(**item))
                    case "helm":
                        armory[g].append(Helm(**item))
                    case "potion":
                        armory[g].append(Potion(**item))
                    case "weapon":
                        armory[g].append(Weapon(**item))


def get_last_item_id() -> int:
    """

    :return:
    """
    i = 0

    for category in armory:
        for item in armory[category]:
            if item.id > i:
                i = item.id

    return i


def get_item_name(name) -> Item:
    """

    :param name:
    :return:
    """
    for slot in armory:
        for item in armory[slot]:
            if item.info["name"] == name:
                return item
    return None


def get_item_id(i) -> Item:
    """

    :param i:
    :return:
    """
    for slot in armory:
        for item in armory[slot]:
            if item.info["id"] == i:
                return item
    return None
