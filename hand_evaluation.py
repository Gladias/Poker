import itertools

import const


def hand_ranking(combination: []):
    """Return tuple (name,value) of combination of 5 cards passed as list"""

    combination.sort()

    flush = True
    straight = True
    pairs = []

    for i in range(len(combination)):
        for j in range(i + 1, len(combination)):

            if combination[i].symbol != combination[j].symbol:
                flush = False

            # cards are sorted, for straight check if next card - 1 is equal to previous one
            if combination[i].number - i != combination[j].number - j:
                straight = False

            if combination[i].number == combination[j].number:
                pairs.append(combination[i].number)

    if flush and straight and combination[0].number == 10:
        return const.SETS_AND_VALUES[0]

    elif flush and straight:
        return const.SETS_AND_VALUES[1]

    elif len(pairs) > 4:
        return const.SETS_AND_VALUES[2]

    elif len(pairs) == 4:
        return const.SETS_AND_VALUES[3]

    elif flush:
        return const.SETS_AND_VALUES[4]

    elif straight:
        return const.SETS_AND_VALUES[5]

    elif len(pairs) == 3:
        return const.SETS_AND_VALUES[6]

    elif len(pairs) == 2:
        return const.SETS_AND_VALUES[7]

    elif len(pairs) == 1:
        return const.SETS_AND_VALUES[8]

    else:
        return const.SETS_AND_VALUES[9]


def hands_combinations(table_and_player_cards, bot):
    """
    Check all 5 elements combinations of players cards and cards on table
    and set each players card_set tuple to the best combination they have.
    """

    #cards = []
    #cards.extend(table)
    #cards.append(player.card_1)
    #cards.append(player.card_2)

    comb_list = list(itertools.combinations(table_and_player_cards, 5))

    best_value = 0

    for j in range(len(comb_list)):
        combination = hand_ranking(list(comb_list[j]))

        if combination[1] > best_value:
            bot.card_set = combination
            best_value = combination[1]
