import random
from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
import config
import time
from datetime import datetime

# DEBUG ON
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)

phones = []
with open("PHONES.txt", encoding="utf-8") as f:
    for line in f.readlines():
        phone = line.replace("\n", "")
        print(f'Reading phone {phone}')
        phones.append(phone)

with open("TEXT.txt", encoding="utf-8") as f:
    TEXT = f.read()

print(phones)
for session in phones:
    # TELEGRAM CLIENT SIGN-IN INIT
    client = TelegramClient(session, config.api_id, config.api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(session)
        client.sign_in(session, str(input(f'{session} Код подтверждения из телеграмм: \n')))

    # GETTING GROUP
    group = client.get_entity(PeerChannel(channel_id=config.group))
    subscribers = client.get_participants(group)
    print(f'SUCCESS SING IN {session}')
    # READING ID'S FROM .txt
    id_list = []
    with open(f'data/{config.output_file}', encoding="utf-8") as f:
        for elem in f.readlines():
            id_list.append(int(elem.replace("\n", "")))

    success_count = 0

    try:
        for user in subscribers:
            if success_count == config.msg_per_account:
                break

            if user.id in id_list:
                # SKIP MUTUAL CONTACT
                if user.phone is not None:
                    print("Skipping mutual contact...")
                    continue
                # SEND MESSAGE
                try:
                    client.send_message(user, message=TEXT)
                    id_list.remove(user.id)
                    success_count += 1
                except Exception as err:
                    print(err)
                    print(f'ВНИМАНИЕ ПРЕВЫШЕН ЛИМИТ || СМС #{success_count} | {session}')
                    time.sleep(random.triangular(2, 3))
                    break
                # LOGS
                print(f'{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second} Смс #{success_count} '
                      f'отправлено| Осталось {len(id_list)}')

                time.sleep(random.triangular(125, 160))
            else:
                continue

    finally:
        with open(f'data/{config.output_file}', "w", encoding="utf-8") as f:
            for elem in id_list:
                f.write(str(elem) + "\n")
