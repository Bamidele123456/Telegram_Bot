from telegram import Update, Bot, ReplyKeyboardMarkup,InputMediaDocument, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, User, ChatMember, Chat
from datetime import datetime
import telegram
import asyncio
import json
from telegram.ext import Application, CommandHandler,ConversationHandler, MessageHandler, filters, ContextTypes, CallbackContext, \
    CallbackQueryHandler
from typing import Final
import base64
import time
import io


SIZE, NUMBER, EMAIL, PHONE, ADDRESS = range(5)

def byte_image(image):
    image_bytes = base64.b64decode(image)
    return image_bytes

async def start(update: Update, context: CallbackContext) -> None:
    userid = 1111
    detail = user_collection.find_one({"userid": userid})
    buisness = detail.get("buisness-name", "")
    message_type: str = update.message.chat.type
    message = update.message
    username: str = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name if update.message.from_user.last_name else ""
    user: User = update.message.from_user
    chat_id = update.message.chat.id
    text: str = update.message.text
    keyboard = [
        [
            InlineKeyboardButton("Product", callback_data='product'),
            InlineKeyboardButton("Services", callback_data='services'),
            InlineKeyboardButton("FAQ", callback_data='faq'),
        ],
    ]
    sentb = await context.bot.send_message(
        chat_id=message.chat_id,
        text=f'Hello {first_name} {last_name} Welcome to {buisness} your number 1 store for clothing and services what can we help you with today',
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    context.user_data['sentb'] = sentb.message_id



async def buttonc(update: Update, context: CallbackContext) -> int:
    userid = 1111
    query = update.callback_query
    data = query.data
    message = update.effective_message
    chat_id = message.chat_id
    if data == 'product':
        details = category.find_one(({"userid": userid}))
        keyboard = []
        if details:
            categorys = details.get("categories", '')
            for detail in categorys:
                keyboard.append([InlineKeyboardButton(detail, callback_data=f"category_{detail}")])

            sent_message = await context.bot.send_message(
                chat_id=message.chat_id,
                text='What kind of product do you want to purchase',
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['sent_message_id'] = sent_message.message_id
        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text='There are no products'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)


    elif data == 'services':
        details = scategory.find_one(({"userid": userid}))
        keyboard = []
        if details:
            services = details.get("categories", '')
            for detail in services:
                keyboard.append([InlineKeyboardButton(detail, callback_data=f"scategory_{detail}")])

            sent_message = await context.bot.send_message(
                chat_id=message.chat_id,
                text='What kind of service do you need:',
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['sent_message_id'] = sent_message.message_id
        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text='There are no services'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)
    elif data == 'faq':
        details = faq.find_one({"userid":userid})
        if details:
            questions = details.get("question")
            answers = details.get("answers")
            faqs = zip(questions, answers)

            for question, answer in faqs:
                question = question.get("question", '')
                answer = answer.get("answer", '')
                await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f'{question}\n{answer}'
                )

        else:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no faq'
            )


async def buttons(update: Update, context: CallbackContext) -> None:
    userid = 1111
    query = update.callback_query
    data = query.data
    message = update.effective_message
    chat_id = message.chat_id
    if data.startswith('category_'):
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        name = data.split('_')[1]
        details = dpictures.find({"category":name})
        subs = []
        keyboard = []
        if details:
            for detail in details:
                sub = detail.get("sub",'')
                subs.append(sub)
            if subs:
                for sub in subs:
                    keyboard.append([InlineKeyboardButton(sub, callback_data=f"sub_{sub}")])
                sent_message = await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f'What type of {name} are you looking for',
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                context.user_data['sent_message_id'] = sent_message.message_id
            else:
                send = await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f'There are no subcategory for this category'
                )
                time.sleep(3)
                await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)



        else:
            sent_message = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no subcategory for this category'
            )
    elif data.startswith('scategory_'):
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        name = data.split('_')[1]
        details = services.find({"category": name})
        subs = []
        keyboard = []
        if details:
            for detail in details:
                sub = detail.get("sub", '')
                subs.append(sub)
            if subs:
                for sub in subs:
                    keyboard.append([InlineKeyboardButton(sub, callback_data=f"ssub_{sub}")])
                sent_message = await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f'what kind of {name} are you looking for',
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode='Markdown'
                )
                context.user_data['sent_message_id'] = sent_message.message_id
            else:
                send = await context.bot.send_message(
                    chat_id=message.chat_id,
                    text=f'There are no subcategory for this category'
                )
                time.sleep(3)
                await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)

        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no subcategory for this category'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)



async def buttonp(update: Update, context: CallbackContext) -> None:
    userid = 1111
    query = update.callback_query
    data = query.data
    message = update.effective_message
    chat_id = message.chat_id
    if data.startswith('sub_'):
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        name = data.split('_')[1]
        products = []
        keyboard = []
        details = dpictures.find({"sub":name})
        if details:
            for detail in details:
                product = detail.get("name",'')
                products.append(product)
            for product in products:
                keyboard.append([InlineKeyboardButton(product, callback_data=f"product_{product}")])
            sent_message = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'What kind of {name} are you looking for?',
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['sent_message_id'] = sent_message.message_id
        else:
            send =await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no available product for this subcategory'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)
    elif data.startswith('ssub_'):
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        name = data.split('_')[1]
        servicess = []
        keyboard = []
        details = services.find({"sub":name})
        if details:
            for detail in details:
                service = detail.get("name", '')
                servicess.append(service)
            for service in servicess:
                keyboard.append([InlineKeyboardButton(service, callback_data=f"service_{service}")])
            sent_message = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'Wht kind of {name} are you looking for?',
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            context.user_data['sent_message_id'] = sent_message.message_id
        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no available service for this subcategory'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)


async def buttonv(update: Update, context: CallbackContext) -> None:
    userid = 1111
    query = update.callback_query
    data = query.data
    message = update.effective_message
    chat_id = message.chat_id
    if data.startswith('product_'):
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        name = data.split('_')[1]
        details = dpictures.find_one({"name": name})

        if details:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'Here is a list of awailable {name}'
            )


            vnames = json.loads(details.get("vname", "[]"))
            vprices = json.loads(details.get("vprice", "[]"))
            vquantities = json.loads(details.get("vquantity", "[]"))
            vsizes = json.loads(details.get("vsize", "[]"))
            vtypes = json.loads(details.get("vtype", "[]"))
            vcolors = json.loads(details.get("vcolor", "[]"))
            vimages = json.loads(details.get("vimage", "[]"))

            # Combine all the parsed details into a list of dictionaries
            variants = zip(vnames, vprices, vquantities, vsizes, vtypes, vcolors, vimages)

            for vname, vprice, vquantity, vsize, vtype, vcolor, vimage in variants:
                name = vname.get("vname", '')
                price = vprice.get("vprice", '')
                quantity = vquantity.get("vquantity", '')
                size = vsize.get("vsize", '')
                type = vtype.get("vtype", '')
                color = vcolor.get("vcolor", '')
                image = vimage.get("vimage", '')

                if image:
                    image_file = byte_image(image)

                    keyboard = [
                        [InlineKeyboardButton("Menu", callback_data='product')],
                        [InlineKeyboardButton("Buy", callback_data=f'variantp_{name}_{size}_{type}_{color}_{price}')]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    caption = (f"Name: {name}\nSize: {size}\nType: {type}\n"
                               f"Color: {color}\nQuantity: {quantity}\nPrice: {price}")

                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_file,
                        caption=caption,
                        reply_markup=reply_markup
                    )
                    context.user_data[f'{name}_{price}'] = image
        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no available variants for this product'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)
    elif data.startswith('service_'):
        name = data.split('_')[1]
        if 'sent_message_id' in context.user_data:
            # Determine the chat ID based on the type of update
            if message:
                chat_id = message.chat_id
            elif query:
                chat_id = query.message.chat_id
            else:
                print("No valid message or callback query found in the update")
                return

            # Delete the message containing the first set of buttons
            await context.bot.delete_message(chat_id, context.user_data['sent_message_id'])
        details = services.find_one({"name": name})

        if details:
            await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'Here is a list of available {name}'
            )

            vnames = json.loads(details.get("vname", "[]"))
            vprices = json.loads(details.get("vprice", "[]"))
            vimages = json.loads(details.get("vimage", "[]"))

            # Combine all the parsed details into a list of dictionaries
            variants = zip(vnames, vprices, vimages)

            for vname, vprice, vimage in variants:
                name = vname.get("vname", '')
                price = vprice.get("vprice", '')
                image = vimage.get("vimage", '')

                if image:
                    image_file = byte_image(image)

                    keyboard = [
                        [InlineKeyboardButton("Menu", callback_data='services')],
                        [InlineKeyboardButton("Buy", callback_data=f'variants_{name}_{price}')]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)

                    caption = (f"Name: {name}\n Price: {price}")

                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=image_file,
                        caption=caption,
                        reply_markup=reply_markup
                    )
                    context.user_data[f'{name}_{price}'] = image
        else:
            send = await context.bot.send_message(
                chat_id=message.chat_id,
                text=f'There are no available variants for this product'
            )
            time.sleep(3)
            await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)

async def buttond(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    message = update.effective_message
    data = query.data
    if data.startswith('variantp_'):
        _, name, size, type, color, price = data.split('_')
        context.user_data['name'] = name
        context.user_data['size'] = size
        context.user_data['type'] = type
        context.user_data['color'] = color
        context.user_data['price'] = price
        await query.answer('What is the quantity of product do you want?')
        sent_message = await context.bot.send_message(
            chat_id=message.chat_id,
            text=f'{name}\n{size}\n{type}\n{color}\n{price}\nWhat is the quantity of product do you want?'
        )
        context.user_data['sent_message_id'] = sent_message.message_id
        return SIZE
    if data.startswith('variants_'):
        _, name, price,= data.split('_')
        context.user_data['name'] = name
        context.user_data['price'] = price
        await query.answer('What is the quantity of product do you want?')
        sent_message = await context.bot.send_message(
            chat_id=message.chat_id,
            text=f'{name}\n{price}\nWhat is the quantity of product do you want?'
        )
        context.user_data['sent_message_id'] = sent_message.message_id
        return SIZE


async def size(update: Update, context: CallbackContext) -> int:
    quantity = update.message.text
    message = update.message
    context.user_data['quantity'] = quantity
    await context.bot.delete_message(update.message.chat_id, context.user_data['sent_message_id'])
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    sent_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text='What is your contact number so that we can contact you when your product arrives:'

    )
    context.user_data['sent_message_id'] = sent_message.message_id
    return NUMBER

async def number(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_input = message.text
    context.user_data['number'] = user_input
    await context.bot.delete_message(update.message.chat_id, context.user_data['sent_message_id'])
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    sent_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text='What is your email address'

    )
    context.user_data['sent_message_id'] = sent_message.message_id

    return EMAIL

async def email(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_input = message.text
    context.user_data['email'] = user_input
    await context.bot.delete_message(update.message.chat_id, context.user_data['sent_message_id'])
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    sent_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text=f'Input your phone number so that we can contact you when the product is being delivered'

    )
    context.user_data['sent_message_id'] = sent_message.message_id
    return PHONE

async def phone(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_input = message.text
    context.user_data['phone'] = user_input
    await context.bot.delete_message(update.message.chat_id, context.user_data['sent_message_id'])
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    sent_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text='Input your delivery address:'
    )
    context.user_data['sent_message_id'] = sent_message.message_id
    return ADDRESS

async def address(update: Update, context: CallbackContext) -> None:
    message = update.message
    user_input = message.text
    context.user_data['address'] = user_input
    name = context.user_data['name']
    size = context.user_data['size']
    type = context.user_data['type']
    email = context.user_data['email']
    color = context.user_data['color']
    price = context.user_data['price']
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name if update.message.from_user.last_name else ""
    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data='yes'),
            InlineKeyboardButton("NO", callback_data='no')
        ],
    ]
    phone = context.user_data['phone']
    image = context.user_data[f'{name}_{price}']
    await context.bot.delete_message(update.message.chat_id, context.user_data['sent_message_id'])
    await context.bot.delete_message(update.message.chat_id, update.message.message_id)
    sent_message = await context.bot.send_message(
        chat_id=message.chat_id,
        text=f'*Order Summary*\nYou"ll receive a payment link in your email to make payments for your order\nProduct Name:{name}\nSize:{size}\ntype:{type}\nColor:{color}\nPrice:{price}\n*Name of Buyer*:{first_name} {last_name}\n*Email*:{email}\nPhone Number:{phone}\nShipping Address:{user_input}\nIs the above correct?',
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    context.user_data['sent_message_id'] = sent_message.message_id
    return ConversationHandler.END

async def buttonyn(update: Update, context: CallbackContext) -> int:
    userid = 1111
    query = update.callback_query
    data = query.data
    message = update.effective_message
    chat_id = message.chat_id
    if data == 'yes':
        await context.bot.delete_message(query.message.chat_id, context.user_data['sent_message_id'])
        await context.bot.send_message(
            chat_id=message.chat_id,
            text='Hurray your order has been placed\nYou"ll revceive a payment link in your emialto make payments for your order\n*Order Tracking Code*:\nInput the code in order to track your order'
        )
        await context.bot.delete_message(query.message.chat_id, context.user_data['sentb'])
    if data == 'no':
        await context.bot.delete_message(query.message.chat_id, context.user_data['sent_message_id'])
        send = await context.bot.send_message(
            chat_id=message.chat_id,
            text='Ok'
        )
        await context.bot.delete_message(query.message.chat_id, context.user_data['sent_message_id'])
        time.sleep(3)
        await context.bot.delete_message(chat_id=chat_id, message_id=send.message_id)







async def cancel(update: Update, context: CallbackContext) -> None:
    message = update.message
    await context.bot.send_message(
        chat_id=message.chat_id,
        text='Your information has not been saved. Goodbye!'
    )
    return ConversationHandler.END







async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = 1111
    detail = user_collection.find_one({"userid":userid})
    buisness = detail.get("buisness-name","")
    message_type: str = update.message.chat.type
    message = update.message
    username: str = update.message.from_user.username
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name if update.message.from_user.last_name  else ""
    user: User = update.message.from_user
    chat_id = update.message.chat.id
    text: str = update.message.text
    keyboard = [
        [
            InlineKeyboardButton("Product", callback_data='product'),
            InlineKeyboardButton("Services", callback_data='services'),
            InlineKeyboardButton("FAQ", callback_data='faq'),
        ],
    ]
    sentb = await context.bot.send_message(
        chat_id=message.chat_id,
        text=f'Hello {first_name} {last_name} Welcome to {buisness} your number 1 store for clothing and services what can we help you with today',
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    context.user_data['sentb'] = sentb.message_id



if __name__ == '__main__':
    print('Starting ....')
    app = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(buttond, pattern='^(variantp_|variants_)')],
        states={
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, size)],
            NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, number)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(buttonc, pattern='^product$|^services$'))
    app.add_handler(CallbackQueryHandler(buttons, pattern='^(category_|scategory_)'))
    app.add_handler(CallbackQueryHandler(buttonp, pattern='^(sub_|ssub_)'))
    app.add_handler(CallbackQueryHandler(buttonv, pattern='^(product_|service_)'))
    app.add_handler(CallbackQueryHandler(buttond, pattern='^(variantp_|variants_)'))
    app.add_handler(CallbackQueryHandler(buttonyn, pattern='^yes$|^no$'))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    print('polling ....')
    app.run_polling(poll_interval=1)


