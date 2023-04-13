import asyncio
import logging

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram import types, Dispatcher
from shop.photos import photos
from shop.videos import videos
import shop.keyboards.works as keyboards
from create import bot
async def our_works_begin(callback: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	if data.get('delete_msg', None) is not None:
		try:
			await bot.delete_message(callback.message.chat.id, data.get('delete_msg'))
		except Exception as e:
			logging.error(e)
	await callback.message.delete()


	await callback.message.answer(text="⚡️Выберите интересующий вас проект",
										reply_markup=keyboards.works_keyboard)
	await state.reset_data()
	await callback.answer()

async def our_works_begin_msg(message: types.Message, state: FSMContext):
	await message.answer(text="⚡️Выберите интересующий вас проект",
								  reply_markup=keyboards.works_keyboard)
	await state.reset_data()

async def our_works_1(callback: types.CallbackQuery, state: FSMContext):

	media_group = types.MediaGroup()
	for i in photos['works1']:
		media_group.attach_photo(photo=i)
	await callback.message.delete()

	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="1. Бассейн 25 м\nБассейны шириной 25 метров являются юношескими олимпийскими бассейнами и обычно используются в соревнованиях по плаванию. Эти бассейны также используются на чемпионатах мира, проводимых FINA, руководящим органом международных соревнований по плаванию. На соревнованиях по плаванию эти бассейны часто называют бассейнами с коротким ходом.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page = "Наши работы: 1. Бассейн 25 м")
	await callback.answer()

async def our_works_2(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works2']:
		media_group.attach_photo(photo=i)
	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="2. Композитный бассейн\nБассейн из композита представляет собой емкость для плавания, которая изготовлена на основе пластика с добавлением к нему иных компонентов. Отличительной чертой данной конструкции считается возможность ее использования не только по сезону, но и как круглогодичное сооружение благодаря возможности накрывания.Композитное соединение – это одна из разновидностей полимерных изделий, которые усилены прочными синтетическими волокнами.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 2. Композитный бассейн")
	await callback.answer()

async def our_works_3(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works3']:
		media_group.attach_photo(photo=i)
	res = await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="3. Мозаичный бассейн\nПод мозаичным бассейном подразумевается бетонная чаша, отделанная мозаичной плиткой. Преимущество и отличие мозаики от форматной плитки в том, что она позволяет гибко отделать поверхность любой формы, а технология обеспечивает высокую водонепроницаемость.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 3. Мозаичный бассейн")
	await callback.answer()

async def our_works_4(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works4']:
		media_group.attach_photo(photo=i)
	res = await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="4. Пленочный бассейн\nПВХ мембрана (пленка ПВХ) представляет собой плотный материал из пластифицированного поливинилхлорида с армированием полиэстерной сеткой. ПВХ мембрана разработана специально для отделки дна и бортов плавательного бассейна. Основным преимуществом ПВХ мембраны для бассейнов является быстрота проведения отделочных работ, отсутствие мусора во время проведения работ, а так же то, что ПВХ мембрана является не только отделочным материалом бассейна, ни и его гидроизоляцией, что значительно удешевляет процесс строительства бассейна. Благодаря богатому выбору цветов и орнаментов ПВХ мембраны для бассейна и возможность отделки бассейна практически любой формы и размеров делают ее наиболее распространенным вариантом отделки чаши бассейна в мире.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 4. Пленочный бассейн")
	await callback.answer()

async def our_works_5(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works5']:
		media_group.attach_photo(photo=i)
	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="5. Переливной бассейн\nПереливной бассейн – это бассейн в котором забор воды на фильтрацию осуществляется с помощью перелива через борт. Возврат отфильтрованной воды осуществляется донными форсунками. Благодаря этой системе достигается максимальное качество фильтрации воды. Переливная система придает шарм бассейну, за счет наполнения чаши бассейна до краев.Строительство такого бассейна – достаточно сложная процедура, которая требует инженерных расчетов для подбора оборудования.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 5. Переливной бассейн")
	await callback.answer()

async def our_works_6(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works6']:
		media_group.attach_photo(photo=i)
	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="6. Скиммерный бассейн\nСкиммерный бассейн – это тип бассейна, в котором вода с поверхности бассейна уходит в фильтровальную установку через скиммер. Скиммер – устройство, с помощью которого забирается верхний слой воды бассейна (более загрязненный). В скиммерном бассейне уровень воды находится на горизонтальной оси скиммера, то есть от поверхности воды до верхней кромки бассейна свободное пространство, около 10-20 см. Стационарные железобетонные бассейны оборудуют не только скиммером, но и донным выпуском.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 6. Скиммерный бассейн")
	await callback.answer()

async def our_works_7(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works7']:
		media_group.attach_photo(photo=i)
	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="7. Строительные процессы", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 1. Бассейн 25 м")
	await callback.answer()

async def our_works_8(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()

	for i in videos['works8']:
		media_group.attach_video(video=i)
	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="Описание ", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 8. Видео")
	await callback.answer()

async def our_works_9(callback: types.CallbackQuery, state: FSMContext):
	media_group = types.MediaGroup()
	for i in photos['works9']:
		media_group.attach_photo(photo=i)

	for i in videos['works9']:
		media_group.attach_video(video=i)

	await callback.message.answer_media_group(media=media_group)
	await callback.message.answer(text="9. Расположение и размеры технологического отсека\nОно обычно расположено рядом с бассейном. За короткой стороной чаши бассейна на такой же глубине как глубина самого бассейна. При этом доступ в технический отсек обеспечивает люк, сделанный на поверхности и оборудование устанавливается ниже зеркала воды бассейна. Размер тех.помещения зависит от количества оборудования, которое будет установлено в бассейне.Если это будет фильтровальная установка, несколько насосов для аттракционов (противоток, водопад и др),УФ установка, оборудование для нагрева воды, то размер помещения должен быть примерно 1.5м(ширина)*2-2.5м(длина)Если оборудования будет меньше, то размер можно сделать тоже немного меньше(шириной 1.2-1.3м)При отсутствии первой возможности, оборудование располагают где-то рядом с бассейном в отдельной комнате(кладовке),в котельной или в другом месте.При этом оборудование будет располагаться выше уровня зеркала воды бассейна.\n\nТребования к технологическому отсеку Необходимо знать, что в техническое помещение, где будет смонтировано оборудование для бассейна нужно провести следующие коммуникации:\n\n- Питающий электрический кабель подобранный по сечению, исходя из общей мощности оборудования которое оно будет питать.\n- Подающая и обратная труба горячего водоснабжения(ГВС),если обогрев воды будет осуществляться с помощью теплообменника. Использование теплообменника уменьшает эксплуатационные расходы по сравнению с использованием электронагревателя для подогрева воды в бассейне.\n- Нужно провести холодную воду(ХВС) для подпитки и заполнения бассейна водой- Нужно подвести канализационную трубу небольшого диаметра(40-50мм) для слива воды при промывке песка. Эту простую 3-х минутную -операцию нужно проводить один раз в 10-14 дней при которой сливается 150-200л воды. При правильном уходе за водой в бассейне полный слив воды из него производится редко(один раз в год ). Поэтому другой вариант слива воды это присоединение обычного садового шланга с помощью которого можно слить большой объем воды из бассейна в доступное для этого место.- Вот такие главные требования к построению технического помещения в котором располагается оборудование для бассейна. Готовы ответить на все ваши вопросы, которые у вас появляются при проектировании технологического отсека для бассейнного оборудования.", reply_markup=keyboards.define_work_keyboard)
	await state.update_data(order_from_page="Наши работы: 9")
	await callback.answer()














def register_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(our_works_begin, state='*', text='shop_our_works')
	dp.register_callback_query_handler(our_works_1, state='*', text='shop_works_1')
	dp.register_callback_query_handler(our_works_2, state='*', text='shop_works_2')
	dp.register_callback_query_handler(our_works_3, state='*', text='shop_works_3')
	dp.register_callback_query_handler(our_works_4, state='*', text='shop_works_4')
	dp.register_callback_query_handler(our_works_5, state='*', text='shop_works_5')
	dp.register_callback_query_handler(our_works_6, state='*', text='shop_works_6')
	dp.register_callback_query_handler(our_works_7, state='*', text='shop_works_7')
	dp.register_callback_query_handler(our_works_8, state='*', text='shop_works_8')
	dp.register_callback_query_handler(our_works_9, state='*', text='shop_works_9')




