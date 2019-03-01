import pygame
FPS=40
stripx=40
stripy=40
X0=stripx
Y0=0
WIDTH=800
width=WIDTH/8
HEIGTH=800
heigth=HEIGTH/8
Totalwidth=WIDTH+stripx
Totalheigth=HEIGTH+stripx
pygame.init()
screen=pygame.display.set_mode((Totalwidth,Totalheigth))
clock=pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 30, True)
alphabet='0abcdefghijklmn'

def translatecoord(coordinate):
	fileletter=coordinate[0]
	row=int(coordinate[1])
	if fileletter=='a':
		File=1
	if fileletter=='b':
		File=2
	if fileletter=='c':
		File=3
	if fileletter=='d':
		File=4
	if fileletter=='e':
		File=5
	if fileletter=='f':
		File=6
	if fileletter=='g':
		File=7
	if fileletter=='h':
		File=8
	
	return [File,row]
def invtranslatecoord(numcoord):
	File=alphabet[numcoord[0]]	
	return File+str(numcoord[1])





class makecoordinatesletter(pygame.sprite.Sprite):
	def __init__(self,i):
		pygame.sprite.Sprite.__init__(self)
		self.image=font.render(alphabet[i],1,(0,0,0))
		self.rect=self.image.get_rect()
		self.rect.center=(X0+(i-1)*width+width/2,HEIGTH+stripy/2)
class makecoordinatesnumber(pygame.sprite.Sprite):
	def __init__(self,i):
		pygame.sprite.Sprite.__init__(self)
		self.image=font.render(str(i),1,(0,0,0))
		self.rect=self.image.get_rect()
		self.rect.center=(X0/2,HEIGTH-(-.5+i)*heigth)



class square(pygame.sprite.Sprite):
	def __init__(self,coordinate):
		pygame.sprite.Sprite.__init__(self)
		self.coordinate=coordinate
		self.fileletter=coordinate[0]
		self.row=coordinate[1]
		self.numcoord=translatecoord(coordinate)
		self.Occupied=False
		self.image=pygame.Surface((width,heigth),1)
		#~ black=(139,0,0)
		black=(139,0,0)
		white=(245,222,179)
		if (self.numcoord[0]+self.numcoord[1])%2==0:
				self.color=black
		else:
			self.color=white
		self.image.fill(self.color)
		self.rect=self.image.get_rect()
		self.rect.bottomleft=(X0+(self.numcoord[0]-1)*width,HEIGTH-(self.numcoord[1]-1)*heigth)
		self.layer=0
		


	

class Piece(pygame.sprite.Sprite):
	def __init__(self,color,coordinate,name):
		pygame.sprite.Sprite.__init__(self)
		self.color=color
		self.coordinate=coordinate
		self.numcoord=translatecoord(coordinate)
		self.name=name
		self.movelist=[]
	def isonboard(self,numcoord):
		if numcoord[0]>0 and numcoord[0]<9 and numcoord[1]>0 and numcoord[1]<9:
			return True
		else:
			return False
	
	def displaypiecesetting(self):
		print(self.name)
		print(self.color)
		print(self.coordinate)
		print("*------~~~~~-------*")
	
	def checkmove(self,candidatecoordself,allpieces):
		if self.isonboard(candidatecoordself)==False:
			return 'Nomove'
		else:
			for p in allpieces:
				#~ p.displaypiecesetting()
				if p.name!=self.name:
					if p.color==self.color:
						if p.numcoord==candidatecoordself:
							return 'Nomove'
					elif p.color!=self.color:
						if p.numcoord==candidatecoordself:
							return 'x'+invtranslatecoord(candidatecoordself)
			return invtranslatecoord(candidatecoordself)
						
						
					
		
class Knight(Piece):
	def __init__(self,color,coordinate,name):
		Piece.__init__(self,color,coordinate,name)
		if self.color=='black':
			self.image=pygame.image.load('./chess_piece_2_black_knight.png').convert()
		else:
			self.image=pygame.image.load('./chess_piece_2_white_knight.png').convert()
		self.rect=self.image.get_rect()
		xi=(self.numcoord[0]-1)*width+width/2+X0
		yi=HEIGTH-(self.numcoord[1])*heigth+heigth/2+Y0

		self.rect.center=(xi,yi)
		self.layer=1
	def Movelist(self,allpieces):
		self.movelist=[]
		poscoord=[0,0]
		curcoord=self.numcoord
		for l in [-2,2]:
			for u in [-1,1]:
				poscoord[0]=curcoord[0]+l
				poscoord[1]=curcoord[1]+u
				move=self.checkmove(poscoord,allpieces)
				if move!='Nomove':
					self.movelist.append(move)		
		for l in [-1,1]:
			for u in [-2,2]:
				poscoord[0]=curcoord[0]+l
				poscoord[1]=curcoord[1]+u
				move=self.checkmove(poscoord,allpieces)
				if move!='Nomove':
					self.movelist.append(move)

class Bishop(Piece):
	def __init__(self,color,coordinate,name):
		Piece.__init__(self,color,coordinate,name)		
		if self.color=='black':
			self.image=pygame.image.load('./chess_piece_2_black_bishop.png').convert()
		else:
			self.image=pygame.image.load('./chess_piece_2_white_bishop.png').convert()
		self.rect=self.image.get_rect()
		xi=(self.numcoord[0]-1)*width+width/2+X0
		yi=HEIGTH-(self.numcoord[1])*heigth+heigth/2+Y0

		self.rect.center=(xi,yi)
		self.layer=1
	def Movelist(self,allpieces):
		self.movelist=[]
		poscoord=[0,0]
		curcoord=self.numcoord
		
		#bishops move in 4 directions they all need to be checked for pieces
		for i in range(1,8):	
			poscoord[0]=curcoord[0]+i
			poscoord[1]=curcoord[1]+i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
			else: #next one will also be not on board
				break
		for i in range(1,8):	
			poscoord[0]=curcoord[0]-i
			poscoord[1]=curcoord[1]-i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
			else: #next one will also be not on board
				break
		for i in range(1,8):	
			poscoord[0]=curcoord[0]+i
			poscoord[1]=curcoord[1]-i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
			else: #next one will also be not on board
				break
		for i in range(1,8):	
			poscoord[0]=curcoord[0]-i
			poscoord[1]=curcoord[1]+i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
			else: #next one will also be not on board
				break

class Rook(Piece):
	def __init__(self,color,coordinate,name):
		Piece.__init__(self,color,coordinate,name)
		if self.color=='black':
			self.image=pygame.image.load('./chess_piece_2_black_rook.png').convert()
		else:
			self.image=pygame.image.load('./chess_piece_2_white_rook.png').convert()
		self.rect=self.image.get_rect()
		xi=(self.numcoord[0]-1)*width+width/2+X0
		yi=HEIGTH-(self.numcoord[1])*heigth+heigth/2+Y0

		self.rect.center=(xi,yi)
		self.layer=1

	def Movelist(self,allpieces):
		self.movelist=[]
		poscoord=[0,0]
		curcoord=self.numcoord
		for i in range(1,8):
			poscoord[0]=curcoord[0]+i
			poscoord[1]=curcoord[1]
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
		for i in range(1,8):
			poscoord[0]=curcoord[0]-i
			poscoord[1]=curcoord[1]
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
		for i in range(1,8):
			poscoord[0]=curcoord[0]
			poscoord[1]=curcoord[1]+i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
		for i in range(1,8):
			poscoord[0]=curcoord[0]
			poscoord[1]=curcoord[1]-i
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)
				if move[0]=='x':
					break
class Pawn(Piece):
	def __init__(self,color,coordinate,name):
		Piece.__init__(self,color,coordinate,name)
		self.hasmoved=False
		if self.color=='black':
			self.image=pygame.image.load('./chess_piece_2_black_pawn.png').convert()
		else:
			self.image=pygame.image.load('./chess_piece_2_white_pawn.png').convert()
		self.rect=self.image.get_rect()
		xi=(self.numcoord[0]-1)*width+width/2+X0
		yi=HEIGTH-(self.numcoord[1])*heigth+heigth/2+Y0

		self.rect.center=(xi,yi)
		self.layer=1
		
	def checkmovelist(self,pieces):
		#need adapted movelist for pawns
		return
		
	def Movelist(self,allpieces):
		self.movelist=[]
		curcoord=self.numcoord
		poscoord=[0,0]
		if self.color=='white':
			direc=+1
		if self.color=='black':
			direc=-1
		poscoord[0]=curcoord[0]
		poscoord[1]=curcoord[1]+1*direc
		move=self.checkmove(poscoord,allpieces)
		if move!='Nomove':
			self.movelist.append(move)
		if self.hasmoved==False:
			poscoord[0]=curcoord[0]
			poscoord[1]=curcoord[1]+2*direc
			move=self.checkmove(poscoord,allpieces)
			if move!='Nomove':
				self.movelist.append(move)

all_sprites=pygame.sprite.Group()
board_sprites=pygame.sprite.Group()
white_sprites=pygame.sprite.Group()
black_sprites=pygame.sprite.Group()
letter_sprites_perimiter=pygame.sprite.Group()

for i in range(1,9):
	L=makecoordinatesletter(i)
	N=makecoordinatesnumber(i)
	#~ N=makecoordinates()
	letter_sprites_perimiter.add(L)
	letter_sprites_perimiter.add(N)
	#~ letter_sprites_perimiter.add(N.number(i))



board=[]		
for i in range(0,8):
	row=[]
	for j in range(0,8):
		row.append(square(invtranslatecoord((i+1,j+1))))
		board_sprites.add(square(invtranslatecoord((i+1,j+1))))
	board.append(row)


#Pawns
Wpa=Pawn('white','a2','wpa')
Wpb=Pawn('white','b2','wpb')
Wpc=Pawn('white','c2','wpc')
Wpd=Pawn('white','d2','wpd')
Wpe=Pawn('white','e2','wpe')
Wpf=Pawn('white','f2','wpf')
Wpg=Pawn('white','g2','wpg')
Wph=Pawn('white','h2','wph')
#Knights
Wnb=Knight('white','b1','wnb')
Wng=Knight('white','g1','wng')
#Bishops
Wbc=Bishop('white','c1','wbc')
Wbf=Bishop('white','f1','wbf')
#Rooks
Wra=Rook('white','a1','wra')
Wrh=Rook('white','h1','wrh')

white_sprites.add(Wpa)
white_sprites.add(Wpb)
white_sprites.add(Wpc)
white_sprites.add(Wpd)
white_sprites.add(Wpe)
white_sprites.add(Wpf)
white_sprites.add(Wpg)
white_sprites.add(Wph)
white_sprites.add(Wnb)
white_sprites.add(Wng)
white_sprites.add(Wbc)
white_sprites.add(Wbf)
white_sprites.add(Wra)
white_sprites.add(Wrh)

Bpa=Pawn('black','a7','bpa')
Bpb=Pawn('black','b7','bpb')
Bpc=Pawn('black','c7','bpc')
Bpd=Pawn('black','d7','bpd')
Bpe=Pawn('black','e7','bpe')
Bpf=Pawn('black','f7','bpf')
Bpg=Pawn('black','g7','bpg')
Bph=Pawn('black','h7','bph')
#Knights
Bnb=Knight('black','b8','bnb')
Bng=Knight('black','g8','bng')
#Bishops
Bbc=Bishop('black','c8','bbc')
Bbf=Bishop('black','f8','bbf')
#Rooks
Bra=Rook('black','a8','bra')
Brh=Rook('black','h8','brh')

black_sprites.add(Bpa)
black_sprites.add(Bpb)
black_sprites.add(Bpc)
black_sprites.add(Bpd)
black_sprites.add(Bpe)
black_sprites.add(Bpf)
black_sprites.add(Bpg)
black_sprites.add(Bph)
black_sprites.add(Bnb)
black_sprites.add(Bng)
black_sprites.add(Bbc)
black_sprites.add(Bbf)
black_sprites.add(Bra)
black_sprites.add(Brh)


run=True	
while run:
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			run=False
	
	
	#~ #update
	screen.fill((255,255,255))
	
	

	white_sprites.update()
	black_sprites.update()
	
	board_sprites.draw(screen)

	white_sprites.draw(screen)
	black_sprites.draw(screen)
	letter_sprites_perimiter.draw(screen)
	pygame.display.flip()
	
	

	clock.tick(FPS)
