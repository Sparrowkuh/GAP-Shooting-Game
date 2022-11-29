import pygame
import sys #system 라이브러리
from time import sleep #게임은 시간과 관련된 것이 있어야 한다.
import random

#화면 크키 설정
#RGB를 0으로 설정해서 검은색을 만드는 방법(BLACK=(0, 0, 0))
screen_w=480
screen_h=640
rockimage=['rock01.png', 'rock02.png', 'rock03.png', 'rock04.png', 'rock05.png', \
           'rock06.png', 'rock07.png', 'rock08.png', 'rock09.png', 'rock10.png', \
           'rock11.png', 'rock12.png', 'rock13.png', 'rock14.png', 'rock15.png', \
           'rock01.png', 'rock17.png', 'rock18.png', 'rock19.png', 'rock20.png', \
           'rock01.png', 'rock22.png', 'rock23.png', 'rock24.png', 'rock25.png', \
           'rock01.png', 'rock27.png', 'rock28.png', 'rock29.png', 'rock30.png']
explosionsound=['explosion01.wav', 'explosion02.wav', 'explosion03.wav', 'explosion04.wav']

#운석을 맞춘 개수 계산(실제로는 오염물) https://blog.naver.com/mollayo18/221560236410->폰트 수정 참고
def writescore(count):
    global screen
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 오염물:'+ str(count), True, (255,255,255))
    screen.blit(text, (10,0))

#운석이 화면 아래로 통과한 개수(놓친 오염물)
def writepassed(count):
    global screen
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 오염물:'+ str(count), True, (255,0,0))#255, 0, 0은 RGB를 의미한다.
    screen.blit(text, (360,0))

#운석이 화면 아래로 통과한 개수(놓친 오염물)
def writemessage(text):
    global screen, gameoversound
    textfont = pygame.font.Font('NanumGothic.ttf', 70)
    text = textfont.render(text, True, (255,0,0))#255, 0, 0은 RGB를 의미한다.
    textpos=text.get_rect()
    textpos.center=(screen_w/2, screen_h/2) #정중앙에 출력
    screen.blit(text, textpos)
    pygame.display.update() #화면 업데이트
    pygame.mixer.music.stop() #배경음악 정지
    gameoversound.play()#게임오버 사운드 재생
    sleep(2)#2초 쉬고 게임 다시 실
    pygame.mixer.music.play(-1)#배경음악 재생
    runGame()


#전투기가 운석과 충돌했을 때 메세지 출력
def crash():
    global screen
    writemessage('GAME OVER')

#게임오버 메세지 출력
def gameover():
    global screen
    writemessage('GAME OVER')


#게임에 등장하는 객체를 드로잉
def drawobj(obj, x, y):
    global screen
    screen.blit(obj, (x, y))#blit는 비티 현상과 관련해서 해당하는 오브젝트를 xy좌표로부터 그리라는 뜻


def initGame():
    global screen, clock, background, fighter, missile, explosion, missilesound, gameoversound
    pygame.init()
    screen=pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption('GAP Shooting Game') #이름
    background = pygame.image.load('background.png') #배경그림
    fighter = pygame.image.load('fighter.png') #전투기그림
    missile = pygame.image.load('missile.png') #미사일그림
    explosion=pygame.image.load('explosion.png')#폭발그림
    pygame.mixer.music.load('music.wav')
    pygame.mixer.music.play(-1)
    missilesound=pygame.mixer.Sound('missile.wav')
    gameoversound=pygame.mixer.Sound('gameover.wav')
    clock=pygame.time.Clock()

def runGame(): #게임 실행함수
    global screen, clock, background, fighter, missile, explosion, missilesound, gameoversound

    #전투기 크기
    fightersize=fighter.get_rect().size
    fighterw=fightersize[0]
    fighterh=fightersize[1]

    #전투기 초기위치(x,y)
    x=screen_w*0.45
    y=screen_h*0.9 #폭에서 0.45, 높이에서 0.9->중간위
    fighterX=0
    fighterY=0

    #무기좌표리스트
    missileXY=[]

    #운석 랜덤생성
    rock=pygame.image.load(random.choice(rockimage))
    rocksize=rock.get_rect().size #운석크기
    rockw=rocksize[0]
    rockh=rocksize[1]
    destroysound=pygame.mixer.Sound(random.choice(explosionsound))

    #운석초기위치설정
    rockX=random.randrange(0, screen_w-rockw)
    rockY=0
    rockSpeed=2

    #미사일에 운석이 맞은 경우 True
    isshot=False
    shotcount=0
    rockpassed=0

   
    #gameover
    
    onGame=False
    while not onGame:
        for event in pygame. event. get():
            if event.type in [pygame.QUIT]:#게임 프로그램 종료
                pygame.quit()
                sys.exit()

            if event.type in [pygame.KEYDOWN]: #키가 눌리면
                if event.key==pygame.K_LEFT: #전투기 왼쪽으로 이동
                    fighterX-=5

                elif event.key==pygame.K_RIGHT: #전투기 오른쪽으로 이동
                    fighterX+=5

                elif event.key==pygame.K_DOWN: #전투기 아래로 이동
                    fighterY +=5

                elif event.key==pygame.K_UP: #전투기 위로 이동
                    fighterY -=5

                elif event.key==pygame.K_SPACE: #미사일 발사
                    missilesound.play() #미사일 사운
                    missileX =x+fighterw/2 #미사일이 전투기 중간에서 나오게끔 설정
                    missileY =y-fighterh
                    missileXY.append([missileX, missileY])

            if event.type in [pygame.KEYUP]: #키 눌림이 해제되면
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    fighterX=0
                elif event.key==pygame.K_DOWN or event.key==pygame.K_UP:
                    fighterY=0

        drawobj(background, 0, 0) #배경화면 그리기

        #전투기 위치 재조정
        x += fighterX
        if x<0:
            x=0
        elif x>screen_w - fighterw:
            x=screen_w - fighterw

        y += fighterY
        if y<0:
            y=0
        elif y>screen_h - fighterh:
            y=screen_h - fighterh


        #전투기가 운석과 충돌했는지 체크
        if y<rockY + rockh:
            if (rockX>x and rockX< x+fighterw) or (rockX+rockw>x and rockX+rockw<x+fighterw):
                crash()

        drawobj(fighter, x, y) #비행기를 x,y에 그리기


        #미사일 발사 화면에 그리기
        if len(missileXY)!=0:
            for i, bxy in enumerate(missileXY): #미사일 요소에 대해 반복
                bxy[1] -= 10 #총알의 y좌표 -10(위로이동)
                missileXY[i][1]=bxy[1]

                #미사일이 운석을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX+rockw:
                        missileXY.remove(bxy)
                        isshot= True
                        shotcount +=1

                if bxy[1] <=0: #미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy) #미사일 제거
                        
                    except:
                        pass

        if len(missileXY)!=0:
            for bx, by in missileXY:
                drawobj(missile, bx, by)


        #오염물 점수 표시
        writescore(shotcount)

        rockY += rockSpeed #운석이 아래로 움직임

        #운석을 여러개 하고싶으면 '''맞아요. 조금 복잡해     rockY += rockSpeed -> for rock in stones: rock[1] += rockSpeed'''

        #운석이 지구로 떨어진 경우
        if rockY > screen_h:
            #새로운 운석(랜덤)
            rock=pygame.image.load(random.choice(rockimage))
            rockSize=rock.get_rect().size
            rockw=rockSize[0]
            rockh=rockSize[1]
            rockX=random.randrange(0, screen_w-rockw)
            rockY=0
            rockpassed +=1


        #3개 놓치면 게임오버
        if rockpassed ==3:
            gameover()

        #놓친 점수 표시
        writepassed(rockpassed)

        #전투기와 운석이 부딪힌 경우
        '''if crash:
            drawobj(explosion, rockX, rockY)

            #멈추기
            x += fighterX
            if x<0:
                x=0
            elif x>screen_w - fighterw:
                x=screen_w - fighterw

            y += fighterY
            if y<0:
                y=0
            elif y>screen_h - fighterh:
                y=screen_h - fighterh'''



            #drawobj(fighter, x, y) #비행기를 x,y에 그리기
            
        
            

        #운석을 맞춘 경우
        if isshot:
            #운석 폭발
            drawobj(explosion, rockX, rockY)
            destroysound.play() #운석폭발사운드 재생

            #새로운 운석(랜덤)
            rock=pygame.image.load(random.choice(rockimage))
            rockSize=rock.get_rect().size
            rockw=rockSize[0]
            rockh=rockSize[1]
            rockX=random.randrange(0, screen_w-rockw)
            rockY=0
            destroysound = pygame.mixer.Sound (random.choice(explosionsound))
            isshot=False

            #운석 맞추면 속도 증가
            rockSpeed += 0.05
            if rockSpeed>=10:
                rockSpeed=10

        

                
        drawobj(rock, rockX, rockY)#운석그리기

        pygame.display.update() #게임화면을 다시그림

        clock.tick(60) #게임화면의 초당 프레임수를 60으로 설정

    pygame.quit() #pygame 종료

initGame()
runGame()


