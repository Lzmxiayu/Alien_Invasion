class Settings:
	"""存储游戏《外星人入侵》中所有设置的类"""

	def __init__(self):
		"""初始化游戏的设置。"""
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0,0,0)#(230,230,230)

		#bgm顺序
		self.music_number=0

		#飞船设置
		self.ship_speed = 1.5
		self.ship_limit = 2

		#子弹设置
		self.bullet_speed = 2.0
		self.bullet_width = 5
		self.bullet_height = 15
		self.bullet_color =(255,255,255)#(60,60,60)
		self.bullets_allowed=3

		#外星人
		self.alien_speed = 5
		self.fleet_drop_speed = 10
		#fleet_direction为1代表向右移，为-1表示向左移
		self.fleet_direction =-1

		#加快游戏节奏的速度
		self.speedup_scale = 1.1
		self.score_scale = 1.5

		self.initialize_dynamic_settings()


	def initialize_dynamic_settings(self):
		self.ship_speed = 2.0
		self.bullet_speed = 4.0
		self.alien_speed = 1.5

		#fleet_direction为1代表向右移，为-1表示向左移
		self.fleet_direction =-1

		#记分
		self.alien_points = 50

	def initialize_dynamic_settings2(self,level):
		self.initialize_dynamic_settings()
		self.alien_speed *=level

		#fleet_direction为1代表向右移，为-1表示向左移
		self.fleet_direction =-1
		#记分
		self.alien_points = 50

	def increase_speed(self):
		"""提高速度设置"""
		self.ship_speed *=self.speedup_scale
		self.bullet_speed *=self.speedup_scale
		self.alien_speed *=self.speedup_scale
		
		self.alien_points = int(self.alien_points * self.score_scale)
		#print(self.alien_points)