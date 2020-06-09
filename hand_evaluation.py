import itertools

import const


def hand_ranking(combination: []):
    """Returns tuple (name,value) of combination of 5 cards passed as list"""

    combination.sort()

    flush = True
    straight = True
    pairs = []

    for i, card in enumerate(combination):
        for j in range(i + 1, len(combination)):
            next_card = combination[j]
            if card.symbol != next_card.symbol:
                flush = False

            # cards are sorted, for straight check if next card - 1 is equal to previous one
            if card.number - i != next_card.number - j:
                straight = False

            if card.number == next_card.number:
                pairs.append(card.number)

    if flush and straight and combination[0].number == 10:
        return const.SetsAndValues.ROYAL_FLUSH.describe()
    elif flush and straight:
        return const.SetsAndValues.STRAIGHT_FLUSH.describe()
    elif len(pairs) > 4:
        return const.SetsAndValues.FOUR_OF_A_KIND.describe()
    elif len(pairs) == 4:
        return const.SetsAndValues.FULL_HOUSE.describe()
    elif flush:
        return const.SetsAndValues.FLUSH.describe()
    elif straight:
        return const.SetsAndValues.STRAIGHT.describe()
    elif len(pairs) == 3:
        return const.SetsAndValues.THREE_OF_A_KIND.describe()
    elif len(pairs) == 2:
        return const.SetsAndValues.TWO_PAIRS.describe()
    elif len(pairs) == 1:
        return const.SetsAndValues.ONE_PAIR.describe()
    else:
        return const.SetsAndValues.HIGH_CARD.describe()


def hands_combinations(table_and_player_cards, bot):
    """
    Checks all 5 element combinations of players cards and cards on table
    and sets each players card_set tuple to the best combination they have.
    """

    combination_list = list(itertools.combinations(table_and_player_cards, 5))

    # if len(comb_list) != 21:
    #    print(len(comb_list))

    best_value = 0

    for comb in combination_list:
        evaluated_comb = hand_ranking(list(comb))

        if evaluated_comb[1] > best_value:
            bot.card_set = evaluated_comb
            best_value = evaluated_comb[1]
