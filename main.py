import pygame
from pygame.locals import *
import os
import random
# tạo không gian làm việc mới
pygame.init()

W, H = 900, 450
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Tetris the Jumpping')

# stimg=pygame.image.load(os.path.join('images', 'bg - Copy.png')).convert()
bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

class player(object):

    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]#load img cho obj
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]#load img cho obj
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]#load img cho obj
    fall = pygame.image.load(os.path.join('images', '0.png'))
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]#chuyển động khi nhảy

    def __init__(self, x, y, width, height):
        self.x = x  #tọa độ xuất hiện của obj
        self.y = y#tọa độ xuất hiện của obj
        self.width = width #chiều rộng của obj
        self.height = height #chiều cao của obj
        #khỏi tạo hàn ban đầu
        self.jumping = False #jump :nhảy
        self.sliding = False  #slide:trượt
        self.falling = False  #ngã
        self.slideCount = 0  
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
#làm hiệu ưng  hành động
    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 40))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.5
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x, self.y+3, self.width-8, self.height-35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.runCount = 0
                self.slideUp = False
                self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
            win.blit(self.slide[self.slideCount//10], (self.x, self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//6], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-13)

        # pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.png')), pygame.image.load(os.path.join('images', 'SAW1.png')), pygame.image.load(os.path.join('images', 'SAW2.png')), pygame.image.load(os.path.join('images', 'SAW3.png'))]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 15, self.width - 20, self.height - 5) #xác định hitbox cho obj
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:  #hỗ trợ cho phép tạo hiệu ứng cho cưa
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y)) #co hình ảnh về định dạng 64 bit trứớc khi vẽ
        self.rotateCount += 1
        # pygame.draw.rect(win, (255,0,0),self.hitbox, 2)

     #tương tác  hitbox 
    def collide(self, rect):
        #kiểm tra vị trí hitbox theo X
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:#vị trí (x) + chiều rộng
            #kiểm tra vị trí hitbox theo y
            if rect[1] + rect[3] > self.hitbox[1]:#vị trí +chiều cao
                return True #trả về nếu tọa độ x player ở trên cưa
        return False


class spike(saw):#kế thừa luôn từ lớp saw(cưa) vì 2 cái giống nhau
    img = pygame.image.load(os.path.join('images', 'spike.png'))

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28,315)
        # pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x, self.y))
        
       
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

# updateFile điểm
def updateFile():
    f = open('scores.txt','r')# mở file ở chế độ đọc 
    file = f.readlines() # đọc tất cả các dòng trong danh sách 
    last = int(file[0])# lấy dòng đầu tiên của file

    if last < int(score):# xem điểm hiện tại có lớn hơn điểm tốt nhất trước đó không 
        f.close()# đóng/lưu file
        file = open('scores.txt', 'w')# mở lại nó trong
        file.write(str(score))# ghi 
        file.close()# đóng/lưu file 

        return score

    return last



def endScreen():
    global pause, score, speed, obstacles
    #nhưng biến này cần reset lại 
    pause = 0
    speed = 60
    obstacles = []
#đây là vong lặp khác (vong lạp của game sau khi dc chơi lại)
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():#tạo vòng lặp cho game để làm mới
            # quit game
            if event.type == pygame.QUIT:#kiểm tra nếu user nhấn tắt (dấu X đỏ)
                run = False #kết thucvs vòng lặp
                pygame.quit()#thoát hẳn game
            # dừng mọi action của game
            if event.type == pygame.MOUSEBUTTONDOWN:#kiểm tra khi nhấn chuột
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False

        win.blit(bg, (0,0))
        # hiển thị endScreen
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile()),1,(255,255,255))
        RestartText = largeFont.render('Click to restart!',1,(255,255,255))
        # hiển thị điểm và update điểm cao mới  vào file

        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        win.blit(RestartText,(W/2 - lastScore.get_width()/2, 340))
        pygame.display.update()
    score = 0

def redrawWindow():
    largeFont = pygame.font.SysFont('comicsans', 30)
    win.blit(bg, (bgX, 0))#vẽ bg 1
    win.blit(bg, (bgX2,0))#vẽ bg 2
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    
    
    
    runner.draw(win)#vẽ runner

    for obstacle in obstacles: #vòng lặt hiển thị các chướng ngại
        obstacle.draw(win)

    win.blit(text, (700, 10))
    pygame.display.update() #update screen


pygame.time.set_timer(USEREVENT+1, 500)# Đặt hẹn giờ trong 0,5s userevent có 1 sự kiên người dùng dc kích hoạt
pygame.time.set_timer(USEREVENT+2, random.randrange(2000,3500))# Đặt hẹn giờ trong khoảng 2000-3500 có 1 sự kiên dc kích hoạt



speed = 60
score = 0
run = True
runner = player(200, 313, 64, 64)
# Điều này sẽ vượt lên trên vòng lặp trò chơi của chúng ta



obstacles = [] #tạo mangr chướng ngại vật ngại vật
# lưu trữ tất cả các đối tượng của mình trong một danh sách và lặp qua danh sách để vẽ từng đối tượng.

pause = 0
fallSpeed = 0

while run:
    if pause > 0:#nếu player bị ngã thì pause sẽ +1
        pause += 1
        if pause > fallSpeed * 2:#kiểm tra pause>fallSpeend x2 thì gọi tới end screen()( đến giây t2 thì endscreen hiên lên)
            endScreen()
#nhiệm vụ của if là check time để hiển thị endscreen 
    score = speed//10 - 6 #tính điểm

    for obstacle in obstacles: 
        if obstacle.collide(runner.hitbox):#nếu hibox runner va chạm vs chướng ngại thì runner ngã
            runner.falling = True
            # pygame.time.delay(1000)

            if pause == 0:  #kiểm tra runner đã chạn vào obj chưa
                pause = 1 #pause dc gán =1s
                fallSpeed = speed #speed sẽ ko dc tăng lên nữa


        if obstacle.x < -64: #kiểm tra nếu obj(obstacle) ra khỏi khung hình thì loại bỏ(64px)
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4#dịch chuyển sang tráii nên -1.4

    bgX -= 1.4  #dịch chuyển cả 2 background tạo hieuj ứng di chuyển
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1: #nếu background đã đi qua (-width ) thì reset về vị trí
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False

        if event.type == USEREVENT+1: # Kiểm tra xem bộ đếm thời gian có tắt không 
            speed += 1 #tăng tốc bg

        if event.type == USEREVENT+2: #random hien thị chướng ngại
            r = random.randrange(0,2)
            if r == 0:
                obstacles.append(saw(810, 310, 64, 64))
            elif r == 1:
                obstacles.append(spike(810, 0, 48, 310))

    if runner.falling == False:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:# kiểm tra nhảy 
            if not(runner.jumping): 
                runner.jumping = True

        if keys[pygame.K_DOWN]:# kiểm tra  trượt nếu ko trượt thì trươtj
            if not(runner.sliding):
                runner.sliding = True

    clock.tick(speed)
    redrawWindow()
