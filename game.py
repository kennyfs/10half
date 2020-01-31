import random
class card:
	def __init__(self):
		self.left=[4]*11#half+1~10
		self.left[0]=12
	def getone(self):
		if sum(self.left)==0:return False
		a=random.randint(1,sum(self.left))
		for i in range(11):
			if a<=self.left[i]:
				self.left[i]-=1
				if i==0:return 0.5
				return i
			else:a-=self.left[i]
class holder:
	def __init__(self,money,players):
		self.card=card()
		self.money=money
		self.players=players
		self.cards=[]
	def newgame(self):
		self.cards=[]
	def give_init_card(self):
		self.card.__init__()
		for player in self.players:
			player.cards.append(self.card.getone())
		self.cards.append(self.card.getone())
	def askplayers(self):
		anyplayernotend=True
		for player in self.players:
			print(self.card.left)
			if player.end:anyplayernotend=False;continue
			try:self.money+=player.DecideToAddCard(self.card.getone)
			except:player.end=True
		return anyplayernotend
	def decide(self):
		while 1:
			while 1:
				end=True
				for player in self.players:
					if player.living:end=False
				if end:return
				print('(holder)',end='')
				for i in range(len(self.players)):
					if self.players[i].living:
						print('player',self.players[i].num,'\'s open cards\' sum is:',sum(self.players[i].cards[1:]))
				print('You have ',len(self.cards),'cards.Your cards\' sum is ',sum(self.cards),'\nWhich player to \"scratch\"(id)?Type any WORD to exit')
				try:i=int(input())
				except:break
				if not self.players[i].living:print('He already died');continue
				player_sum=sum(self.players[i].cards)
				holder_sum=sum(self.cards)
				print('player',player_sum,'you',holder_sum)
				self.players[i].ended()
				if player_sum>holder_sum:
					print('failed')
					self.money-=self.players[i].moneytoplay
					self.players[i].money+=self.players[i].moneytoplay
				elif player_sum==holder_sum:
					print('Nothing happended.')
				elif player_sum<holder_sum:
					print('success!')
					self.money+=self.players[i].moneytoplay
					self.players[i].money-=self.players[i].moneytoplay
			print('You finished \"scratch\" players.Now add a card.')
			self.cards.append(self.card.getone())#self.card is the whole cards(card object)
			if sum(self.cards)>10.5:
				print('Your cards:',self.cards)
				print('boom!You lose ',end='')
				lose=0
				for player in self.players:
					if not player.living:continue
					lose+=player.moneytoplay
					player.money+=player.moneytoplay
				print(str(lose)+' dollars')
				self.money-=lose
				return
			if len(self.cards)==6:
				print('Wow!You \"Pass 5\"!\nYou win ',end='')
				win=0
				for player in self.players:
					if not player.living:continue
					win+=player.moneytoplay
					player.money-=player.moneytoplay
				print(str(win)+' dollars')
				self.money+=win
				return
			if sum(self.cards)==10.5:
				print('Wow!You reached 10.5!\nYou win ',end='')
				win=0
				for player in self.players:
					if not player.living:continue
					win+=player.moneytoplay
					player.money-=player.moneytoplay
				print(str(win)+' dollars')
				self.money+=win
				return
	def set_moneytoplay(self):
		for player in self.players:
			player.set_moneytoplay()
class player:
	def __init__(self,money,num):
		self.num=num
		self.money=money
		self.moneytoplay=10
		self.cards=[]
		self.living=True
		self.end=False
	def newgame(self):
		self.cards=[]
		self.living=True
		self.end=False
	def DecideToAddCard(self,card):
		while 1:
			print('(player '+str(self.num)+')Your now cards are',self.cards,'sum=',sum(self.cards),'\n1(yes) or 0(no)?')
			if int(input()):
				self.cards.append(card())
				if sum(self.cards)>10.5:
					print('boom!You lose!')
					self.ended()
					self.money-=self.moneytoplay
					return self.moneytoplay
				if len(self.cards)==6:
					print('Wow!You \"Pass 5\"!')
					self.money+=self.moneytoplay*2
					self.ended()
					return -player.moneytoplay*2
				if sum(self.cards)==10.5:
					if len(self.cards)==2:
						print('Wow!You reached 10.5 within 2 cards!')
						self.money+=self.moneytoplay*2
						self.ended()
						return -self.moneytoplay*2
					else:
						print('You reached 10.5!')
						self.money+=self.moneytoplay
						self.ended()
						return -self.moneytoplay
			else:
				self.end=True
				return 'No'
		return 0
	def ended(self):
		self.living=False
		self.end=True
	def set_moneytoplay(self):
		while 1:
			print('player(',self.num,')How much do you want to gamble?')
			a=int(input())
			if a<=self.money:
				break
			print('You don\'t have such money.')
		self.moneytoplay=a
def progress():
	players=[]
	for i in range(2):
		players.append(player(100,i))
	hold=holder(100,players)
	while 1:
		hold.set_moneytoplay()
		print('holder\'s money=',hold.money)
		for p in hold.players:
			print(p.num,p.money)
		hold.give_init_card()
		while hold.askplayers():
			pass
		hold.decide()
		for play in players:
			play.newgame()
		hold.newgame()
progress()
