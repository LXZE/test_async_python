import asyncio
from random import randint

class RobotNode():
	def __init__(self) -> None:
		self.loop = True
		self.current_state = 0
		self.current_value = ''

	def stop(self):
		self.loop = False

	async def update(self):
		while self.loop:
			self.current_state = randint(0, 9)
			await asyncio.sleep(0.1)

	async def print_status(self):
		while self.loop:
			print(f'robot_state {self.current_state}')
			print(f'robot_value {self.current_value}')
			await asyncio.sleep(1)

class User():
	def __init__(self, robot: RobotNode) -> None:
		self.robot = robot
		self.server = None

	async def init_socket(self):
		self.server = await asyncio.start_server(self.handle_msg, '127.0.0.1', 8888)
		async with self.server: await self.server.serve_forever()

	async def handle_msg(self, reader, writer):
		while True:
			data = await reader.read(1024)
			message = data.decode()
			if message == 'end':
				self.robot.stop()
				self.server.close()
				break
				# raise KeyboardInterrupt

			# addr = writer.get_extra_info('peername')
			# print(f"Received {message!r} from {addr!r}")

			print(f'set robot value to {message}')
			self.robot.current_value = message
			print('check robot status')
			print('-'*20)
			print(f'get current_state: {self.robot.current_state}')
			print('-'*20)

async def main():
	# rclpy.init(args=args)
	# tb3ControllerNode = Turtlebot3Controller()
	# print('tb3ControllerNode created')

	robot = RobotNode()
	user = User(robot)
	task_list = (
		robot.update,
		robot.print_status,
		user.init_socket
	)
	tasks = [asyncio.ensure_future(task()) for task in task_list]
	try:
		# tasks = [asyncio.create_task(task()) for task in task_list]
		# loop.run_forever()
		await asyncio.wait(tasks)

		#Spin the node in the same thread if only callbacks are used
		# rclpy.spin(tb3ControllerNode)
		# print("Got CancelledError")
	except KeyboardInterrupt:
		print('Got interrupt signal')
		for task in tasks:
			task.cancel()

	# tb3ControllerNode.publishVelocityCommand(0.0,0.0)
	# tb3ControllerNode.destroy_node()
	# robotStop()
	# rclpy.shutdown()

if __name__ == '__main__':
	asyncio.run(main())
