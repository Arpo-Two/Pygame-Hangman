import pygame
import random
pygame.init()
pygame.font.init()
tlarg = 821
talt = 600
pygame.display.set_caption('Hangman')
fonte = pygame.font.SysFont('Candaras', 70)
small = pygame.font.SysFont('Candaras', 50)

win = pygame.display.set_mode((tlarg, talt), pygame.FULLSCREEN)
default = (247, 197, 0)
looser = (138, 7, 7)
winner = (97, 138, 61)
with open('words.txt', 'r') as f:
    names =[line.strip() for line in f]


class Game(object):
    def __init__(self):
        self.word = random.choice(names)
        self.misses = 0
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                        'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.pos = [(381, 50), (381, 135), (381, 220), (381, 305),
                    (477, 50), (477, 135), (477, 220), (477, 305), (477, 390), (477, 475),
                    (573, 50), (573, 135), (573, 220), (573, 305), (573, 390), (573, 475),
                    (669, 50), (669, 135), (669, 220), (669, 305), (669, 390), (669, 475),
                    (765, 50), (765, 135), (765, 220), (765, 305)]
        self.lines = []
        self.discovered_letters = []
        self.color = default
        self.score = 1000 * names.index(self.word) / len(names)
        self.menu = True
        self.difficulty = 'easy'
        self.veasy_color = (238, 130, 238)
        self.easy_color = (148, 0, 211)
        self.medium_color = (238, 130, 238)
        self.hard_color = (238, 130, 238)
        self.vhard_color = (238, 130, 238)


game = Game()


def menu():
    pygame.draw.rect(win, (0, 0, 0), (0, 0, tlarg // 5, talt // 3), 8)
    pygame.draw.rect(win, game.veasy_color, (0, 0, tlarg // 5, talt // 3))
    win.blit(fonte.render('V.Easy', False, (0, 0, 0)), (5, 80))

    pygame.draw.rect(win, (0, 0, 0), (tlarg // 5, 0, tlarg // 5, talt // 3), 8)
    pygame.draw.rect(win, game.easy_color, (tlarg // 5, 0, tlarg // 5, talt // 3))
    win.blit(fonte.render('Easy', False, (0, 0, 0)), (30 + tlarg // 5, 80))

    pygame.draw.rect(win, (0, 0, 0), (2 * tlarg // 5, 0, tlarg // 5, talt // 3), 8)
    pygame.draw.rect(win, game.medium_color, (2 * tlarg // 5, 0, tlarg // 5, talt // 3))
    win.blit(small.render('Medium', False, (0, 0, 0)), (20 + 2 * tlarg // 5, 90))

    pygame.draw.rect(win, (0, 0, 0), (3 * tlarg // 5, 0, tlarg // 5, talt // 3), 8)
    pygame.draw.rect(win, game.hard_color, (3 * tlarg // 5, 0, tlarg // 5, talt // 3))
    win.blit(fonte.render('Hard', False, (0, 0, 0)), (20 + 3 * tlarg // 5, 80))

    pygame.draw.rect(win, (0, 0, 0), (4 * tlarg // 5, 0, tlarg // 5, talt // 3), 8)
    pygame.draw.rect(win, game.vhard_color, (4 * tlarg // 5, 0, tlarg // 5, talt // 3))
    win.blit(fonte.render('V.Hard', False, (0, 0, 0)), (4 * tlarg // 5, 80))

    pygame.draw.rect(win, (0, 0, 0), (tlarg // 3, talt * 2 // 3, tlarg // 3, talt // 3), 8)
    pygame.draw.rect(win, (230, 230, 250), (tlarg // 3, talt * 2 // 3, tlarg // 3, talt // 3))
    win.blit(fonte.render('Play', False, (0, 0, 0)), (80 + tlarg // 3, 80 + talt * 2 // 3))


def dr(x1, x2, y1, y2):
    return((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def ocurrs(letter, string):
    po = []
    for le in enumerate(string):
        if le[1] == letter:
            po.append(le[0])
    return po


def organize(lines):
    old_list = lines
    new_list = []
    for _ in range(0, len(old_list)):
        b = 1000
        c = None
        for x in enumerate(old_list):
            if x[1][0] < b:
                b = x[1][0]
                c = x[0]
        if old_list[c][0] < old_list[c][1]:
            new_list.append(old_list[c])
        else:
            new_list.append((old_list[c][1], old_list[c][0]))
        old_list.remove(old_list[c])
    return new_list


def new_game():
    if game.difficulty == 'veasy':
        game.word = names[random.randint(0, len(names) // 5)]
    elif game.difficulty == 'easy':
        game.word = names[random.randint(len(names) // 5, len(names) * 2 // 5)]
    elif game.difficulty == 'medium':
        game.word = names[random.randint(2 * len(names) // 5, len(names) * 3 // 5)]
    elif game.difficulty == 'hard':
        game.word = names[random.randint(3 * len(names) // 5, len(names) * 5 // 5)]
    else:
        game.word = names[random.randint(len(names) * 4 // 5, len(names))]
    game.misses = 0
    game.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                    'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    game.pos = [(381, 50), (381, 135), (381, 220), (381, 305),
                (477, 50), (477, 135), (477, 220), (477, 305), (477, 390), (477, 475),
                (573, 50), (573, 135), (573, 220), (573, 305), (573, 390), (573, 475),
                (669, 50), (669, 135), (669, 220), (669, 305), (669, 390), (669, 475),
                (765, 50), (765, 135), (765, 220), (765, 305)]
    game.lines = []
    game.discovered_letters = []
    game.color = default
    if len(game.word) % 2 == 0:
        l = len(game.word) - 2
        game.lines.append((355, 400))
        game.lines.append((405, 450))
        while l > 0:
            if l % 2 == 0:
                game.lines.append((405 + (len(game.word) - l) * 25, 450 + (len(game.word) - l) * 25))
                l -= 1
            else:
                game.lines.append((425 - (len(game.word) - l) * 25, 380 - (len(game.word) - l) * 25))
                l -= 1
    else:
        l = len(game.word) - 1
        game.lines.append((380, 425))
        while l > 0:
            if l % 2 == 0:
                game.lines.append((405 + (len(game.word) - l) * 25, 450 + (len(game.word) - l) * 25))
                l -= 1
            else:
                game.lines.append((425 - (len(game.word) - l) * 25, 380 - (len(game.word) - l) * 25))
                l -= 1
    game.lines = organize(game.lines)
    game.score = 1000 * names.index(game.word) / len(names)



run = True
while run:
    pygame.time.Clock()
    win.fill(game.color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.menu:
                if pygame.mouse.get_pos()[1] < talt // 3:
                    if pygame.mouse.get_pos()[0] < tlarg // 5:
                        game.veasy_color = (148, 0, 211)
                        game.easy_color = (238, 130, 238)
                        game.medium_color = (238, 130, 238)
                        game.hard_color = (238, 130, 238)
                        game.vhard_color = (238, 130, 238)
                        game.difficulty = 'veasy'
                    elif pygame.mouse.get_pos()[0] < 2 * tlarg // 5:
                        game.veasy_color = (238, 130, 238)
                        game.easy_color = (148, 0, 211)
                        game.medium_color = (238, 130, 238)
                        game.hard_color = (238, 130, 238)
                        game.vhard_color = (238, 130, 238)
                        game.difficulty = 'easy'
                    elif pygame.mouse.get_pos()[0] < 3 * tlarg // 5:
                        game.veasy_color = (238, 130, 238)
                        game.easy_color = (238, 130, 238)
                        game.medium_color = (148, 0, 211)
                        game.hard_color = (238, 130, 238)
                        game.vhard_color = (238, 130, 238)
                        game.difficulty = 'medium'
                    elif pygame.mouse.get_pos()[0] < 4 * tlarg // 5:
                        game.veasy_color = (238, 130, 238)
                        game.easy_color = (238, 130, 238)
                        game.medium_color = (238, 130, 238)
                        game.hard_color = (148, 0, 211)
                        game.vhard_color = (238, 130, 238)
                        game.difficulty = 'hard'
                    else:
                        game.veasy_color = (238, 130, 238)
                        game.easy_color = (238, 130, 238)
                        game.medium_color = (238, 130, 238)
                        game.hard_color = (238, 130, 238)
                        game.vhard_color = (148, 0, 211)
                        game.difficulty = 'vhard'
                elif pygame.mouse.get_pos()[1] > talt * 2 // 3 and 2 * tlarg // 3 > pygame.mouse.get_pos()[0] >\
                        tlarg // 3:
                    game.menu = False
                    if game.difficulty == 'easy':
                        game.word = names[random.randint(0, len(names) // 3)]
                    elif game.difficulty == 'medium':
                        game.word = names[random.randint(len(names) // 3, len(names) * 2 // 3)]
                    else:
                        game.word = names[random.randint(len(names) * 2 // 3, len(names))]
                    new_game()

            else:
                if game.color != default:
                    new_game()
                if dr(pygame.mouse.get_pos()[0], 125, pygame.mouse.get_pos()[1], 250) < 50:
                    game.menu = True
                for p in game.pos:
                    if p is not None:
                        if dr(pygame.mouse.get_pos()[0], p[0], pygame.mouse.get_pos()[1], p[1]) < 40:
                            letter = game.letters[game.pos.index(p)][-1].lower()
                            if letter in game.word:
                                for o in ocurrs(letter, game.word):
                                    game.discovered_letters.append((letter, o))

                            else:
                                game.misses += 1

                            game.pos[game.pos.index(p)] = None

    if game.menu:
        menu()
    else:

        pygame.draw.rect(win, (0, 0, 0), (50, 40, 20, 470))
        pygame.draw.rect(win, (0, 0, 0), (50, 40, 200, 20))
        pygame.draw.rect(win, (0, 0, 0), (250, 40, 20, 75))
        pygame.draw.rect(win, (0, 0, 0), (195, 115, 130, 20))

        if game.misses > 0:
            pygame.draw.circle(win, (0, 0, 0), (260, 200), 50, 4)
            if game.misses > 1:
                pygame.draw.line(win, (0, 0, 0), (260, 255), (260, 400), 4)
                if game.misses > 2:
                    pygame.draw.line(win, (0, 0, 0), (265, 405), (300, 500), 4)
                    if game.misses > 3:
                        pygame.draw.line(win, (0, 0, 0), (255, 405), (220, 500), 4)
                        if game.misses > 4:
                            pygame.draw.line(win, (0, 0, 0), (255, 305), (220, 380), 4)
                            if game.misses > 5:
                                pygame.draw.line(win, (0, 0, 0), (265, 305), (300, 380), 4)
                            if game.misses > 6:
                                pygame.draw.line(win, (0, 0, 0), (230, 190), (250, 170), 4)
                                pygame.draw.line(win, (0, 0, 0), (230, 170), (250, 190), 4)
                                pygame.draw.line(win, (0, 0, 0), (270, 190), (290, 170), 4)
                                pygame.draw.line(win, (0, 0, 0), (270, 170), (290, 190), 4)
                                game.color = looser
                                for p in game.pos:
                                    if p is not None:
                                        letter = game.letters[game.pos.index(p)][-1].lower()
                                        if letter in game.word:
                                            for o in ocurrs(letter, game.word):
                                                game.discovered_letters.append((letter, o))
        if len(game.discovered_letters) == len(game.word):
            game.color = winner
        for line in game.lines:
            pygame.draw.line(win, (0, 0, 0), (line[0], 580), (line[1], 580))
        for dl in game.discovered_letters:
            win.blit(fonte.render(dl[0], False, (0, 0, 0)), (game.lines[dl[1]][0], 540))
        for p in game.pos:
            if p is not None:
                pygame.draw.circle(win, (0, 204, 255), (p[0], p[1]), 40)
                pygame.draw.circle(win, (0, 0, 0), (p[0], p[1]), 40, 6)
                win.blit(fonte.render(game.letters[game.pos.index(p)], False, (0, 0, 0)), (p[0] - 20, p[1] - 20))
        pygame.draw.circle(win, (238, 130, 238), (125, 125), 50)
        pygame.draw.circle(win, (0, 0, 0), (125, 125), 50, 6)
        if game.color != default:
            win.blit(fonte.render(str(round(game.score)), False, (0, 0, 0)), (85, 105))
        pygame.draw.circle(win, (238, 30, 30), (125, 250), 50)
        pygame.draw.circle(win, (0, 0, 0), (125, 250), 50, 6)
        win.blit(fonte.render('B', False, (0, 0, 0)), (105, 230))
    pygame.display.update()
