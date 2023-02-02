import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60

# game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Stick men test')

# define game variables
current_character= 1
total_characters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
healthP = False
healthP_effect = 15
Strike = False
damage_effect = 15
clicked = False
game_over = 0

# define fonts
font = pygame.font.SysFont('Arial', 26)

# define colours
red = (255, 0, 0)
green = (0, 255, 0)
black = (0,0,0)

# load images
# background image
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
# panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
# button images
healthP_img = pygame.image.load('img/Icons/healthP.png').convert_alpha()
Strike_img = pygame.image.load('img/Icons/Strike.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
# load victory and defeat images
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
# cursor image
cursor_rep_img = pygame.image.load('img/Icons/cursor_rep.png').convert_alpha()


# create function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_background():
    screen.blit(background_img, (0, 0))


# function for drawing panel
def draw_panel():
    """
    :return:
    """
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    draw_text(f'HP: {player.hp}  MP: {player.magic}', font, green, 100, screen_height - bottom_panel + 10)
    y: character
    for count, y in enumerate(enemy_list):
        draw_text(f'HP: {y.hp}  MP: {y.magic}', font, green, 520, (screen_height - bottom_panel + 20) + count * 60)


# character class
class character():
    def __init__(self, x, y, name, max_hp, strength, potency, healthPs, max_magic, Strikes):
        """
        :param x:
        :param y:
        :param name:
        :param max_hp:
        :param strength:
        :param potency:
        :param healthPs:
        :param max_magic:
        """
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.magic = max_magic
        self.max_magic = max_magic
        self.potency = potency
        self.strength = strength
        self.start_healthPs = healthPs
        self.healthPs = healthPs
        self.start_Strikes = Strikes
        self.Strikes=Strikes
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # load idle images
        temp_list = []
        for i in range(5):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(12):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load hurt images
        temp_list = []
        for i in range(6):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load death images
        temp_list = []
        for i in range(14):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load magic images
        temp_list = []
        for i in range(0):
            img = pygame.image.load(f'img/{self.name}/Magic/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load magic attack
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        """
        :return:
        """
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()



    def attack(self, target):
        """
        :param target:
        :return:
        """
        # deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # run enemy hurt animation
        target.hurt()
        # check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def idle(self):
        """
        :return:
        """
        # set variables to idle animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def hurt(self):
        """
        :return:
        """
        # set variables to hurt animation
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        """
        :return:
        """
        # set variables to death animation
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        """
        :return:
        """
        self.alive = True
        self.healthPs = self.start_healthPs
        self.Strikes = self.start_Strikes
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        """
        :return:
        """
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        """
        :param x:
        :param y:
        :param hp:
        :param max_hp:
        """
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        """
        :param hp:
        :return:
        """
        # update with new health
        self.hp = hp
        # calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, black, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, red, (self.x, self.y, 150 * ratio, 20))

class MagicBar():
    def __init__(self, x, y, mp, max_mp):
        """
        :param x:
        :param y:
        :param mp:
        :param max_mp:
        """
        self.x = x
        self.y = y
        self.magic = mp
        self.max_mp = max_mp

    def draw(self, mp):
        """
        :param mp:
        :return:
        """
        # update with new health
        self.mp = mp
        # calculate health ratio
        ratio = self.mp / self.max_mp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))




class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        """
        :param x:
        :param y:
        :param damage:
        :param colour:
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        """
        :return:
        """
        # move damage text up
        self.rect.y -= 1
        # delete the text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()


damage_text_group = pygame.sprite.Group()

player = character(200, 260, 'player', 25, 10, 40, 3, 25,3)
enemy1 = character(250, 270, 'enemy', 20, 6, 20, 1, 25,0)
enemy2 = character(530, 270, 'enemy', 20, 6, 20, 1, 25,0)

enemy_list = []
enemy_list.append(enemy1)
enemy_list.append(enemy2)

# create buttons
healthP_button = button.Button(screen, 100, screen_height - bottom_panel + 70, healthP_img, 64, 64)
Strike_button = button.Button(screen, 200, screen_height - bottom_panel + 70, Strike_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

player_health_bar = HealthBar(100, screen_height - bottom_panel + 40, player.hp, player.max_hp)
enemy1_health_bar = HealthBar(180,150, enemy1.hp, enemy1.max_hp)
enemy2_health_bar = HealthBar(460,150, enemy2.hp, enemy2.max_hp)


run = True
while run:

    clock.tick(fps)

    # draw background
    draw_background()

    # draw panel
    draw_panel()
    player_health_bar.draw(player.hp)
    enemy1_health_bar.draw(enemy1.hp)
    enemy2_health_bar.draw(enemy2.hp)

    # draw characters

    for enemy in enemy_list:
        enemy.update()
        enemy.draw()

    # draw the damage text
    damage_text_group.update()
    damage_text_group.draw(screen)

    # control player actions
    # reset action variables
    attack = False
    healthP = False
    Strike = False
    target = None
    # make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, enemy in enumerate(enemy_list):
        if enemy.rect.collidepoint(pos):
            # hide mouse
            pygame.mouse.set_visible(False)
            # show cursor_rep in place of mouse cursor
            screen.blit(cursor_rep_img, pos)
            if clicked == True and enemy.alive == True:
                attack = True
                target = enemy_list[count]
    if healthP_button.draw():
        healthP = True
    # show number of healthPs remaining
    draw_text(str(player.healthPs), font, red, 150, screen_height - bottom_panel + 70)
    if Strike_button.draw():
        Strike = True
    # show number of Strikes remaining
    draw_text(str(player.Strikes), font, red, 250, screen_height - bottom_panel + 70)

    if game_over == 0:
        # player action
        if player.alive == True:
            if current_character == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    # look for player action
                    # attack
                    if attack == True and target != None:
                        player.attack(target)
                        current_character += 1
                        action_cooldown = 0
                    # healthP
                    if healthP == True:
                        if player.healthPs > 0:
                            # check if the healthP would heal the player beyond max health
                            if player.max_hp - player.hp > healthP_effect:
                                heal_amount = healthP_effect
                            else:
                                heal_amount = player.max_hp - player.hp
                            player.hp += heal_amount
                            player.healthPs -= 1
                            damage_text = DamageText(player.rect.centerx, player.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_character += 1
                            action_cooldown = 0
                    #Strikes
                    if Strike == True:
                        if player.Strikes > 0:
                            damage_amount = 10
                            damage_amount - enemy.hp
                            player.Strikes -= 1
                            damage_text = DamageText(enemy.rect.centerx, enemy.rect.y, str(damage_amount), red)
                            damage_text_group.add(damage_text)
                            current_character += 1
                            action_cooldown = 0
        else:
            game_over = -1

        # enemy action ai
        for count, enemy in enumerate(enemy_list):
            if current_character == 2 + count:
                if enemy.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        # check if enemy needs to heal first
                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.healthPs > 0:
                            # check if the healthP would heal the enemy beyond max health
                            if enemy.max_hp - enemy.hp > healthP_effect:
                                heal_amount = healthP_effect
                            else:
                                heal_amount = enemy.max_hp - enemy.hp
                            enemy.hp += heal_amount
                            enemy.healthPs -= 1
                            damage_text = DamageText(enemy.rect.centerx, enemy.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_character += 1
                            action_cooldown = 0
                        # attack
                        else:
                            enemy.attack(player)
                            current_character += 1
                            action_cooldown = 0
                else:
                    current_character += 1

        # if all characters have had a turn then reset
        if current_character > total_characters:
            current_character = 1

    # check if all enemys are dead
    alive_enemies = 0
    for enemy in enemy_list:
        if enemy.alive == True:
            alive_enemies += 1
    if alive_enemies == 0:
        game_over = 1

    # check if game is over
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (290, 50))
        if restart_button.draw():
            player.reset()
            for enemy in enemy_list:
                enemy.reset()
            current_character = 1
            action_cooldown
            game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else:
            clicked = False

    pygame.display.update()

pygame.quit()
