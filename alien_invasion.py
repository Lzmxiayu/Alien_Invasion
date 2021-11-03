import sys
import pygame
from random import randint
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from bgm import BackGroundMusic

class AlienInvasion:
	"""管理游戏资源和行为的类"""
	def __init__(self):
		"""初始化游戏并创建游戏资源"""
		pygame.init()
		#初始化设置
		self.settings=Settings()
		
		#初始化窗口
		self.screen=pygame.display.set_mode(
			(self.settings.screen_width,self.settings.screen_height))
		pygame.display.set_caption("Alien Invasion")

		#创建一个用于存储游戏统计信息的实例
		#并创建记分牌
		self.stats = GameStats(self)
		self.sb=Scoreboard(self)

		#设置背景色
		self.bg_color=(230,230,230)

		#加载背景图像并设置其rect属性。
		self.image=pygame.image.load('images/space.jpg')
		self.image=pygame.transform.scale(self.image,(self.settings.screen_width,self.settings.screen_height))
		self.rect=self.image.get_rect() 

		#初始化飞船
		self.ship=Ship(self)

		#初始化子弹
		self.bullets = pygame.sprite.Group()

		#初始化外星人
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		self._set_buttons()
		self.bgm=BackGroundMusic(self)

		#self.simple_button.rect.y=self.simple_button.rect.y-30#-2.0*self.simple_button.rect.height
	def _set_buttons(self):
		#创建Play按钮
		self.medium_button = Button(self,"Medium",[(self.settings.screen_width-200)/2,
						(self.settings.screen_height-50)/2])
		self.simple_button = Button(self,"Simple",[(self.settings.screen_width-200)/2,
						(self.settings.screen_height-50)/2-100])
		self.difficult_button = Button(self,"Difficult",[(self.settings.screen_width-200)/2,
						(self.settings.screen_height-50)/2+100])


	def run_game(self):
		"""开始游戏的主循环"""
		while True:
			self._check_events()	
			
			if self.stats.game_active:
				self.ship.update()		
				self._update_bullet()
				self._update_aliens()
		
			self._update_screen()

	def _check_play_button(self,mouse_pos):
		"""在玩家单机Play按钮且游戏处于非活跃状态时开始游戏"""
		button_clickedsp = self.simple_button.rect.collidepoint(mouse_pos)
		button_clickedmd = self.medium_button.rect.collidepoint(mouse_pos)
		button_clickeddt = self.difficult_button.rect.collidepoint(mouse_pos)
		start = button_clickedsp or button_clickedmd or button_clickeddt

		if not self.stats.game_active:
			if button_clickedsp:
				#简单难度游戏设置
				self.settings.initialize_dynamic_settings2(0.5)
			elif button_clickedmd:
				#中等难度游戏设置
				self.settings.initialize_dynamic_settings2(1.0)
			elif button_clickeddt:
				#困难难度游戏设置
				self.settings.initialize_dynamic_settings2(1.5)
		if start:
			self._start_game()
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

	def _start_game(self):
		#重置游戏统计信息

		self.stats.game_active = True

		#清空余下的外星人和子弹
		self.aliens.empty()
		self.bullets.empty()

		#创建一群新的外星人并让飞船居中
		self._create_fleet()
		self.ship.center_ship()

		#隐藏鼠标光标
		pygame.mouse.set_visible(False)



	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				with open('Highest score.txt','w') as f:
					f.write(f"{self.stats.high_score}")
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_keydown_events(self,event):
		"""响应按下按键"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right=True
		elif event.key == pygame.K_LEFT:
		    self.ship.moving_left=True	
		elif event.key == pygame.K_q:
			with open('Highest score.txt','w') as f:
				f.write(f"{self.stats.high_score}")
			sys.exit()
		elif event.key == pygame.K_m: 
			self.bgm._play_music(self.settings.music_number)
		elif event.key == pygame.K_SPACE and self.stats.game_active:
			self._fire_bullet()
		elif event.key == pygame.K_p and not self.stats.game_active:
			self.settings.initialize_dynamic_settings2(1.0)
			self._start_game()

	def _check_keyup_events(self,event):
		"""响应松开按键"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right=False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left=False	

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed :
			#pygame.mixer.music.load("./Jean-Jacques Milteau - Le Wolf.mp3")
			#pygame.mixer.music.play()			
			new_bullet=Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullet(self):
		"""更新子弹位置并删除消失的子弹"""
		#更新子弹位置
		self.bullets.update()

		#删除消失的子弹
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <=0:
				self.bullets.remove(bullet)
		#检测子弹击中外星人时
		self._check_bullet_alien_collisions()
		#print(len(self.bullets)) #打印数值会极大降低运行速度

	def _check_bullet_alien_collisions(self):
		"""响应子弹和外星人发生碰撞"""
		#删除相应的子弹和外星人
		collisions = pygame.sprite.groupcollide(
					self.bullets,self.aliens,True,True)
		if collisions:
			#pygame.mixer.music.load("./Jean-Jacques Milteau - Sweet 70's.mp3")
			#pygame.mixer.music.play()		
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			self.start_new_level()

	def start_new_level(self):
		#删除现有的子弹并新建一群外星人
		self.bullets.empty()
		self._create_fleet()
		self.settings.increase_speed()
		#提高登记
		self.stats.level += 1
		self.sb.prep_level()

	def _create_fleet(self):
		"""创建外星人群"""
		#创建一个外星人。
		alien=Alien(self)
		alien_width,alien_height  = alien.rect.size
		#计算一行多少外星人
		available_space_x = self.settings.screen_width - (2* alien_width)
		number_aliens_x = available_space_x // ( 2 * alien_width )
		#计算屏幕可容纳多少行外星人
		ship_height=self.ship.rect.height
		available_space_y = self.settings.screen_height - (3* alien_height)-ship_height
		number_rows = available_space_y // ( 2 * alien_height )

		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		"""创建一个外星人,并将其放再放在当前行"""
		alien=Alien(self)
		alien_width,alien_height  = alien.rect.size	
		alien.x=alien_width + 2 * alien_number * alien_width
		alien.rect.x=alien.x
		alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
		self.aliens.add(alien)
		
	def _check_fleet_edges(self):
		"""有外星人到达边缘时采取相应的措施"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""将整群外星人下移，并改变它们的方向。"""
		for alien in self.aliens.sprites():
			alien.rect.y += randint(0,self.settings.fleet_drop_speed)
		self.settings.fleet_direction *= -1

	def _update_aliens(self):
		"""检测是否有外星人在屏幕边缘，
		   并更新整群外星人的位置。
		"""
		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			self._ship_hit()

		self._check_aliens_bottom()

	def _ship_hit(self):
		if self.stats.ships_left > 0:
			self.stats.ships_left -= 1
			self.sb.prep_ships()
			self._start_game()
			sleep(0.5)
		else:
			self.stats.game_active = False
			self.stats.reset_stats()
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#像飞船被撞到一样处理
				self._ship_hit()
				break

	def _update_screen(self):
		#每次循环时都重绘屏幕
		self.screen.fill(self.settings.bg_color)	#全局刷新
		self.screen.blit(self.image,self.rect)
		self.ship.blitme()
		#绘制所有还存在的子弹
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		#绘制外星人
		self.aliens.draw(self.screen)
		
		#显示得分
		self.sb.show_score()

		#如果游戏处于非活动状态，就绘制Play按钮
		if not self.stats.game_active:
			self.simple_button.draw_button()
			self.medium_button.draw_button()
			self.difficult_button.draw_button()
			

		# 让最近绘制的屏幕可见
		pygame.display.flip()


if __name__ == '__main__':
	#创建游戏实例并运行游戏。
	ai=AlienInvasion()
	ai.run_game()