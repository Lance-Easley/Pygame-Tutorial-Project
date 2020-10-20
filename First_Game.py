import pygame
pygame.init()

screen_x = 500
screen_y = 480

win = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'),
             pygame.image.load('R3.png'), pygame.image.load('R4.png'),
             pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'),
             pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'),
            pygame.image.load('L3.png'), pygame.image.load('L4.png'),
            pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'),
            pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

#bulletSound = pygame.mixer.Sound('bullet.wav')
#hitSound - pygame.mixer.Sound('hit.wav')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 19, self.y + 15, 28, 47)

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not (self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3],
                         (int(self.x), int(self.y)))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3],
                         (int(self.x), int(self.y)))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (int(self.x), int(self.y)))
            else:
                win.blit(walkLeft[0], (int(self.x), int(self.y)))
        self.hitbox = (self.x + 19, self.y + 15, 28, 47)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        win.blit(text, (screen_x // 2 -(text.get_width() / 2), screen_y // 2))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 101
                    pygame.quit()


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color,
                           (int(self.x), int(self.y)), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),
                 pygame.image.load('R3E.png'), pygame.image.load('R4E.png'),
                 pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),
                 pygame.image.load('R9E.png'), pygame.image.load('R10E.png'),
                 pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'),
                pygame.image.load('L3E.png'), pygame.image.load('L4E.png'),
                pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'),
                pygame.image.load('L9E.png'), pygame.image.load('L10E.png'),
                pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, self.health * 5.75, 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)
        else:
            self.hitbox = (0, 0, 0, 0,)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel *= -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')


def redrawGameWindow():
    win.blit(bg, (0, 0))
    text = font.render(f'Score: {score}', 1, (0, 0, 0))
    win.blit(text, (390, 10))
    mans.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
mans = player(300, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if mans.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and mans.hitbox[1] + mans.hitbox[3] > goblin.hitbox[1]:
            if mans.hitbox[0] + mans.hitbox[2] > goblin.hitbox[0] and mans.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                mans.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                #hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        #bulletSound.play()
        if mans.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 50:
            bullets.append(projectile(round(mans.x + mans.width // 2),
                                      round(mans.y + mans.height // 2),
                                      6, (0, 0, 0), facing))
        shootLoop = 1
            
    if keys[pygame.K_a] and mans.x > 0:
        mans.x -= mans.vel
        mans.left = True
        mans.right = False
        mans.standing = False
    elif keys[pygame.K_d] and mans.x < screen_x - mans.width:
        mans.x += mans.vel
        mans.left = False
        mans.right = True
        mans.standing = False
    else:
        mans.standing = True
        mans.walkCount = 0

    if not(mans.isJump):
        if keys[pygame.K_w]:
            mans.isJump = True
            mans.left = False
            mans.right = False
            mans.walkCount = 0
    else:
        if mans.jumpCount >= -10:
            neg = 1
            if mans.jumpCount < 0:
                neg = -1
            mans.y -= (mans.jumpCount ** 2) * 0.25 * neg
            mans.jumpCount -= 1
        else:
            mans.isJump = False
            mans.jumpCount = 10

    redrawGameWindow()

pygame.quit()
