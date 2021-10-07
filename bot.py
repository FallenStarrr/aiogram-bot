import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BotBlocked
from os import getenv
from sys import exit
import aiogram.utils.markdown as fmt


#bot_token = getenv("BOT_TOKEN")
#if not bot_token:
#exit("Error: no toke provided")
#Обекс бота
bot = Bot(token='2093079493:AAG3rFaJDCLs7ta_R07fyIIEzhT7dij3U9M',
parse_mode=types.ParseMode.HTML)
#Диспетчер для бота
dp = Dispatcher(bot)
#Включаем логирование чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)





#Хэндлер на команду / test1
@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
  await message.reply("<b>Test 1</b>", parse_mode=types.ParseMode.HTML)

async def cmd_test2(message: types.Message):
  await message.reply("*Test 2*", parse_mode="MarkdownV2")

dp.register_message_handler(cmd_test2, commands="test2")

@dp.message_handler(commands="answer")
async def cmd_answer(message: types.Message):
  await message.answer("<s>Это простой ответ</s>", parse_mode="")


@dp.message_handler(commands="reply")
async def cmd_reply(message: types.Message):
  await message.reply("<u>Это ответ с ответом</u>")

@dp.message_handler(commands="text")
async def cmd_reply(message: types.Message):
  await message.answer(
     fmt.text(
       fmt.text(fmt.hunderline("Яблоки"), ",  вес 1 кг."),
       fmt.text("Старая цена:", fmt.hbold(25), "рублей"),
       sep="\n"
     )
  , parse_mode="HTML")

@dp.message_handler(commands="yo")
async def any_test_message(message: types.Message):
  await message.answer(message.text)
  await message.answer(message.md_text)
  await message.answer(message.html_text)

@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def echo_document(message: types.Message):
  await message.reply_animation(message.animation.file_id)

@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
  #Скачиваем в каталог с ботом созданием подкатологов по типу файла
  await message.document.download()

  @dp.message_handler(content_types=["photo"])
  async def download_photo(message: types.Message):
      await message.photo[-1].download(destination="/tmp/somedir/")
  #Дополняем текст 
  message.answer(
    f"<u>Ваш текст</u>:]\n\n{message.html_text}", parse_mode="HTML"
  )


@dp.message_handler(commands="test4")
async def with_hidden_link(message: types.Message):
    await message.answer(
      f"{fmt.hide_link('https://telegram.org/blog/video-calls/ru')}Кто бы мог подумать, что "
        f"в 2020 году в Telegram появятся видеозвонки!\n\nОбычные голосовые вызовы "
        f"возникли в Telegram лишь в 2017, заметно позже своих конкурентов. А спустя три года, "
        f"когда огромное количество людей на планете приучились работать из дома из-за эпидемии "
        f"коронавируса, команда Павла Дурова не растерялась и сделала качественные "
        f"видеозвонки на WebRTC!\n\nP.S. а ещё ходят слухи про демонстрацию своего экрана :)",
        parse_mode=types.ParseMode.HTML)
    

@dp.message_handler()
async def any_text_message2(message: types.Message):
  await message.answer(f"Привет, <b>{fmt.quote_html(message.text)}", parse_mode=types.ParseMode.HTML)

  # А можно и так 
  await message.answer(fmt.text("Привет" , fmt.hbold(message.text)), parse_mode=types.ParseMode.HTML)  


@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
  await message.answer_dice(emoji="🎲")  
  
@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
  await message.bot.send_dice(-100123456789, emoji="🎲")  
@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
  # Update: обхект события от Telegram. Exception: объект исключения
   # Здесь можно как то обработать блокировку например убрать юзера из бд
   print(f'Меня заблокал юзер! \nСообщение: {update}\nОшибка: {exception}')

   #Такой хэндлер всегда должен возвращать  True
   #если дальнейшая обработка не требуется
   return True
if __name__ == "__main__":
  #Запуск бота
  executor.start_polling(dp, skip_updates=True) 