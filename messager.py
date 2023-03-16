message_queue = []

"""
///////////////
/// METHODS ///
///////////////
"""


def add_message(message: str) -> None:
    """
    Adds a message to the message queue.

    :param message: Message to be added.
    :return: None.
    """
    global message_queue
    message_queue.append(message)


def empty_queue() -> list:
    """
    Empties queue and returns list with all messages.

    :return: List with all messages.
    """
    global message_queue
    messages = message_queue
    message_queue = []
    return messages
