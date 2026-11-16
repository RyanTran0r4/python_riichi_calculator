from pyriichi import GameState, Hand, ScoreCalculator, YakuChecker, parse_tiles, Suit, Tile, TileSet
from tile_models import TaggedTile, mark_last

kans = 0

def get_dora_tile(indicator):
    if (indicator.suit == Suit.HONORS and indicator.rank == 7):
        return Tile(Suit.HONORS, 5)
    else:
        return TileSet().get_dora(indicator)

def get_all_dora(indicator):
    all_indicators = []
    for ind in indicator:
        all_indicators.append(get_dora_tile(parse_tiles(ind)[0]))
    return all_indicators

def score_hand(full_hand, is_tsumo, seat, dealer = 0, honba = 0, sticks = 0, riichi = False, ippatsu = False, dora_indicator = (), ron_from = None):
    # Scan Hand
    winning_tile = None
    new_hand = []
    last_count = 0
    dora = get_all_dora(dora_indicator)
    num_dora = 0
    count = 0
    for t in full_hand:
        check = parse_tiles(t.tile)[0]
        if (check in dora):
            num_dora += dora.count(check)
        if (check.is_red_dora):
            num_dora += 1

        if "last" in t.tags:
            winning_tile = parse_tiles(t.tile)[0]
            last_count += 1
        else:
            new_hand.append(t)
            count += 1

    # Return on invalid hands
    if (last_count != 1):
        return (None, ("Mark exactly one tile as the winning tile."))

    if (count != 13 + kans):
        return (None, (f"Need exactly {13+kans} other tiles."))

    # Turn TaggedTiles into Pyriichi Tiles
    new_hand = Hand(parse_tiles(" ".join(t.tile for t in new_hand)))

    # Set riichi if True
    if (riichi == True):
        new_hand.set_riichi()

    # Find Splits
    splits = new_hand.get_winning_combinations(winning_tile)

    # Return if no valid winning splits
    if (not splits):
        return (None, "Not a winning hand.")

    return (None, f"splits = {len(splits)}") # Temp Test Return


if (__name__ == "__main__"):
    test_hand = input("TEST - Enter your hand with the winning tile as the last tile:\n")
    indics = tuple(input("TEST - Enter Dora Indicators:\n").split())
    tagged_hand = [TaggedTile(t) for t in test_hand.split()]
    mark_last(tagged_hand, -1)

    print(score_hand(tagged_hand, is_tsumo=False, seat=0, dora_indicator=indics))