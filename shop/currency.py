import logging

import aiohttp
import http3
import xml.etree.ElementTree as ET

import create
async def get_price_in_rub(currency, sum):
	if currency == 'RUB':
		return int(sum)
	if currency == 'EUR':
		return int(sum*create.eur_price)


async def get_currency_price():
	text = ''
	async with aiohttp.ClientSession() as session:
		async with session.get('https://cbr.ru/scripts/XML_daily.asp') as resp:
			try:
				text = await resp.text()
			except Exception as e:
				logging.error(e)
				return
	if text == '':
		return
	try:
		tree = ET.fromstring(text)
	except Exception as e:
		logging.error(e)
		return
	for valute in tree.findall('Valute'):
		try:
			char_code = valute.find('CharCode').text
			if char_code == 'EUR':
				value = valute.find('Value').text
				try:
					value = value.replace(',', '.')
					create.eur_price = float(value)
				except Exception as e:
					logging.error(e)
		except Exception as e:
			logging.error(e)
			continue


