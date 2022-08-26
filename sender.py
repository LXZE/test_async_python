import asyncio

async def main():
	_, writer = await asyncio.open_connection('127.0.0.1', 8888)
	try:
		while True:
			input_msg = input('input: ')
			writer.write(input_msg.encode())
			await writer.drain()
	except KeyboardInterrupt:
		writer.write('end'.encode())
		await writer.drain()
		writer.close()

if __name__ == '__main__':
	asyncio.run(main())
