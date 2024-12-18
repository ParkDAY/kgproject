import pygame
import sys
import random
from time import sleep, time

# Pygame 초기화
pygame.init()

# 상수 정의
BLACK = (0, 0, 0)
padWidth = 600
padHeight = 700

# 운석 이미지와 체력
rockImageWithHealth = [
    ('rock01.png', 1), ('rock02.png', 1), ('rock03.png', 1), ('rock04.png', 1), ('rock05.png', 1),
    ('rock06.png', 1), ('rock07.png', 1), ('rock08.png', 1), ('rock09.png', 1), ('rock10.png', 3),
    ('rock11.png', 3), ('rock12.png', 1), ('rock13.png', 1), ('rock14.png', 2), ('rock15.png', 2),
    ('rock16.png', 1), ('rock17.png', 3), ('rock18.png', 1), ('rock19.png', 1), ('rock20.png', 2),
    ('rock21.png', 2), ('rock22.png', 1), ('rock23.png', 1), ('rock24.png', 1), ('rock25.png', 1),
    ('rock26.png', 1), ('rock27.png', 1), ('rock28.png', 1), ('rock29.png', 1), ('rock30.png', 1)
]

# 게임 초기화 함수
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, rock, rockHealth
    global missileSound, gameOverSound, rockDestroySound, specialSound
    global missileCount, missile_upgrade, lives, rockPassed, score, ult  # 추가된 변수들

    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('PyShooting')
    background = pygame.image.load('background.png')
    fighter = pygame.image.load('fighter.png')
    missile = pygame.image.load('missile.png')
    explosion = pygame.image.load('explosion.png')
    ult = pygame.image.load('ult.png')

    # 효과음 로드
    #missileSound = pygame.mixer.Sound('explosion01.wav')  # 미사일 사운드
    #gameOverSound = pygame.mixer.Sound('explosion02.wav')  # 게임 오버 사운드
    #rockDestroySound = pygame.mixer.Sound('explosion03.wav')  # 운석 파괴 사운드
    #specialSound = pygame.mixer.Sound('explosion04.wav')  # 필살기 사운드

    clock = pygame.time.Clock()
    missileCount = 1  # 초기 미사일 수를 1로 설정
    missile_upgrade = 1  # 초기 무기 레벨 설정
    lives = 3  # 초기 목숨 설정
    rockPassed = 0  # 놓친 운석 수 초기화
    score = 0  # 초기 점수 설정

# 게임 실행 함수
def runGame():
    global gamePad, clock, background, fighter, missile, explosion, rock, rockHealth
    global missileSound, gameOverSound, rockDestroySound, specialSound
    global missileCount, missile_upgrade, lives, rockPassed, score, ult  # 추가된 변수들

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    missileXY = []

    # 첫 번째 운석 초기화
    rockImage, rockHealth = random.choice(rockImageWithHealth)
    rock = pygame.image.load(f'{rockImage}')
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 3

    isShot = False
    shotCount = 0
    special_missile_count = 3  # 필살기 사용 가능 횟수

    ult_drawn_time = None  # 필살기 발사 시간 기록

    onGame = True
    gameOverDisplayed = False  # 게임 오버 메시지 표시 여부

    # 전투기 이동 속도 초기화
    fighter_speed = 5  # 기본 이동 속도

    # 게임 루프
    while onGame:
        current_time = time() * 1000  # 밀리초 단위로 변환
        keys = pygame.key.get_pressed()  # 키 상태 확인

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    offset = - (missileCount - 1) * 10  # 미사일이 중첩되지 않도록 좌우로 간격을 줌
                    for i in range(missileCount):  # 현재 미사일 수만큼 미사일 발사
                        missileX = x + (fighterWidth / 2) + offset + (i * 20)
                        missileY = y - fighterHeight
                        missileXY.append([missileX, missileY])
                    #missileSound.play()  # 미사일 사운드 재생
                elif event.key == pygame.K_s:  # 필살기 발사 키 (S키)
                    if special_missile_count > 0:
                        special_missile_count -= 1
                        ult_drawn_time = current_time  # 필살기 발사 시간 기록
                        isShot = True  # 모든 운석이 제거되도록 설정
                        #specialSound.play()  # 필살기 사운드 재생

        # 키 상태에 따라 전투기 이동
        if keys[pygame.K_LEFT]:
            fighterX = -fighter_speed
        elif keys[pygame.K_RIGHT]:
            fighterX = fighter_speed
        else:
            fighterX = 0

        if keys[pygame.K_UP]:
            fighterY = -fighter_speed
        elif keys[pygame.K_DOWN]:
            fighterY = fighter_speed
        else:
            fighterY = 0

        # 게임의 상태 업데이트 (포지션 등)
        gamePad.blit(background, (0, 0))  # 배경 그리기
        x += fighterX
        y += fighterY
        drawObject(fighter, x, y)

        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth

        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight

        def is_collision(fighterX, fighterY, fighterWidth, fighterHeight, rockX, rockY, rockWidth, rockHeight):
            if (fighterX < rockX + rockWidth and
                fighterX + fighterWidth > rockX and
                fighterY < rockY + rockHeight and
                fighterY + fighterHeight > rockY):
                return True
            return False

        # 충돌 체크 및 생명 감소
        if is_collision(x, y, fighterWidth, fighterHeight, rockX, rockY, rockWidth, rockHeight):
            lives -= 1
            isShot = True  # 운석 파괴
            print(f"Collision detected! Lives remaining: {lives}")

        # 미사일 이동 및 충돌 처리
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] <= 0:
                    missileXY.remove(bxy)
                elif bxy[1] < rockY + rockHeight:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        rockHealth -= 1  # 운석 체력 감소
                        if rockHealth <= 0:
                            isShot = True
                            shotCount += 1
                            score += 100
                            #rockDestroySound.play()  # 운석 파괴 사운드 재생

                            # 500점마다 전투기 이동 속도 증가 (최대 5)
                            if score // 500 > 0:
                                fighter_speed = min(5, 5 + (score // 500))

                            # 1000점마다 미사일 수 증가 (최대 4개) 및 무기 레벨 증가
                            if score >= 1000 and missileCount < 4:
                                missileCount = 2
                                if score >= 2000 and missileCount < 4:
                                    missileCount = 3
                                    if score >= 3000 and missileCount < 4:
                                        missileCount = 4

                                missile_upgrade = missileCount  # 미사일 갯수에 따라 무기 레벨 설정

        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)

        if isShot:
            drawObject(explosion, rockX, rockY)

            # 새로운 운석 생성 및 체력 초기화
            rockImage, rockHealth = random.choice(rockImageWithHealth)
            rock = pygame.image.load(f'{rockImage}')
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

            isShot = False
            rockSpeed += 0.02 * (score // 500)
            if rockSpeed >= 10:
                rockSpeed = 10

        rockY += rockSpeed

        if rockY > padHeight:
            rockImage, rockHealth = random.choice(rockImageWithHealth)
            rock = pygame.image.load(f'{rockImage}')
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0

            rockPassed += 1
            lives -= 1  # 운석이 놓쳤을 때 목숨 감소
            score -= 1000  # 놓친 운석으로 인한 점수 감소

        if rockPassed == 3 or lives <= 0:
            gameOver()

        # 필살기 표시 처리
        if ult_drawn_time and current_time - ult_drawn_time < 1000:
            drawObject(ult, 0, 0)  # 필살기 표시
        else:
            ult_drawn_time = None  # 필살기 타이머 종료

        drawObject(rock, rockX, rockY)
        writeScore(score)
        writePassed(rockPassed)
        writeSpecialMissileCount(special_missile_count)
        writeMissileUpgrade(missile_upgrade)
        writeLives(lives)

        pygame.display.update()
        clock.tick(60)

# 객체 그리기 함수
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

# 텍스트 쓰기 함수
def writeText(text, size, x, y, color=(255, 255, 255)):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    gamePad.blit(textSurface, textRect)

# 점수 표시 함수
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('점수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (padWidth // 2 - 50, 0))

# 놓친 운석 표시 함수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('놓친 운석: ' + str(count), True, (255, 0, 0))
    gamePad.blit(text, (460, 0))

# 필살기 수 표시 함수
def writeSpecialMissileCount(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('필살기: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 30))

# 무기 레벨 표시 함수
def writeMissileUpgrade(level):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('무기 레벨: ' + str(level), True, (255, 255, 255))
    gamePad.blit(text, (460, 30))

# 목숨 표시 함수
def writeLives(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('목숨: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 60))

# 게임 오버 메시지 함수
def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font('NanumGothic.ttf', 40)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    #gameOverSound.play()  # 게임 오버 사운드 재생
    sleep(2)
    #pygame.mixer.music.play(-1)
    runGame()

# 게임 오버 처리 함수
def gameOver():
    writeMessage('게임 오버!')

# 게임 초기화 및 실행
initGame()
runGame()
