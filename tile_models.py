from dataclasses import dataclass, field

# Creating a Data Class to Store Info
@dataclass
class TaggedTile:
    tile: str
    tags: set[str] = field(default_factory = set)

def mark_last(hand, index):
    for t in hand:
        t.tags.discard("last")
    hand[index].tags.add("last")