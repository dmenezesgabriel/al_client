async def move_character(character, x, y):
    """
    Move character to coordinates.

    If coordinates point to a place where a character cannot go.
    it will be sent to jail to jail.

    Character will not pass over objects.

    # Map:
    # https://adventure.land/data.js

    """
    await character.socket.emit(
        "move",
        {
            "x": character.x,
            "y": character.y,
            "m": 0,
            "going_x": x,
            "going_y": y,
        },
    )
    character.x = x
    character.y = y
