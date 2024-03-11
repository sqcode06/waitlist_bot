from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import urllib.parse

from enum import Enum


class Lang(Enum):
    EN = "en"
    RU = "ru"


token = "6413387680:AAGREejqioV_S595JCu_NnGiWriGxbQM5FU"  # ENTER TOKEN
tonapi_key = "AEUQULLLKXBKBKQAAAAFEDA7EKEFIR2NCVW2SEZLBSBQYPB5C4MAHYS5ZBUVLFEJMAQRZ5A"

choose_language_message = '''Choose language
_________ 

Выберите язык'''

admin_statistics_loading_text = '''Statistics:
    Total users: ...,
    Total users subscribed: ...
'''

admin_panel_text = "Admin panel"
admin_send_message_text = "Send me the message!"
admin_message_text_confirmation = "Is this your message?"
admin_message_button_question = "Add buttons?"
admin_message_button_title_question = "Send me the button label"
admin_message_button_url_question = "Send me the button url"
admin_message_confirmation_send_text = "Send the message?"
messages_sent_text = "Messages sent!"


def get_enter_address_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return '''<b>Welcome to Gemz Trade Waitlist Bot!</b>

Enter your TON wallet below to join'''
    if lang == Lang.RU:
        return '''<b>Добро пожаловать в лист ожидания Gemz Trade!</b>

Введите адрес вашего TON кошелька'''


def get_invalid_address_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return "Wrong format, check your address"
    if lang == Lang.RU:
        return "Неправильный формат, проверьте адрес вашего кошелька"


def get_raw_form_address_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return "Enter your TON wallet NOT in raw form"
    if lang == Lang.RU:
        return "Введите адрес вашего TON кошелька НЕ в raw формате"


def get_valid_address_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return '''Great, last step!

Subscribe to @gemztrade before joining waitlist'''
    if lang == Lang.RU:
        return '''Отлично, последний шаг! 

Подпишись на @gemztrade, чтобы попасть в лист ожидания'''


def get_not_subscribed_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return "You are not subscribed to the @gemztrade channel, subscribe and click the button below"
    if lang == Lang.RU:
        return "Вы не подписаны на канал @gemztrade, подпишитесь и нажмите кнопку ниже"


def get_restart_message(lang: Lang) -> str:
    if lang == Lang.EN:
        return "You are already in the waitlist, click the button below to return to the menu"
    if lang == Lang.RU:
        return "Вы уже в листе ожидания, нажмите на кнопку ниже, чтобы перейти в меню"


def get_share_message_text(user_id: int, lang: Lang) -> str:
    if lang == Lang.RU:
        return f'''💎 Присоединяйтесь к листу ожидания Gemz Trade, выигрывайте WL и зарабатывайте TON

Gemz Trade - #1 трейдинг платформа на TON

- 🏆 Выиграйте WL - Приглашайте друзей по вашей реферальной ссылке, WL будут разыграны между лучшими участниками.
- 💰 Получайте до 30% от комиссий ваших рефералов, когда они начнут торговать с Gemz.

👉 https://t.me/GemzTradeBot?start={user_id}
'''
    if lang == Lang.EN:
        return f'''💎 Join Gemz Trade Waitlist, win WL and earn TON

Gemz Trade -  #1 Trading Platform on TON

- 🏆 Win WL - Invite friends using your referral link, WLs will be raffled between top participants.
- 💰 Get up to 30% of your referral fees, when they start trading with Gemz.

👉 https://t.me/GemzTradeBot?start={user_id}
'''


def get_presale_standby_text(lang: Lang):
    if lang == Lang.EN:
        return '''
<b><u>GEMZ PASS mint has not started yet.</u></b>

Invite friends, be on TOP - win WL and earn TON from the referrals' trading fees

If you get to win WL, it will appear here
'''
    if lang == Lang.RU:
        return '''
<b><u>Минт GEMZ PASS еще не начался.</u></b>

Приглашайте друзей, будьте в ТОПе - выиграйте WL и зарабатывайте TON с комиссий ваших рефералов

Если вам удастся выиграть WL, он появится здесь
'''


def get_presale_proceed_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return '''<b><u>GEMZ PASS MINT</u></b>

🎉 Congratulations, you recieved WL - 20 TON discount and mint priority

Don’t miss the mint on <b>12 March 12:00 UTC!</b>

<b><a href="https://tonraffles.app/nft/launchpad/EQAZO_HuoR3aP7Pmi5kE3h91mmp4J5OwhbMcrkZlwSMVDt3M">MINT HERE!</a></b>'''
    if lang == Lang.RU:
        return '''<b><u>Минт GEMZ PASS</u></b>

🎉 Поздравляем, Вы получили WL - скидку на минт 20 ТОН и приоритет в очереди.

Не пропустите минт <b>12 Марта 12:00 UTC!</b>

<b><a href="https://tonraffles.app/nft/launchpad/EQAZO_HuoR3aP7Pmi5kE3h91mmp4J5OwhbMcrkZlwSMVDt3M">МИНТ ТУТ!</a></b>'''


def get_presale_fail_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return '''<b><u>GEMZ PASS MINT</u></b>

Don’t miss the mint on <b>12 March 12:00 UTC!</b>

Get WL here: https://getgems.io/collection/EQCvDh92MohIpsSbA0eH_94cLnvEmvx-Sv2PorNqQRf42Kue

<b><a href="https://tonraffles.app/nft/launchpad/EQAZO_HuoR3aP7Pmi5kE3h91mmp4J5OwhbMcrkZlwSMVDt3M">MINT HERE!</a></b>'''
    if lang == Lang.RU:
        return '''<b><u>Минт GEMZ PASS</u></b>

Не пропустите минт <b>12 Марта 12:00 UTC!</b>

Получить WL можно здесь: https://getgems.io/collection/EQCvDh92MohIpsSbA0eH_94cLnvEmvx-Sv2PorNqQRf42Kue

<b><a href="https://tonraffles.app/nft/launchpad/EQAZO_HuoR3aP7Pmi5kE3h91mmp4J5OwhbMcrkZlwSMVDt3M">МИНТ ТУТ!</a></b>'''


def get_menu_text(rank: int, user_id: int, lang: Lang) -> str:
    if lang == Lang.EN:
        return f'''<b><u>Congratulations! You joined Gemz Trade waitlist competition.</u></b>

<b>Your waitlist place - {rank}</b>


<b>Here you can earn TON and get your WL spot.</b> How? 

🏆 <b>Win WL</b> - Invite friends using your referral link, WLs will be raffled between top participants.

💰 <b>Get up to 30%</b> of your referral fees, when they start trading with Gemz


<b>Your Referral Link:</b> <code><b>https://t.me/GemzTradeBot?start={user_id}</b></code>'''
    if lang == Lang.RU:
        return f'''<b><u>Поздравляем! Вы попали в лист ожидания Gemz Trade.</u></b>

<b>Ваше место в листе ожидания - {rank}</b>


<b>Здесь вы можете заработать TON и получить свое место в WL.</b> Как?

🏆 <b>Выйграйте WL</b> - Приглашайте друзей по своей реферальной ссылке, WL будут разыграны между лучшими участниками.

💰 <b>Получайте до 30%</b> от комиссий ваших рефералов, когда они начнут торговать с Gemz


<b>Ваша реферальная ссылка:</b> <code><b>https://t.me/GemzTradeBot?start={user_id}</b></code>'''


def get_ref_dashboard_text(referees: int, user_id: int, lang: Lang) -> str:
    if lang == Lang.EN:
        return f'''
People invited:  {referees}

🏆 <b>Win WL</b> - Invite friends using your referral link, WLs will be raffled between top participants.

💰 <b>Get up to 30%</b> of your referral fees, when they start trading with Gemz

<b>Your Referral Link:</b> <code><b>https://t.me/GemzTradeBot?start={user_id}</b></code>'''
    if lang == Lang.RU:
        return f'''
Приглашено друзей:  {referees}

🏆 <b>Выйграйте WL</b> - Приглашайте друзей по своей реферальной ссылке, WL будут разыграны между лучшими участниками.

💰 <b>Получайте до 30%</b> от комиссий ваших рефералов, когда они начнут торговать с Gemz

<b>Ваша реферальная ссылка:</b> <code><b>https://t.me/GemzTradeBot?start={user_id}</b></code>'''


def get_faq_text(lang: Lang):
    if lang == Lang.EN:
        return '''❓<u><b>FAQ</b></u>

<b>1. What is Gemz Trade?</b>
Gemz Trade - #1 Trading App on TON, which includes features such as:
- Buy/Sell first with fast Buy and Sell functionality 
- Sniping
- Advanced PnL
- Copy Trading
- Limit Orders
- and others ;)

<b>2. What is Waitlist?</b>
Waitlist participants will receive:
- Access to the open beta version
- Monthly income of up to 30% from trading commissions of invited referrals
- $GEMZ Airdrop
- Raffle of 25 WL, between top inviters


<b>3. What is WL?</b>
WL (White List) - selected Gemz Trade community members who will receive a 20 TON discount on GEMZ PASS mint. Participate in activities in our community to get WL.


<b>4. How can I earn TON?</b>
- Each of your invited friends will pay trading fees and you will receive up to 30% of these commissions
- Invite friends and get $GEMZ Airdrop


<b>5. GEMZ PASS Benefits</b>
GEMZ PASS offers exclusive benefits, including:
- 0% Trading Fee for EVER
- Revenue Share from Gemz Trading Fees 
- Special $GEMZ Airdrop
- Access to the Private Gemz Trading Chat
- Access to the Closed Beta
- Increased Refferal Reward to 40%
- and much more :)


<b>6. Where to find friends?</b>
Send your referral link to chats, channels, twitter, discord, youtube, stories and so on. 
Try to invite as many friends as possible to get to the top and win WL.'''
    if lang == Lang.RU:
        return '''❓<u><b>Частые вопросы</b></u>

<b>1. Что такое Gemz Trade?</b>
Gemz Trade - #1 трейдинг платформа на TON, включающая такой функционал, как:
- Быстрая Покупка/Продажа
- Cнайпинг
- Продвинутый PnL
- Копитрейдинг
- Лимитные Ордера
- и другие :)

<b>2. Что такое лист ожидания?</b>
Участники листа ожидания получат:
- Доступ к открытой бета-версии
- Ежемесячный доход до 30% с трейдинг комиссий приглашенных рефералов
- $GEMZ Airdrop
- Розыгрыш 25 WL, между теми кто пригласит больше всего друзей


<b>3. Что такое WL?</b>
WL (White List) - избранные участники Gemz Trade комьюнити, которые получат скидку 20 TON на минт GEMZ PASS. Участвуйте в активностях в нашем комьюнити, чтобы получить WL.


<b>4. Как я могу на этом заработать?</b>
- Каждый из приглашенных вами друзей будет платить торговые комиссии при трейдинге, а вы будете получать до 30% от этих комиссий
- Приглашайте друзей и получите $GEMZ Airdrop


<b>5. Что дает GEMZ PASS</b>
GEMZ PASS предоставит эксклюзивные возможности:
- 0% Трейдинг комиссий НАВСЕГДА
- Особый $GEMZ Airdrop
- Ежемесячный доход с торговых комиссий Gemz
- Доступ к закрытой бета-версии
- Повышенное вознаграждение за рефералов до 40%
- Доступ к приватному чату трейдеров
- и многое другое :)


<b>6. Где найти друзей?</b>
Опубликуйте свою реферальную ссылку в чатах, каналах, twitter, discord, youtube, stories и так далее. 
Постарайтесь пригласить как можно больше друзей, чтобы попасть в топ и выиграть WL.'''


def get_admin_statistics_text(total_users: int, total_users_subscribed: int) -> str:
    return f'''Statistics:
    Total users: {total_users},
    Total users subscribed: {total_users_subscribed}
    '''


def get_admin_message_button_title_confirmation(button_title: str) -> str:
    return f"Is this correct title for the button?\n\n{button_title}"


def get_admin_message_button_url_confirmation(button_url: str) -> str:
    return f"Is this correct url for the button?\n\n{button_url}"


def get_same_address_exists_text(lang: Lang) -> str:
    if lang == Lang.EN:
        return "A user with the same address already exists. Try with another address"
    if lang == Lang.RU:
        return "Пользователь с таким адресом уже существует. Воспользуйтесь другим адресом"


def get_choose_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('🇬🇧 English', callback_data="choose_language_en")],
        [InlineKeyboardButton('🇷🇺 Russian', callback_data="choose_language_ru")]
    ])


def get_subscription_check_keyboard(lang: Lang) -> InlineKeyboardMarkup:
    if lang == Lang.EN:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton('Check', callback_data="subscription_check")
        ]])
    if lang == Lang.RU:
        return InlineKeyboardMarkup([[
            InlineKeyboardButton('Проверить', callback_data="subscription_check")
        ]])


def get_menu_keyboard(user_id: int, lang: Lang) -> InlineKeyboardMarkup:
    if lang == Lang.EN:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Share Referral Link',
                                  url=f"https://t.me/share/url?url= &text={urllib.parse.quote(get_share_message_text(user_id, Lang.EN))}")],
            [InlineKeyboardButton('Referral Dashboard', callback_data="ref_dashboard")],
            [InlineKeyboardButton('GEMZ PASS SALE', callback_data="whitelist_presale")],
            [InlineKeyboardButton('FAQ', callback_data="faq")]
        ])
    if lang == Lang.RU:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Поделиться реферальной ссылкой',
                                  url=f"https://t.me/share/url?url= &text={urllib.parse.quote(get_share_message_text(user_id, Lang.RU))}")],
            [InlineKeyboardButton('Реферальная сводка', callback_data="ref_dashboard")],
            [InlineKeyboardButton('GEMZ PASS SALE', callback_data="whitelist_presale")],
            [InlineKeyboardButton('Частые вопросы', callback_data="faq")]
        ])


def get_return_to_menu_keyboard(lang: Lang, faq: bool) -> InlineKeyboardMarkup:
    if faq:
        if lang == lang.RU:
            return InlineKeyboardMarkup([[
                InlineKeyboardButton('Вернуться в меню', callback_data="return_to_menu"),
                InlineKeyboardButton('Частые вопросы', callback_data="faq")
            ]])
        if lang == lang.EN:
            return InlineKeyboardMarkup([[
                InlineKeyboardButton('Return to menu', callback_data="return_to_menu"),
                InlineKeyboardButton('FAQ', callback_data="faq")
            ]])
    else:
        if lang == lang.RU:
            return InlineKeyboardMarkup([[
                InlineKeyboardButton('Вернуться в меню', callback_data="return_to_menu")
            ]])
        if lang == lang.EN:
            return InlineKeyboardMarkup([[
                InlineKeyboardButton('Return to menu', callback_data="return_to_menu")
            ]])


def get_admin_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('Statistics', callback_data="admin_statistics"),
        InlineKeyboardButton('Send message to users', callback_data="admin_send_message"),
        InlineKeyboardButton('Export database to CSV', callback_data="admin_export_csv")
    ]])


def get_admin_statistics_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton('Refresh', callback_data="admin_statistics"),
        InlineKeyboardButton('Return', callback_data="return_to_admin_panel")
    ]])


def get_admin_message_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Yes', callback_data="admin_message_confirmation_yes")],
        [InlineKeyboardButton('Retry', callback_data="admin_message_confirmation_retry")],
        [InlineKeyboardButton('Abort', callback_data="return_to_admin_panel")]
    ])


def get_admin_button_question_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Add button', callback_data="admin_message_button_add")],
        [InlineKeyboardButton('Next', callback_data="admin_message_confirmation_send")]
    ])


def get_admin_message_button_title_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Yes', callback_data="admin_message_button_title_confirmation_yes")],
        [InlineKeyboardButton('Retry', callback_data="admin_message_button_title_confirmation_retry")],
        [InlineKeyboardButton('Abort', callback_data="return_to_admin_panel")]
    ])


def get_admin_message_button_url_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Yes', callback_data="admin_message_confirmation_yes")],
        [InlineKeyboardButton('Retry', callback_data="admin_message_button_url_confirmation_retry")],
        [InlineKeyboardButton('Abort', callback_data="return_to_admin_panel")]
    ])


def get_admin_message_confirmation_send_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('Yes', callback_data="admin_send_message_confirmed")],
        [InlineKeyboardButton('Abort', callback_data="return_to_admin_panel")]
    ])


def get_faq_keyboard(lang: Lang) -> ReplyKeyboardMarkup:
    if lang == Lang.EN:
        return ReplyKeyboardMarkup([[
            KeyboardButton("FAQ")
        ]])
    if lang == Lang.RU:
        return ReplyKeyboardMarkup([[
            KeyboardButton("Частые вопросы")
        ]])
