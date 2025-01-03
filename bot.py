import sqlite3
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Bot tokeni
TOKEN = '7505093385:AAEGwLI1AJOjukHTnKfkWgUj6MIOMKewOOo'

# SQLite verilənlər bazasına qoşulma və cədvəl yaratma
conn = sqlite3.connect('orders.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS deleted_orders (id INTEGER PRIMARY KEY, order_detail TEXT)''')
conn.commit()


# Əsas menyu funksiyası
async def start(update: Update, context: CallbackContext) -> None:
    welcome_message = (
        "Привет! Меня зовут Умами🍣🥢, и я предоставляю услугу доставки еды.\n\n"
        "Просто выберите пункт в меню и сделайте заказ или получите более подробную информацию..\n\n"
        "Наша служба доставки еды предоставляет быстрые, удобные и качественные блюда. "
        "Вы можете заказать еду из ближайших ресторанов, и мы доставим её прямо к вам домой🚗."
    )
    keyboard = [['🍣Меню', '💬 Информация'], ['🎉Акции', '📞Контакты'], ['👩‍💻Веб-сайт', '🗑Корзина']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


# Menü funksiyası
async def menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Хосомаки и Футомаки роллы 🍣", callback_data='sushi')],
        [InlineKeyboardButton("Урамаки ролль 🍱", callback_data='rolls')],
        [InlineKeyboardButton("Запечённые роллы 🍜", callback_data='soups')],
        [InlineKeyboardButton("Темпуры роллы 🍰", callback_data='desserts')],
        [InlineKeyboardButton("Нигири и Гюнкан 🍣", callback_data='nigiri')],
        [InlineKeyboardButton("Закуски и салаты 🍱", callback_data='snacks')],
        [InlineKeyboardButton("Меню 🍣", callback_data='menu')],
        [InlineKeyboardButton("Супь и Wok 🍜", callback_data='wok')],
        [InlineKeyboardButton("Сашими 🍣", callback_data='sashimi')],
        [InlineKeyboardButton("Роллы от шефа 🍣", callback_data='chef')],
        [InlineKeyboardButton("Сеть 🌐", callback_data='network')],
        [InlineKeyboardButton("Добавки 🍶", callback_data='additives')],
        [InlineKeyboardButton("Напитки 🍹", callback_data='drinks')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # update.message kontrolü
    if update.message:
        await update.message.reply_text("🍱 Menü", reply_markup=reply_markup)
    elif update.callback_query:
        # Callback query durumunu ele al
        await update.callback_query.message.reply_text("🍱 Menü", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()  # Callback query cavablandırılır

    if query.data == 'add_to_cart':
        await query.edit_message_text(text="Seçdiyiniz məhsul səbətə əlavə edildi!")
    elif query.data == 'back_to_menu':
        await query.edit_message_text(text="🍱 Menüə geri qayıtdınız.")
        await menu(update, context)
    elif query.data == 'select_quantity':
        await query.edit_message_text(text="Neçə ədəd seçmək istəyirsiniz? (Məsələn, '3' yazın)")
    elif query.data == 'sushi':
        await query.edit_message_text(text="Хосомаки и Футомаки роллы 🍣\n\n")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/8480c47be00d9619e71abd2b38c5ffbca62b7dc800410dc3e3e69a425724ce0c/6771c2c9/cAv90-koGPMID3856T0QhhTZlioVJaUiwhAAerDWHL9VGchhYPVbZoPzQAeOWTvxk9kh9SqB5rxLb-vV5hICHw%3D%3D?uid=0&filename=DSC_1047.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Хосомаки и Футомаки роллы")
        await show_options(query)
    elif query.data == 'rolls':
        await query.edit_message_text(text="Урамаки ролль 🍱\n\n")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/6cc362e869f69f8b06e3d72eef519a449fcf74e65120132d9cfeaf8611409cc2/6771c2c9/1I4yTB6YPHZQiKrAkswmFBTZlioVJaUiwhAAerDWHL8sTF8XK7D3pkgZvre2R7zZAnGrfCIzvlasdbdYWYOa-A%3D%3D?uid=0&filename=DSC_1063.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Урамаки ролль")
        await show_options(query)
    elif query.data == 'soups':
        await query.edit_message_text(text="Запечённые роллы 🍜\n\n")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/18820cee9fc85552285d45d118f28b2a11f99b2c9ff44e6e9719d4761f999543/6771c2c9/S3EoL1W3CeQYleTBF2rmwRTZlioVJaUiwhAAerDWHL_nNf3b5l8pzLN1HDwj1rl3h8EEdfl6pjvDb7qsGTdnEQ%3D%3D?uid=0&filename=DSC_1073.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Sobada bişirilən rollar")
        await show_options(query)
    elif query.data == 'desserts':
        await query.edit_message_text(text="Темпуры роллы 🍰\n\n Темпуры роллы")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/3177f79ea24ba3d8ff1e20bbc2caf7a298443c5e3a868ac7ff0a6d19c3c9e43a/6771c2c9/wQkxdlyxuOAk1iRI8mHwqAQ3bLLkLcowMCVK5fKH1SLY9il2soV39_Eg0X6oqlnZZgJiseSSSm4bMdFnGc9QjA%3D%3D?uid=0&filename=DSC_1093.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Tempura rolları")
        await show_options(query)
    elif query.data == 'nigiri':
        await query.edit_message_text(text="Нигири и Гюнкан 🍣\n\nMəlumat: Nigiri və Gyunkan suşi.")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/06a1834fa2076a09390d1b0b4f1f84b27bba10a0d4bbf9e1d34a3844c561635f/6776ccc2/SP-v__kLpMBpYlRwWlNJu3nLercz3c6NzttiCMlPcl5liHfJYSwv5eLpKCO1awHjW73S3WiXikirCQccoQR4Wg%3D%3D?uid=0&filename=DSC_1102.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Nigiri və Gyunkan suşisi")
        await show_options(query)
    elif query.data == 'snacks':
        await query.edit_message_text(text="Закуски и салаты 🍱\n\nMəlumat: Çeşidli salatlar və qəlyanaltılar.")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/c57835db64109cb6d51605872f90408b91f814f3552b458ef6758a9f8e41b1be/6776ccc2/Ft11foOPDgv8XG4rxJOATLIVP1pqSSvN906Vqepk3fkrCdP8-XYJR80o4l-kEmURMQYRewcF2q6pxm0g9uJ1dQ%3D%3D?uid=0&filename=DSC_1105.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Çeşidli salatlar və qəlyanaltılar")
        await show_options(query)
    elif query.data == 'wok':
        await query.edit_message_text(text="Супь и Wok 🍜\n\nMəlumat: Wok yeməkləri və şorbalar.")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/48f351d4f94dddd87a04ceb85b712e3d93d1b98ac33ad0cb785b8d9bf2744622/6776ccc2/Yk1AZQW8Aph5_BPJM1jw62jlziapQVenX953dkt2WHiGhsbmXO4ioO7qHTUfKYn4QleoYNO-kKHsKtk_lSL5sQ%3D%3D?uid=0&filename=DSC_1116.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Wok yeməkləri")
        await show_options(query)
    elif query.data == 'sashimi':
        await query.edit_message_text(text="Сашими 🍣\n\nMəlumat: Xam balıq parçaları.")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/ebf45e13a8499b950fd2ed4b913e3f600132561137a1c433d09428914662b936/6776ccc2/yU_F0bsM5sbF5P246MktOMjAKhgJDBTganDisG8lC9Oa4ipZtTR1Yrgdy7muK_1XfHOD7KZWybhqFadSeerEjw%3D%3D?uid=0&filename=DSC_1121.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Xam balıq parçaları")
        await show_options(query)
    elif query.data == 'chef':
        await query.edit_message_text(text="Роллы от шефа 🍣\n\nMəlumat: Şefin özəl rolu.")
        await query.message.reply_photo(
            photo="https://downloader.disk.yandex.ru/preview/4e1689535768e67b3786f8264c385ddc97e442a44d661e8cc02c1ee01079d30e/6776ccc2/TBlwpAtm7alYj9gzlCuzlUHqybfg6rPlekc58m1K5Q7i5Au4AXV9Vob6zQVlw1vIQqy9y99803C_4O1x_Ryn5Q%3D%3D?uid=0&filename=DSC_1124.jpg&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=1898x912",
            caption="Şefin özəl rolu")
        await show_options(query)
    elif query.data == 'network':
        await query.edit_message_text(text="Сеть 🌐")
        await show_options(query)
    elif query.data == 'additives':
        await query.edit_message_text(text="Добавки 🍶\n\nMəlumat: Əlavə məhsullar.")
        await show_options(query)
    elif query.data == 'drinks':
        await query.edit_message_text(text="Напитки 🍹\n\nMəlumat: İçkilər.")
        await show_options(query)


async def show_options(query):
    keyboard = [
        [InlineKeyboardButton("Добавить в корзину 🛒", callback_data='add_to_cart')],
        [InlineKeyboardButton("Назад 🔙", callback_data='back_to_menu')],
        [InlineKeyboardButton("Выбор количества 🧮", callback_data='select_quantity')]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Выглядит вкусно 🍣", reply_markup=reply_markup)

#
# async def options_button(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     await query.answer()




# İstifadəçi müəyyən ədəd seçdiyi zaman
async def select_quantity(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    try:
        quantity = int(user_input)
        await update.message.reply_text(f"{quantity} ədəd seçdiniz.")
    except ValueError:
        await update.message.reply_text("Xahiş edirəm, düzgün bir ədəd daxil edin.")


# Əlaqə məlumatları funksiyası
async def contact_info(update: Update, context: CallbackContext) -> None:
    contact_message = (
        "📞 Контактная информация:\n\n"
        "✅ Телефон:+7 929 033 66 99\n"
        "✅ Email: info@company.com\n"
        "✅ Адрес: Борисоглебская 58 А\n\n"
        "Мы будем рады вам помочь!"
    )
    await update.message.reply_text(contact_message)


# İnformasiya funksiyası
async def info(update: Update, context: CallbackContext) -> None:
    info_message = (
        "📍 Информация о ресторане:\n\n"
        "✅ Название: Умами Суши 🍣\n"
        "✅ Услуги: Быстрая и качественная доставка еды.\n"
        "✅ Время доставки:\n"
        "  • пн-чт, вс : 12:00 - 23:00\n"
        "  • пт, сб: 12:00 - 01:00\n\n"
        "✅ Минимальная сумма заказа:\n"
        "  • Обнинск: 1000 р.\n"
        "  • Кривское, Экодолье, Белкино, Борисоглебская, Кабицыно: 1500 р.\n"
        "🛵 Для получения более подробной информации ознакомьтесь с нашим меню."
    )
    await update.message.reply_text(info_message)


# Akciya funksiyası
async def discounts(update: Update, context: CallbackContext) -> None:
    image_url = 'https://r.resimlink.com/7Qf_XzqGF.jpg'  # Əsl şəkil URL-i ilə əvəz edin
    await update.message.reply_photo(photo=image_url, caption="🎉 Специальные акции! Не пропустите!")


# Veb-saytı göndərmə funksiyası
async def website(update: Update, context: CallbackContext) -> None:
    website_url = 'https://umami.com.ru/'  # Əsl sayt URL-i ilə əvəz edin
    await update.message.reply_text(f"👩‍💻 Наш сайт: {website_url}\n\nВы можете посетить наш сайт, чтобы узнать больше!")


# Sepet fonksiyonu
async def cart(update: Update, context: CallbackContext) -> None:
    cart_message = (
        "🗑 Корзина:\n\n"
        "Здесь будут отображаться ваши заказы. Пока корзина пуста."
    )
    await update.message.reply_text(cart_message)


# Komandaların və mesajların idarə edilməsi
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Komandaların qeydiyyatı
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^🍣Меню$'), menu))
    application.add_handler(MessageHandler(filters.Regex('^💬 Информация$'), info))
    application.add_handler(MessageHandler(filters.Regex('^📞Контакты$'), contact_info))
    application.add_handler(MessageHandler(filters.Regex('^🎉Акции$'), discounts))
    application.add_handler(MessageHandler(filters.Regex('^👩‍💻Веб-сайт$'), website))
    application.add_handler(MessageHandler(filters.Regex('^🗑Корзина$'), cart))

    # Callback handler for inline buttons
    application.add_handler(CallbackQueryHandler(button))

    # Botun işə salınması
    application.run_polling()


if __name__ == "__main__":
    main()
