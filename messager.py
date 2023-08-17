message_queue = {}

"""
///////////////
/// METHODS ///
///////////////
"""


def messager_add_player(player_name: str) -> None:
    """
    Adds a new player to the messager system.
    Needs to be called when a player is created or all players are loaded.

    :param player_name: Player name to be added.
    :return: None
    """

    message_queue.update({player_name: []})


def add_message(player_name: str, message: str) -> None:
    """
    Adds a message to the message queue.

    :param player_name: Player's name to add the message to.
    :param message: Message to be added.
    :return: None.
    """

    global message_queue
    message_queue[player_name].append(message)


def empty_queue(player_name: str) -> list:
    """
    Empties queue and returns list with all messages.

    :param player_name: Player's name to dequeue all messages to.
    :return: List with all messages.
    """

    global message_queue
    messages = message_queue[player_name]
    message_queue[player_name] = []
    return messages
