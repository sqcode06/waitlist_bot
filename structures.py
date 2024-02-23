from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import urllib.parse

from enum import Enum


class Lang(Enum):
    EN = "en"
    RU = "ru"


token = ""  # ENTER TOKEN

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
        return "Вы уже в WL, нажмите на кнопку ниже, чтобы перейти в меню"


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
<b><u>The NFT PASS sale has not started yet.</u></b>

Invite friends, be on TOP - win WL and earn TON from the referrals' trading fees

If you get to win WL, it will appear here
'''
    if lang == Lang.RU:
        return '''
<b><u>Продажа NFT PASS еще не началась.</u></b>

Приглашайте друзей, будьте в ТОПе - выиграйте WL и зарабатывайте TON с комиссий ваших рефералов

Если вам удастся выиграть WL, он появится здесь
'''


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
Gemz Trade - #1 Trading Platform on TON. Features:
- Buy/Sell first with fast Buy and Sell functionality 
- Sniping
- Advanced PnL
- Copy Trading
- Limit Orders
- and others ;)

<b>2. What is waitlist?</b>
Waitlist - waitlist participants will get access to open beta.

<b>3. What is WL?</b>
WL - White List, access to discount on NFT PASS mint. 

<b>4. How can I earn TON?</b>
- If you invite friends and win WL NFT, you mint NFT PASS with 25% discount and sell higher on Get Gems for example. 
- Each of your invited friend will pay trading fees when trading and you will get up 30% from it.

<b>5. WL NFT Benefits</b>
WL NFT provides 25% discount for NFT PASS mint.

<b>6. NFT PASS Benefits</b>
Gemz Trade NFT PASS will provide exclusive features:
- 0% Trading Fee for EVER
- Access to closed beta - trade on Gemz first and make cash $ 
- Private Chat for PASS holders  
- and more :)

<b>7. Where to find friends?</b>
Send your referral link to chats, channels, twitter, discord, youtube, stories and so on. 
Try to invite as most as possible to get in top and win WL.'''
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
Лист ожидания - участники листа ожидания получат доступ к открытой бета-версии.

<b>3. Что такое WL?</b>
WL - White List, доступ к скидке на минт NFT PASS. 

<b>4. Как я могу на этом заработать?</b>
- Если вы пригласите друзей и выиграете WL NFT, вы сминтите NFT PASS со скидкой 25% и продадите дороже, например, на Get Gems. 
- Каждый из приглашенных вами друзей будет платить торговые комиссии при трейдинге, а вы будете получать до 30% от этих комиссий.

<b>5. Что дает WL NFT?</b>
WL NFT предоставляет 25% скидку на минт NFT PASS.

<b>6. Что дает NFT PASS?</b>
Gemz Trade NFT PASS предоставит эксклюзивные возможности:
- 0% комиссии за трейдинг НАВСЕГДА
- Доступ к закрытой бета-версии - торгуйте на Gemz первыми и зарабатывайте кэш $
- Приватный чат для владельцев NFT PASS  
- и многое другое :)

<b>7. Где найти друзей?</b>
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
            [InlineKeyboardButton('NFT PASS SALE', callback_data="whitelist_presale")],
            [InlineKeyboardButton('FAQ', callback_data="faq")]
        ])
    if lang == Lang.RU:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Поделиться реферальной ссылкой',
                                  url=f"https://t.me/share/url?url= &text={urllib.parse.quote(get_share_message_text(user_id, Lang.RU))}")],
            [InlineKeyboardButton('Реферальная сводка', callback_data="ref_dashboard")],
            [InlineKeyboardButton('NFT PASS SALE', callback_data="whitelist_presale")],
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
