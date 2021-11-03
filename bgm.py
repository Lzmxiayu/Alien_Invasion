import pygame

class BackGroundMusic:
	def __init__(self,ai_game):
		pygame.init()
		#初始化mixer
		pygame.mixer.init()

		self.settings=ai_game.settings

		self.music_library=[
		"./music/久石让 (ひさいし じょう) - The Wind Forest (风中森林).mp3",
		"./music/Jean-Jacques Milteau - Sweet 70's.mp3",
		"./music/Jean-Jacques Milteau - Le Wolf.mp3",
		]

		self.music_number = 0
		

	def _play_music(self,music_number):
		
		self.music_number = self.settings.music_number%len(self.music_library)

		pygame.mixer.music.load(self.music_library[self.music_number])
		pygame.mixer.music.play()	

		self.settings.music_number += 1
		