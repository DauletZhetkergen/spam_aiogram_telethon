import json

from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest


def get_delay() -> int:
    # Get saved delay from db

    db = json.load(open("db.json", 'r'))
    delay = db['delay']
    return delay


def set_delay(delay: str) -> None:
    # Update/set new delay in db

    db = json.load(open('db.json', 'r'))

    db['delay'] = int(delay)
    json.dump(db, open('db.json', 'w'))


def set_message(message: str) -> None:
    # Update/set new message in db

    db = json.load(open('db.json', 'r'))

    db['message'] = message
    json.dump(db, open('db.json', 'w'))


def filter_groups(chats: list) -> list:
    # Filter to have only groups and mega-groups

    groups = []
    for chat in chats:
        try:
            if chat.broadcast:
                continue
        except AttributeError:
            pass
        try:
            if chat.participants_count:
                groups.append([chat.id, chat.title])
        except AttributeError:
            continue
    return groups


async def get_groups(client) -> list:
    # Scrap user's dialogs.

    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0))

    groups = filter_groups(result.chats)

    return groups


def parse_groups(groups: list) -> list:
    """
    Check if user's groups are allowed to send message
    Return list of True or False to every group
    """

    groups_json = json.load(open('groups.json', 'r'))

    for group in groups:
        if group[0] in groups_json:
            if len(group) == 3:
                group[-1] = True
            else:
                group.append(True)
        else:
            if len(group) == 3:
                group[-1] = False
            else:
                group.append(False)
    return groups


def change_settings(chat_id: int) -> None:
    # Change list of allowed groups to send message to

    groups = json.load(open("groups.json", 'r'))

    if chat_id in groups:
        groups.remove(chat_id)
    else:
        groups.append(chat_id)
    json.dump(groups, open("groups.json", 'w'))


def delete_left_group(chat_id: int) -> None:
    # Remove group from the allowed group list

    groups = json.load(open("groups.json", 'r'))
    try:
        groups.remove(chat_id)
    except ValueError:
        pass
    else:
        json.dump(groups, open("groups.json", 'w'))
