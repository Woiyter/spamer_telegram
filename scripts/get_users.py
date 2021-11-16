from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, ChannelParticipantsAdmins
import config

client = TelegramClient(config.phones[0], config.api_id, config.api_hash)
client.connect()
if not client.is_user_authorized():
    client.send_code_request(config.phones[0])
    client.sign_in(config.phones[0], str(input("Код подтверждения из телеграмм: \n")))


# GETTING USERS
group = client.get_entity(PeerChannel(channel_id=config.group))
subscribers = client.get_participants(group)
users_list = []
for user in subscribers:
    users_list.append(user.id)
# WRITING USER'S ID'S TO .txt
with open(f'data/{config.output_file}', "w", encoding="utf-8") as f:
    for elem in users_list:
        f.write(str(elem)+"\n")
