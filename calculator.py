import streamlit as st
from dataclasses import dataclass, field
# from pyriichi import *

# Functions

# Creating Persistent Lists
if "hand" not in st.session_state:
    st.session_state.hand = []

if "message" not in st.session_state:
    st.session_state.message = []
    
# Shortening List Calls
hand = st.session_state.hand
message = st.session_state.message

# Creating a Data Class to Store Info
@dataclass
class TaggedTile:
    tile: str
    tags: set[str] = field(default_factory = set)

# Future Kan implementation
kan = 0

# Function to Sort by Suit, then number
def sort_hand():
    hand.sort(key=lambda t: (t.tile[-1], t.tile[-2]))

# Function to clear hand
def clear_hand():
    message.clear()
    hand.clear()

# Function to Create Tiles for x Suit
def tiles_for(suit):
    # Create New List
    result = []

    # If suit is an Honor
    if suit == "z":
        for i in range(1, 8):
            result.append((f"{i}z", f"{i}z"))
    # If suit is not an Honor
    else:
        for i in range(1, 10):
            result.append((f"{i}{suit}", f"{i}{suit}"))
            if i == 5:
                result.append((f"Red 5{suit}", f"r5{suit}"))
    # Return Full list of x Suit
    return result

# Function to treat Red 5 as Normal 5
def base(tile):
    return tile.removeprefix("r")

# Function logic for full hand
def is_full(value):
    if len(hand) > 13:
        full_error = f"Too many tiles, tile {value} not added"
        if full_error not in message:
            message.append(full_error)
        return True
    return False

# Function Logic for Tile Limit, 4 max for a tile
def reached_tile_limit(value, suit):
    # Count variables to keep track
    count = 1
    red_count = 0
    
    # Looping through hand and counting values
    for i in hand:
        if i.tile == f"r5{suit}":
            red_count = 1
        if base(i.tile) == base(value):
            count += 1
        # Hand Logic
        if count > 4:
            tile_count_error = f"Too many of tile {base(value)}, tile {base(value)} not added"
            if tile_count_error not in message:
                message.append(tile_count_error)
            return True
        if red_count == 1 and value == f"r5{suit}":
            red_tile_count_error = f"Too many of tile Red 5{suit}, tile Red 5{suit} not added"
            if red_tile_count_error not in message:
                message.append(red_tile_count_error)
            return True
    return False

# Function to add a tile to hand
def add_hand(value, suit):
    # Exit before adding if a rule is broken
    if is_full(value):
        return
    if reached_tile_limit(value, suit):
        return
    message.clear()
    hand.append(TaggedTile(value))

# Function to remove item from button hand display
def remove_item(index):
    message.clear()
    hand.pop(index)

# Function to add last to a tile
def mark_last():
    index = st.session_state.pick_last
    if index is None or index > len(hand):
        return
    for t in hand:
        t.tags.discard("last")
    hand[index].tags.add("last")








# UI
# st.header("Riichi Mahjong Calculator")

# Adding Tiles Section
st.header("Adding Tiles")

# Additional Information
suit_info = st.checkbox("Suit Explanation")
if suit_info:
    st.info(
    """
m for Manzu - Characters\n
p for Pinzu - Ball\n
s for Souzu - Sticks/Bamboo\n
z for Zihai - Honors (1-4 = ESWN, 5-7 = WGR Dragon)\n
    """
    )   

# Separating tiles by suit
suit = st.segmented_control("Suits",["m", "p", "s", "z"], default=None, key="suit")
if suit is None:
    st.info("Pick a Suit")
else:
    st.write(f"You chose {suit}")

    # Create buttons for chosen suit
    c = st.columns(5)
    for i, (label, value) in enumerate(tiles_for(suit)):
        with c[i % 5]:
            st.button(label, key=f"add{value}", on_click = add_hand, args=(value, suit))

# Clear Button
st.button("Clear Hand", key="clear_all", on_click = clear_hand)

# Print any error messages
if message:
    for m in message:
        st.error(m)


# Print hand
st.header("Current Hand")
if hand:
    # Create interactive buttons
    sort_hand()
    hand_col = st.columns(4)
    for i, t in enumerate(hand):
        with hand_col[i % 3]:
            st.button(f"({t.tile})" if "last" in t.tags else t.tile, key=f"del_{i}", on_click=remove_item, args=(i,))

    # Mark tile as last
    st.selectbox("Pick Last Tile", options=range(len(hand)), index=None, format_func=lambda i: hand[i].tile, key="pick_last", placeholder="Select Last Tile")
    st.button("Mark Last", key=f"mark_last_tile", on_click=mark_last)
else:
    message.clear()
    st.write("Nothing Yet")