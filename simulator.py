import random
from math import ceil

enchs = ['ATK', 'ATK%', 'DEF', 'DEF%', 'MDEF', 'MDEF%', 'INT', 'INT%', 'HP', 'HP%']
enchs_acc = ['ATK', 'ATK%', 'DEF', 'DEF%', 'MDEF', 'MDEF%', 'INT', 'INT%', 'HP', 'HP%', 'CRIT%']

testing_base_stats = {
    'HP': 3760,
    'ATK': 550,
    'INT': 243,
    'DEF': 260,
    'MDEF': 170
}

def getWepStat(ench):
    if ench == 'ATK' or ench == 'INT':
        return (6, 12, 21, 30)
    elif ench == 'DEF' or ench == 'MDEF':
        return (1, 2, 4, 6)
    elif ench == 'ATK%' or ench == 'INT%':
        return (3, 6, 10, 15)
    elif ench == 'DEF%' or ench == 'MDEF%':
        return (1, 2, 3, 5)
    elif ench == 'HP':
        return (26, 52, 91, 130)
    elif ench == 'HP%':
        return (2, 4, 7, 10)


def getArmorStat(ench):
    if ench == 'ATK' or ench == 'INT':
        return (2, 4, 7, 10)
    elif ench == 'DEF' or ench == 'MDEF':
        return (4, 7, 13, 18)
    elif ench == 'ATK%' or ench == 'INT%':
        return (1, 2, 3, 5)
    elif ench == 'DEF%' or ench == 'MDEF%':
        return (3, 6, 10, 15)
    elif ench == 'HP':
        return (40, 80, 140, 200)
    elif ench == 'HP%':
        return (3, 6, 10, 15)


def getAccStat(ench):
    if ench == 'ATK' or ench == 'INT':
        return (4, 8, 14, 20)
    elif ench == 'DEF' or ench == 'MDEF':
        return (2, 5, 8, 12)
    elif ench == 'HP':
        return (26, 52, 91, 130)
    elif ench == 'HP%' or ench == 'ATK%' or ench == 'DEF%' or ench == 'MDEF%' or ench == 'INT%':
        return (2, 4, 7, 10)
    elif ench == 'CRIT%':
        return (3, 6, 10, 15)


def getStat(slot, ench):
    if slot == 'Weapon':
        return getWepStat(ench)
    elif slot == 'Armor' or slot == 'Helmet':
        return getArmorStat(ench)
    else:
        return getAccStat(ench)


def getRoll(ranges, size):
    if size == 0:
        return ceil(random.uniform(0, ranges[0]))
    else:
        return ceil(random.uniform(ranges[size-1], ranges[size]))


def getStatValue(ranges, rarity):
    roll = random.random()
    if rarity == 'SSR':
        if roll < 0.35:
            return getRoll(ranges, 1)
        elif roll < 0.95:
            return getRoll(ranges, 2)
        else:
            return getRoll(ranges, 3)
    elif rarity == 'SR':
        if roll < 0.2:
            return getRoll(ranges, 0)
        elif roll < 0.88:
            return getRoll(ranges, 1)
        elif roll < 0.98:
            return getRoll(ranges, 2)
        else:
            return getRoll(ranges, 3)
    elif rarity == 'R':
        if roll < 0.80:
            return getRoll(ranges, 0)
        elif roll < 0.97:
            return getRoll(ranges, 1)
        else:
            return getRoll(ranges, 2)


def getRandomStats(size, slot):
    if slot == 'Accessory':
        return random.sample(enchs_acc, size)
    else:
        return random.sample(enchs, size)


def getStatsAmount(rarity):
    roll = random.random()
    if rarity == 'R':
        # tested 20 cases, 8x 1 stat, 10x 2 stats, 2x 3 stats
        if roll < 0.4:
            return 1
        elif roll < 0.9:
            return 2
        else:
            return 3
    elif rarity == 'SR':
        # 100 cases, 65x 2 stats, 35x 3 stats
        if roll < 0.65:
            return 2
        else:
            return 3
    elif rarity == 'SSR':
        return 3


def convertStats(stats, base_stats):
    new_stats = {}
    for key, value in stats.items():
        if key == 'CRIT%':
            new_stats['CRIT%'] = value
            continue
        if key[len(key)-1] == '%':
            key = key[0:len(key)-1]
            value = value * base_stats[key] / 100.0
        if key in new_stats:
            raise ValueError('Duplicate key') 
        new_stats[key] = value
    return new_stats


def doEnchant(slot, rarity):
    size = getStatsAmount(rarity)
    stats = getRandomStats(size, slot)
    enchant = {}
    for stat in stats:
        enchant[stat] = getStatValue(getStat(slot, stat), rarity)
    return enchant


def evaluateEnchantBonus(enchant, base_stats):
    bonuses = {}
    for key, value in enchant.items():
        if key == 'CRIT%':
            bonuses['CRIT%'] = value
            continue
        if key[len(key)-1] == '%':
            key = key[0:len(key)-1]
            if key not in base_stats:
                continue
            real = value * base_stats[key] / 100.0
        else:
            real = value
        if key in bonuses:
            bonuses[key] = bonuses[key] + real
        else:
            bonuses[key] = real
    return bonuses


def doUntilStat(slot, rarity, stats):
    for i in range(1000000):
        enchant = doEnchant(slot, rarity)
        fail = False
        for key, value in stats.items():
            if key not in enchant:
                fail = True
                break
            if value > enchant[key]:
                fail = True
                break
        if not fail:
            print('Enchant succeeded on roll ' + str(i))
            print(enchant)
            break


def findProbability(slot, rarity, stats, base_stats, attempts, nice_print=True):
    success = 0
    stats = convertStats(stats, base_stats)
    for i in range(attempts):
        bonuses = evaluateEnchantBonus(doEnchant(slot, rarity), base_stats)
        fail = False
        for key, value in stats.items():
            if key not in bonuses:
                fail = True
                break
            if value > bonuses[key]:
                fail = True
                break
        if not fail:
            success = success + 1
        if i > 0 and i % 10000 == 0 and nice_print:
            print(str(i) + " enchants evaluated...")
    if nice_print:
        print(str(attempts) + " enchants were evaluated. " + str(success) + " of those had the requested stats.")
        print("Estimated probability is: " + str(100.0 * success / attempts) + "%")
    return 1.0 * success / attempts


findProbability('Accessory', 'SSR', {'INT%': 9, 'HP%': 5}, {'INT': 554, 'HP': 3340}, 100000)
