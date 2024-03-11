import asyncio
import json
import logging
import re
import requests
import urllib.parse as urllib
from collections import OrderedDict
from operator import itemgetter
from urllib.error import HTTPError
from urllib.request import urlopen

import redis.asyncio as redis
import pickle
import base64

import telegram.error
from telegram import *
from telegram.constants import ChatMemberStatus, ParseMode
from telegram.ext import *

from db.Database import Database
from db.Database import Table
from db.Database import Column
from db import utils
import structures

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__file__)

NO_REFEREES = {"no_referees": 0}

subscription_requirement_chat_id = -1002131461518

cache = redis.Redis()


async def init_cache():
    global cache
    await cache.set("admin_message_data", "{}")
    await cache.set("user_reg_data", "{}")


async def create_admin_message_entry(chat_id: int):
    global cache
    raw_all_admin_message_data = await cache.get("admin_message_data")
    all_admin_message_data = {}
    if raw_all_admin_message_data:
        all_admin_message_data = json.loads(raw_all_admin_message_data)
    all_admin_message_data[str(chat_id)] = {
        "waiting_for_message": 1,
        "waiting_for_button_title": 0,
        "waiting_for_button_url": 0,
        "message": str(base64.b64encode(pickle.dumps(Message(message_id=Message.message_id, chat=Message.chat, date=Message.date))), "utf-8"),
        "message_keyboard": str(base64.b64encode(pickle.dumps([])), "utf-8"),
        "button_title": "",
        "button_url": ""
    }
    await cache.set("admin_message_data", json.dumps(all_admin_message_data))


async def create_user_reg_entry(chat_id: int, ref_id: int):
    global cache
    raw_all_user_reg_data = await cache.get("user_reg_data")
    all_user_reg_data = {}
    if raw_all_user_reg_data:
        all_user_reg_data = json.loads(raw_all_user_reg_data)
    all_user_reg_data[str(chat_id)] = {
        "waiting_for_address": 1,
        "lang": "",
        "referral": ref_id,
        "address": ""
    }
    await cache.set("user_reg_data", json.dumps(all_user_reg_data))


async def remove_admin_message_entry(chat_id: int):
    global cache
    all_admin_message_data = json.loads(await cache.get("admin_message_data"))
    if str(chat_id) in all_admin_message_data.keys():
        del all_admin_message_data[str(chat_id)]
    await cache.set("admin_message_data", json.dumps(all_admin_message_data))


async def remove_user_reg_entry(chat_id: int):
    global cache
    all_user_reg_data = json.loads(await cache.get("user_reg_data"))
    if str(chat_id) in all_user_reg_data.keys():
        del all_user_reg_data[str(chat_id)]
    await cache.set("user_reg_data", json.dumps(all_user_reg_data))


db_columns = (Column("id", int, False),
              Column("name", str, False),
              Column("is_subscribed", bool, False),
              Column("referrer", int, False),
              Column("referees", int, False),
              Column("serial", int, True),
              Column("lang", str, False),
              Column("ton_addr", str, False))

database = Database("database.db")

users_table = Table("users", db_columns)


def get_referee_number(user_id) -> int:
    global users_table, db_columns
    referee_rows = database.query(users_table, (db_columns[0],),
                                  {db_columns[3]: user_id},
                                  [utils.OPERATORS['is']], False)
    return len(referee_rows)


def get_top_referrers(user_id) -> dict:
    global users_table, db_columns
    user_rows = database.query(users_table, (db_columns[1], db_columns[4]),
                               {db_columns[3]: int(user_id)},
                               [utils.OPERATORS['is']], False)

    if len(user_rows) == 0:
        return NO_REFEREES

    referee_numbers = {}
    for user_row in user_rows:
        referee_numbers[user_row[0]] = user_row[1]

    return dict(sorted(referee_numbers.items(), key=itemgetter(1), reverse=True)[:10])


def get_rank(user_id: int, corrected: bool) -> int:
    global users_table, db_columns
    user_rows = database.query(users_table, (db_columns[0], db_columns[4], db_columns[5]),
                               utils.NO_CONDITION,
                               utils.NO_OPERATOR, False)

    base_ranks = {}
    for user_row in user_rows:
        base_ranks[user_row[0]] = user_row[2]
    sorted_base_ranks = OrderedDict(sorted(base_ranks.items(), key=itemgetter(1), reverse=False))

    if not corrected:
        return OrderedDict(sorted(base_ranks.items(), key=itemgetter(1), reverse=True))[user_id]

    referee_numbers = {}
    for user_row in user_rows:
        referee_numbers[user_row[0]] = user_row[1]
    sorted_referee_numbers = OrderedDict(sorted(referee_numbers.items(), key=itemgetter(1), reverse=True))

    ranks = []

    for user in sorted_referee_numbers.keys():
        same_referee_number = [k for k, v in sorted_referee_numbers.items() if v == sorted_referee_numbers[user]]
        if len(same_referee_number) == 1:
            if user not in ranks:
                ranks.append(user)
        else:
            same_referee_number_base_ranks = {}
            for repeated_user in same_referee_number:
                same_referee_number_base_ranks.update({repeated_user: sorted_base_ranks[repeated_user]})
            sorted_same_referee_number_base_ranks = OrderedDict(
                sorted(same_referee_number_base_ranks.items(), key=itemgetter(1), reverse=False))
            for repeated_user in sorted_same_referee_number_base_ranks.keys():
                if repeated_user not in ranks:
                    ranks.append(repeated_user)

    return ranks.index(user_id) + 1


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int) -> None:
    global database, db_columns
    user_id = update.effective_user.id
    lang = database.query(users_table, (db_columns[6],),
                          {db_columns[0]: update.effective_chat.id},
                          [utils.OPERATORS["is"]], False)[0][0]
    await context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=message_id)
    await context.bot.send_message(
        text=structures.get_menu_text(get_rank(user_id, False), user_id, structures.Lang(lang)),
        chat_id=update.effective_chat.id,
        reply_markup=structures.get_menu_keyboard(user_id, structures.Lang(lang)),
        parse_mode=ParseMode.HTML)


async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE, message_id: int) -> None:
    await context.bot.edit_message_text(
        text=structures.admin_panel_text,
        chat_id=update.effective_chat.id,
        message_id=message_id,
        reply_markup=structures.get_admin_panel_keyboard(),
        parse_mode=ParseMode.HTML
    )


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global database, db_columns, subscription_requirement_chat_id
    status_channel = (await context.bot.getChatMember(subscription_requirement_chat_id,
                                                      update.effective_user.id)).status
    if status_channel == ChatMemberStatus.MEMBER or status_channel == ChatMemberStatus.ADMINISTRATOR:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=structures.admin_panel_text,
                                       reply_markup=structures.get_admin_panel_keyboard())


async def address_valid(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int) -> None:
    global cache
    offset = 274  # normally 1

    user_reg_data = json.loads(await cache.get("user_reg_data"))[str(user_id)]
    lang = user_reg_data["lang"]
    ref_id = user_reg_data["referral"]
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=structures.get_valid_address_text(structures.Lang(lang)),
                                   reply_markup=structures.get_subscription_check_keyboard(structures.Lang(lang)))
    referee_rows = database.query(users_table, (db_columns[0],),
                                  {db_columns[3]: int(ref_id)},
                                  [utils.OPERATORS['is']], False)
    if referee_rows is not None:
        database.update(users_table, {db_columns[4]: len(referee_rows) + 1},
                        {db_columns[0]: int(ref_id)})
    database.insert(users_table, {db_columns[0]: update.effective_chat.id,
                                  db_columns[1]: update.effective_user.full_name,
                                  db_columns[2]: False, db_columns[3]: int(ref_id),
                                  db_columns[4]: 0,
                                  db_columns[5]: database.count_rows(users_table)[0] + offset,
                                  db_columns[6]: lang, db_columns[7]: user_reg_data["address"]})
    await remove_user_reg_entry(user_id)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global users_table, db_columns, cache
    ref_id = context.args
    user_row = database.query(users_table, (db_columns[0], db_columns[2], db_columns[6]),
                              {db_columns[0]: update.effective_user.id},
                              [utils.OPERATORS['is']], False)
    if not len(user_row):
        if (not len(ref_id)) or int(ref_id[0]) == update.effective_user.id:
            ref_id = [-1]
        await create_user_reg_entry(update.effective_chat.id, int(ref_id[0]))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=structures.choose_language_message,
                                       reply_markup=structures.get_choose_language_keyboard())
    else:
        lang = user_row[0][2]
        if not user_row[0][1]:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=structures.get_valid_address_text(structures.Lang(lang)),
                                           reply_markup=structures.get_subscription_check_keyboard(
                                               structures.Lang(lang)))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=structures.get_restart_message(structures.Lang(lang)),
                                           reply_markup=structures.get_return_to_menu_keyboard(structures.Lang(lang),
                                                                                               True))


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global subscription_requirement_chat_id, users_table, db_columns, cache

    query = update.callback_query
    await query.answer()

    raw_all_admin_message_data = await cache.get("admin_message_data")
    all_admin_message_data = {}
    if raw_all_admin_message_data:
        all_admin_message_data = json.loads(raw_all_admin_message_data)

    raw_all_user_reg_data = await cache.get("user_reg_data")
    all_user_reg_data = {}
    if raw_all_user_reg_data:
        all_user_reg_data = json.loads(raw_all_user_reg_data)

    if str(update.effective_chat.id) in all_admin_message_data:
        admin_message_data = all_admin_message_data[str(update.effective_chat.id)]

        if query.data == "admin_message_confirmation_yes":
            button_title = admin_message_data["button_title"]
            button_url = admin_message_data["button_url"]
            message_keyboard = pickle.loads(base64.b64decode(bytes(admin_message_data["message_keyboard"], "utf-8")))

            if button_title:
                message_keyboard.append([InlineKeyboardButton(button_title, url=button_url)])

            admin_message_data["message_keyboard"] = str(base64.b64encode(pickle.dumps(message_keyboard)), "utf-8")

            await context.bot.edit_message_text(text=structures.admin_message_button_question,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id,
                                                reply_markup=structures.get_admin_button_question_keyboard())
        if query.data == "admin_message_confirmation_retry":
            await context.bot.edit_message_text(text=structures.admin_send_message_text,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id)
            admin_message_data["waiting_for_button_title"] = 1
        if query.data == "admin_message_button_add":
            await context.bot.edit_message_text(text=structures.admin_message_button_title_question,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id)
            admin_message_data["waiting_for_button_title"] = 1
        if query.data == "admin_message_confirmation_send":
            message = pickle.loads(base64.b64decode(bytes(admin_message_data["message"], "utf-8")))
            message_keyboard = pickle.loads(base64.b64decode(bytes(admin_message_data["message_keyboard"], "utf-8")))

            await context.bot.copy_message(chat_id=update.effective_chat.id,
                                           from_chat_id=message.chat_id,
                                           message_id=message.message_id,
                                           reply_markup=InlineKeyboardMarkup(message_keyboard))
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=structures.admin_message_confirmation_send_text,
                                           reply_markup=structures.get_admin_message_confirmation_send_keyboard())
        if query.data == "admin_send_message_confirmed":
            user_rows = database.query(users_table, (db_columns[0],), utils.NO_CONDITION,
                                       utils.NO_OPERATOR, False)
            message = pickle.loads(base64.b64decode(bytes(admin_message_data["message"], "utf-8")))
            message_keyboard = pickle.loads(base64.b64decode(bytes(admin_message_data["message_keyboard"], "utf-8")))

            for user in user_rows:
                try:
                    await context.bot.copy_message(chat_id=user[0],
                                                   from_chat_id=message.chat_id,
                                                   message_id=message.message_id,
                                                   reply_markup=InlineKeyboardMarkup(message_keyboard))
                except telegram.error.Forbidden:
                    print(f"User {user[0]} is unavailable.")

            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=structures.messages_sent_text)
            await remove_admin_message_entry(update.effective_chat.id)
            await admin_panel(update, context)
        if query.data == "admin_message_button_title_confirmation_yes":
            await context.bot.edit_message_text(text=structures.admin_message_button_url_question,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id)
            admin_message_data["waiting_for_button_url"] = 1
        if query.data == "admin_message_button_title_confirmation_retry":
            await context.bot.edit_message_text(text=structures.admin_message_button_title_question,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id)
            admin_message_data["waiting_for_button_title"] = 1
        if query.data == "admin_message_button_url_confirmation_retry":
            await context.bot.edit_message_text(text=structures.admin_message_button_url_question,
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id)
            admin_message_data["waiting_for_button_url"] = 1
        all_admin_message_data[str(update.effective_chat.id)] = admin_message_data
        await cache.set("admin_message_data", json.dumps(all_admin_message_data))
    if str(update.effective_chat.id) in all_user_reg_data:
        user_reg_data = all_user_reg_data[str(update.effective_chat.id)]
        choose_lang_pattern = re.compile("choose_language_[a-z]*")
        if choose_lang_pattern.match(query.data):
            lang = query.data[-2:]
            await context.bot.edit_message_text(text=structures.get_enter_address_text(structures.Lang(lang)),
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id,
                                                parse_mode=ParseMode.HTML)
            user_reg_data["lang"] = lang
        all_user_reg_data[str(update.effective_chat.id)] = user_reg_data
        await cache.set("user_reg_data", json.dumps(all_user_reg_data))
    if query.data == "subscription_check":
        status_channel = (await context.bot.getChatMember(subscription_requirement_chat_id,
                                                          update.effective_user.id)).status
        if (status_channel == ChatMemberStatus.MEMBER or
                status_channel == ChatMemberStatus.ADMINISTRATOR or
                status_channel == ChatMemberStatus.OWNER):
            database.update(users_table, {db_columns[2]: True}, {db_columns[0]: query.from_user.id})
            await show_menu(update, context, query.message.message_id)
        else:
            lang = database.query(users_table, (db_columns[6],),
                                  {db_columns[0]: update.effective_chat.id},
                                  [utils.OPERATORS["is"]], False)[0][0]
            await context.bot.edit_message_text(text=structures.get_not_subscribed_text(structures.Lang(lang)),
                                                chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id,
                                                reply_markup=structures.get_subscription_check_keyboard(
                                                    structures.Lang(lang)),
                                                parse_mode=ParseMode.HTML)
            database.update(users_table, {db_columns[2]: False}, {db_columns[0]: update.effective_chat.id})
    if query.data == "ref_dashboard":
        user_id = update.effective_user.id
        lang = database.query(users_table, (db_columns[6],),
                              {db_columns[0]: user_id},
                              [utils.OPERATORS["is"]], False)[0][0]
        await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                            message_id=query.message.message_id,
                                            text=structures.get_ref_dashboard_text(get_referee_number(user_id),
                                                                                   user_id, structures.Lang(lang)),
                                            reply_markup=structures.get_return_to_menu_keyboard(structures.Lang(lang),
                                                                                                True),
                                            parse_mode=ParseMode.HTML)
    if query.data == "whitelist_presale":
        lang, address = database.query(users_table, (db_columns[6], db_columns[7]),
                              {db_columns[0]: update.effective_chat.id},
                              [utils.OPERATORS["is"]], False)[0]
        headers = {"Authorization": f"Bearer {structures.tonapi_key}"}
        response = requests.get("https://tonapi.io/v2/nfts/collections/EQCvDh92MohIpsSbA0eH_94cLnvEmvx-Sv2PorNqQRf42Kue/items", headers=headers)
        response = response.json()
        has_nft = False
        with urlopen(f"https://toncenter.com/api/v2/detectAddress?address={urllib.quote_plus(address)}") as addr_response:
            addr_response = json.loads(str(addr_response.read().decode("utf-8")))
            address = addr_response["result"]["raw_form"]
        for item in response["nft_items"]:
            if item["owner"]["address"] == address:
                has_nft = True
                break
        if has_nft:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id,
                                                text=structures.get_presale_proceed_text(structures.Lang(lang)),
                                                reply_markup=structures.get_return_to_menu_keyboard(
                                                    structures.Lang(lang),
                                                    True),
                                                parse_mode=ParseMode.HTML)
        else:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                message_id=query.message.message_id,
                                                text=structures.get_presale_fail_text(structures.Lang(lang)),
                                                reply_markup=structures.get_return_to_menu_keyboard(
                                                    structures.Lang(lang),
                                                    True),
                                                parse_mode=ParseMode.HTML)
    if query.data == "return_to_menu":
        await show_menu(update, context, query.message.message_id)
    if query.data == "admin_statistics":
        await context.bot.edit_message_text(text=structures.admin_statistics_loading_text,
                                            chat_id=update.effective_chat.id,
                                            message_id=query.message.message_id,
                                            reply_markup=structures.get_admin_statistics_keyboard())
        total_users = len(database.query(users_table, (db_columns[0],),
                                         utils.NO_CONDITION,
                                         utils.NO_OPERATOR, False))
        total_users_subscribed = len(database.query(users_table, (db_columns[0],),
                                                    {db_columns[2]: True},
                                                    utils.OPERATORS['is'], False))
        await context.bot.edit_message_text(text=structures.get_admin_statistics_text(total_users,
                                                                                      total_users_subscribed),
                                            chat_id=update.effective_chat.id,
                                            message_id=query.message.message_id,
                                            reply_markup=structures.get_admin_statistics_keyboard())
    if query.data == "admin_send_message":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=structures.admin_send_message_text)
        await create_admin_message_entry(update.effective_chat.id)
    if query.data == "admin_export_csv":
        database.export_to_xlsx(users_table, "users.xlsx")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open("users.xlsx", "rb"))
    if query.data == "return_to_admin_panel":
        await remove_admin_message_entry(update.effective_chat.id)
        await show_admin_panel(update, context, query.message.message_id)
    if query.data == "faq":
        lang = database.query(users_table, (db_columns[6],),
                              {db_columns[0]: update.effective_chat.id},
                              [utils.OPERATORS["is"]], False)[0][0]
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=structures.get_faq_text(structures.Lang(lang)),
                                       parse_mode=ParseMode.HTML,
                                       reply_markup=structures.get_return_to_menu_keyboard(structures.Lang(lang),
                                                                                           False))


async def message_handler(update: Update, context: CallbackContext) -> None:
    global database, db_columns, cache
    chat_id = update.effective_chat.id

    raw_all_user_reg_data = await cache.get("user_reg_data")
    all_user_reg_data = {}
    if raw_all_user_reg_data:
        all_user_reg_data = json.loads(raw_all_user_reg_data)

    if str(chat_id) in all_user_reg_data:
        user_reg_data = all_user_reg_data[str(chat_id)]
        if user_reg_data["waiting_for_address"]:
            lang = user_reg_data["lang"]
            try:
                with urlopen(f"https://toncenter.com/api/v2/detectAddress?address={urllib.quote_plus(update.message.text)}") as response:
                    same_address = database.query(users_table, (db_columns[0],),
                                                  {db_columns[7]: update.message.text},
                                                  [utils.OPERATORS['is']], False)
                    if len(same_address):
                        await context.bot.send_message(chat_id=chat_id,
                                                       text=structures.get_same_address_exists_text(structures.Lang(lang)))
                    else:
                        response = json.loads(str(response.read().decode("utf-8")))
                        if response["result"]["given_type"] == "raw_form":
                            await context.bot.send_message(chat_id=chat_id,
                                                           text=structures.get_raw_form_address_text(structures.Lang(lang)))
                        else:
                            user_reg_data["waiting_for_address"] = 0
                            user_reg_data["address"] = update.message.text
                            all_user_reg_data[str(chat_id)] = user_reg_data
                            await cache.set("user_reg_data", json.dumps(all_user_reg_data))
                            await address_valid(update, context, chat_id)
            except HTTPError:
                await context.bot.send_message(chat_id=chat_id,
                                               text=structures.get_invalid_address_text(structures.Lang(lang)))
            except TypeError:
                await context.bot.send_message(chat_id=chat_id,
                                               text=structures.get_invalid_address_text(structures.Lang(lang)))

    raw_all_admin_message_data = await cache.get("admin_message_data")
    all_admin_message_data = {}
    if raw_all_admin_message_data:
        all_admin_message_data = json.loads(raw_all_admin_message_data)

    if str(chat_id) in all_admin_message_data:
        admin_message_data = all_admin_message_data[str(chat_id)]
        if admin_message_data["waiting_for_message"]:
            message = update.message
            admin_message_data["waiting_for_message"] = 0
            admin_message_data["message"] = str(base64.b64encode(pickle.dumps(message)), "utf-8")
            await message.copy(chat_id=chat_id)
            await context.bot.send_message(chat_id=chat_id,
                                           text=structures.admin_message_text_confirmation,
                                           reply_markup=structures.get_admin_message_confirmation_keyboard())
        if admin_message_data["waiting_for_button_title"]:
            admin_message_data["waiting_for_button_title"] = 0
            admin_message_data["button_title"] = update.message.text

            await context.bot.send_message(chat_id=chat_id,
                                           text=structures.get_admin_message_button_title_confirmation(
                                               update.message.text),
                                           reply_markup=structures.get_admin_message_button_title_confirmation_keyboard())
        if admin_message_data["waiting_for_button_url"]:
            admin_message_data["waiting_for_button_url"] = 0
            admin_message_data["button_url"] = update.message.text

            await context.bot.send_message(chat_id=chat_id,
                                           text=structures.get_admin_message_button_url_confirmation(
                                               update.message.text),
                                           reply_markup=structures.get_admin_message_button_url_confirmation_keyboard())
        all_admin_message_data[str(chat_id)] = admin_message_data
        await cache.set("admin_message_data", json.dumps(all_admin_message_data))


if __name__ == '__main__':
    application = ApplicationBuilder().token(structures.token).build()

    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(init_cache())

    database.add_table(users_table)

    start_handler = CommandHandler('start', start)
    admin_handler = CommandHandler('admin', admin_panel)
    message_handler = MessageHandler(~filters.COMMAND, message_handler)
    application.add_handler(start_handler)
    application.add_handler(admin_handler)
    application.add_handler(message_handler)
    application.add_handler(CallbackQueryHandler(callback_handler))

    application.run_polling()
