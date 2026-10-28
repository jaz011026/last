import os
import random
import shutil
import sys
import time
import pygame

pygame.init()
pygame.mixer.init()

# Load background music and sound effects
criit = pygame.mixer.Sound("crit.wav")
chet = pygame.mixer.Sound("cheat.wav")
bg = pygame.mixer.Sound("Energizing Game.wav")
back = pygame.mixer.Sound("back.wav")
bell = pygame.mixer.Sound("bell.wav")
buy = pygame.mixer.Sound("buy.wav")
denied = pygame.mixer.Sound("denied.wav")
hurt = pygame.mixer.Sound("hurt.wav")  
lose = pygame.mixer.Sound("ko_lose.wav")
win = pygame.mixer.Sound("ko_win.wav")
tick = pygame.mixer.Sound("tick.wav")
select = pygame.mixer.Sound("select.wav")
move = pygame.mixer.Sound("move.wav")
punch = pygame.mixer.Sound("punch.wav") 
roar = pygame.mixer.Sound("roar.wav")
ult1 = pygame.mixer.Sound("ult.wav")
ult2 = pygame.mixer.Sound("ult_berserk.wav")
ult3 = pygame.mixer.Sound("ult_bloodlust.wav")
ult4 = pygame.mixer.Sound("ult_lava.wav")

bg.set_volume(0.1)
back.set_volume(0.3)
bell.set_volume(0.5)
buy.set_volume(0.5)
criit.set_volume(1)
chet.set_volume(0.6)
denied.set_volume(0.5)
hurt.set_volume(0.6)
win.set_volume(0.6)
lose.set_volume(0.6)
tick.set_volume(0.5)
select.set_volume(0.5)
move.set_volume(0.5)


# Play the music (-1 means it will loop forever in the background)
bg.play(-1)

# --- YOUR ORIGINAL VARIABLES (DO NOT CHANGE) ---
ult = 0
xult = 0
gold = 0
pdamage = 20
pdmg = 30
crit = random.randint(1, 100)
player = 100
pult = 1.5
ehit = 0
phit = 0
x = 1
a = 0
b = 0
c = 0
next = 0
cheat = 0
crits = 0
map2 = 0
map3 = 0
enemy = 0
hp = 0
dmg = 0
edmg = 0
choice1 = 0
choice2 = 0
choice4 = 0
choice6 = 0
gg = 0
gol = 0

wrong_count = 0
slow_count = 0
last_action_text = "None"
ult_status_text = "CHARGING [---]"

# --- GRAPHICS & LARGE SPRITES ---
FONT = {
    "P": ["#### ", "#   #", "#### ", "#    ", "#    "],
    "U": ["#   #", "#   #", "#   #", "#   #", " ### "],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    "C": [" ####", "#    ", "#    ", "#    ", " ####"],
    "H": ["#   #", "#   #", "#####", "#   #", "#   #"],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    "Y": ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    "E": ["#####", "#    ", "#### ", "#    ", "#####"],
    "A": [" ### ", "#   #", "#####", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", " ### "],
    "K": ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    "W": ["#   #", "#   #", "# # #", "## ##", "#   #"],
    "I": ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#####"],
    "S": [" ####", "#    ", " ### ", "    #", "#### "],
    "M": ["#   #", "## ##", "# # #", "#   #", "#   #"],
    "Q": [" ### ", "#   #", "# # #", "#  ##", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#### "],
    "F": ["#####", "#    ", "#### ", "#    ", "#    "],
    " ": ["   ", "   ", "   ", "   ", "   "],
}

TITLE = "PUNCH TYPE"

def block_text(text):
    return [" ".join(FONT[ch][row] for ch in text) for row in range(5)]

BOX_W = 16

# DYNAMIC PLAYER FRAMES BASED ON EQUIPPED GLOVES
def get_player_frame(punching=False):
    if choice6 == 2:
        glove = "[^]" # Spiked Gloves
    elif choice6 == 3:
        glove = "[*]" # Bomb Gloves
    elif choice6 == 4:
        glove = "[#]" # Lava Gloves
    else:
        glove = "(@)" # No Gloves / Standard Fists

    if punching:
        raw = [
            "  .-\"\"\"\"\"-.  ",
            " /  ,   ,  \\ ",
            "|  (>) (<)  |",
            " \\   O     / ",
            "  \\  ===  /  ",
            f" {glove}=\\___/={glove}==>",
            "   |   |   ",
            "  |   |  ",
            "    |___|     ",
        ]
    else:
        raw = [
            "  .-\"\"\"\"\"-.  ",
            " /  ,   ,  \\ ",
            "|  (o) (o)  |",
            " \\   ^     / ",
            "  \\  ===  /  ",
            f" {glove}=\\___/={glove} ",
            "   |   |   ",
            "  |   |  ",
            "    |___|     ",
    ]
    return [l.center(BOX_W) for l in raw]

# MAP 1: STREET THUG
THUG_IDLE = [
    "   .------.   ",
    "  / x  x   \\  ",
    " |   v v    | ",
    "  \\  ===   /  ",
    "   \\ ___  /   ",
    "(#)==/___\\==(#)",
    "   | # |   ",
    "   |   |   ",
    "    |___|     ",
]
THUG_HURT = [
    "   .------.   ",
    "  / >  <   \\  ",
    " |   o o    | ",
    "  \\   W    /  ",
    "   \\ ===  /   ",
    "(#)==\\___/==(#)",
    "   | # |   ",
    "   |   |   ",
    "    |___|     ",
]
THUG_ATTACK = [
    "   .------.   ",
    "  / x  x   \\  ",
    " |   v v    | ",
    "  \\  ===   /  ",
    "   \\ ___  /   ",
    "<==(#)==/___\\==(#)",
    "   | # |    ",
    "   |   |    ",
    "    |___|     ",
]

# MAP 2: UNDERGROUND BRAWLER
BRAWLER_IDLE = [
    "   ._______.  ",
    "  / -  -  \\  ",
    " |   o  o   | ",
    "  \\   V    /  ",
    "   \\ ###  /   ",
    " (%)=\\___/=(%) ",
    "   | $$$ |  ",
    "   |     |  ",
    "    |_____|   ",
]
BRAWLER_HURT = [
    "   ._______.  ",
    "  / x  x  \\  ",
    " |   O  O   | ",
    "  \\   w    /  ",
    "   \\ ###  /   ",
    " (%)=\\___/=(%) ",
    "   | $$$ |  ",
    "   |     | ",
    "    |_____|   ",
]
BRAWLER_ATTACK = [
    "   ._______.  ",
    "  / -  -  \\  ",
    " |   o  o   | ",
    "  \\   V    /  ",
    "   \\ ###  /   ",
    " <==(%)=\\___/=(%)",
    "   | $$$ |  ",
    "   |     |  ",
    "    |_____|   ",
]

# MAP 3: HEAVYWEIGHT CHAMPION
CHAMP_IDLE = [
    "   .#######.  ",
    "  / [===]  \\  ",
    " |   O   O   | ",
    "  \\   ___   / ",
    "   \\  ---  /  ",
    "[$]==/___\\==[$]",
    "   | ### | ",
    "   |     | ",
    "    |_____|   ",
]
CHAMP_HURT = [
    "   .#######.  ",
    "  / [ X X ]  \\ ",
    " |   o   o   | ",
    "  \\   w   /  ",
    "   \\  ---  /  ",
    "[$]==\\___/==[$]",
    "   | ### |  ",
    "   |     |  ",
    "    |_____|   ",
]
CHAMP_ATTACK = [
    "   .#######.  ",
    "  / [===]  \\  ",
    " |   O   O   | ",
    "  \\   ___   / ",
    "   \\  ---  /  ",
    "<==[$]==/___\\==[$]",
    "   |  ### |  ",
    "   |     |  ",
    "    |_____|   ",
]

MAP_SIDE_ART = {
    1: [
        "|##| /||\\ |##| /||\\ |##|",
        "|##|/ || \\|##|/ || \\|##|",
        "|##| || ||##| || ||##|",
        "|##|\\ || /|##|\\ || /|##|",
        "#PUNCH###TYPE!###PUNCH##",
        "|TYPE!###PUNCH###TYPE!##",
        "|##|/ || \\|##|/ || \\|##|",
        "|(((@@@@@@@@@)))(((@)))|",
        "'--_______----_______--'",
        "|##| /||\\ |##| /||\\ |##|",
        "'--_______----_______--'"
    ],
    2: [
        "==|===|==|===|==|===|==",
        " \\||||//  \\||||//  \\||||// ",
        "  \\||//    \\||//    \\||//  ",
        "   \\\\//     \\\\//     \\\\//  ",
        "    ||       ||       ||   ",
        "   //\\\\     //\\\\     //\\\\  ",
        "  //  \\\\   //  \\\\   //  \\\\ ",
        "  ''  ''   ''  ''   ''  '' ",
        "==|===|==|===|==|===|==",
        " \\||||//  \\||||//  \\||||// ",
        "  ''  ''   ''  ''   ''  '' "
    ],
    3: [
        "+==+==+==++==+==+==++==+",
        "|_ [__] _|| _[__] _|| _|",
        "|/    \\|||/    \\|||/    \\|",
        "||O  O||||O  O|||||O  O||",
        "|\\____/|||\\____/|||\\____/|",
        "| |||| ||| |||| ||| |||| |",
        "|/    \\|||/    \\|||/    \\|",
        "|      ||      ||      ||",
        "+--+--+--++--+--+--++--+",
        "|_ [__] _|| _[__] _|| _|",
        "+--+--+--++--+--+--++--+"
    ]
}

WIDTH = 104
INNER = WIDTH - 2

def draw_main_menu():
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row(f"  GOLD: {gold} [o]"), row()]
    lines += [row(l.center(INNER)) for l in block_text(TITLE)]
    lines += [row(), row(stars), row()]

    buttons = [
        "|  1  [   START   ]  |",
        "+======================+",
        "|  2  [    SHOP   ]  |",
        "+======================+",
        "|  3  [    EXIT   ]  |",
        "+======================+"
    ]
    
    portrait = portrait_box_single("FIGHTER", get_player_frame(False))
    right_margin = 2
    left_w = INNER - BOX_W - 2 - right_margin
    box_left = (left_w - 24) // 2

    for i, p in enumerate(portrait):
        b_str = ""
        if 1 <= i <= len(buttons):
            b_idx = i - 1
            if b_idx < len(buttons):
                b_str = " " * box_left + buttons[b_idx]
        b_str = b_str.ljust(left_w)
        lines.append(row(b_str + p.ljust(BOX_W + 2) + " " * right_margin))

    lines += [row(), row(stars), row("Type 1, 2 or 3 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def portrait_box_single(title="FIGHTER", frame=None):
    if frame is None:
        frame = get_player_frame(False)
    top = "+" + f" {title} ".center(BOX_W, "-") + "+"
    return [top, *["|" + l + "|" for l in frame], "+" + "-" * BOX_W + "+"]

def draw_difficulty_menu():
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row("  SELECT DIFFICULTY".center(INNER)), row(), row(stars), row()]
    lines.append(row("CONTROLS: QWERTY (More letters added on Medium/Hard)".center(INNER)))
    lines.append(row())
    lines.append(row("  1. [ EASY   ] - 500 HP   | 10 DMG".center(INNER)))
    lines.append(row("  2. [ MEDIUM ] - 1000 HP  | 25 DMG".center(INNER)))
    lines.append(row("  3. [ HARD   ] - 1500 HP  | 50 DMG".center(INNER)))
    lines.append(row("  4. [ BACK   ]".center(INNER)))
    lines += [row(), row(stars), row("Type 1, 2, 3 or 4 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def draw_map_menu():
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row("  CHOOSE MAP".center(INNER)), row(), row(stars), row()]
    lines.append(row("  1. [ STREET      ]".center(INNER)))
    m2_status = "" if map2 == 1 else " (LOCKED)"
    lines.append(row(f"  2. [ UNDERGROUND ]{m2_status}".center(INNER)))
    m3_status = "" if map3 == 1 else " (LOCKED)"
    lines.append(row(f"  3. [ BOXING RING ]{m3_status}".center(INNER)))
    lines.append(row("  4. [ BACK        ]".center(INNER)))
    lines += [row(), row(stars), row("Type 1, 2, 3 or 4 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def draw_equipment_menu():
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row("  CHOOSE EQUIPMENTS".center(INNER)), row(), row(stars), row()]
    lines.append(row("  1. [ NO GLOVES     ]".center(INNER)))
    g2_status = "" if a == 1 else " (LOCKED)"
    lines.append(row(f"  2. [ SPIKED GLOVES ]{g2_status}".center(INNER)))
    g3_status = "" if b == 1 else " (LOCKED)"
    lines.append(row(f"  3. [ BOMB GLOVES   ]{g3_status}".center(INNER)))
    g4_status = "" if c == 1 else " (LOCKED)"
    lines.append(row(f"  4. [ LAVA GLOVES   ]{g4_status}".center(INNER)))
    lines.append(row("  5. [ BACK          ]".center(INNER)))
    lines += [row(), row(stars), row("Type 1, 2, 3, 4 or 5 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def draw_shop_menu():
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row(f"  SHOP (GOLD: {gold})".center(INNER)), row(), row(stars), row()]
    s1 = "OWNED" if a == 1 else "2500 G"
    lines.append(row(f"  1. [ SPIKED GLOVES ] - {s1}".center(INNER)))
    lines.append(row("     20% Crit + Berserk Ult".center(INNER)))
    s2 = "OWNED" if b == 1 else "5000 G"
    lines.append(row(f"  2. [ BOMB GLOVES   ] - {s2}".center(INNER)))
    lines.append(row("     +200% Dmg + Bloodlust Ult".center(INNER)))
    s3 = "OWNED" if c == 1 else "10000 G"
    lines.append(row(f"  3. [ LAVA GLOVES   ] - {s3}".center(INNER)))
    lines.append(row("     +150% Dmg + 30% Crit + Lava Ult".center(INNER)))
    lines.append(row("  4. [ BACK          ]".center(INNER)))
    lines += [row(), row(stars), row("Type 1, 2, 3 or 4 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def draw_win_menu(gol, note=""):
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row(f"  GOLD: {gold} [o]"), row()]
    lines += [row(l.center(INNER)) for l in block_text("YOU WIN")]
    lines += [row(), row(stars), row()]
    if note:
        lines += [row(note.center(INNER)), row()]

    buttons = [
        "|  1  [   RETRY   ]  |",
        "+======================+",
        "|  2  [    MENU   ]  |",
        "+======================+"
    ]
    
    portrait = portrait_box_single("WINNER", get_player_frame(False))
    right_margin = 2
    left_w = INNER - BOX_W - 2 - right_margin
    box_left = (left_w - 24) // 2

    stats_line = f"HITS GAVE: {phit}   HITS TAKEN: {ehit}   CRITS: {crits}   GOLD: +{gol}G"

    for i, p in enumerate(portrait):
        b_str = ""
        if i == 0:
            b_str = " " * ((left_w - len(stats_line)) // 2) + stats_line
        elif 2 <= i <= len(buttons) + 1:
            b_idx = i - 2
            if b_idx < len(buttons):
                b_str = " " * box_left + buttons[b_idx]
        b_str = b_str.ljust(left_w)
        lines.append(row(b_str + p.ljust(BOX_W + 2) + " " * right_margin))

    lines += [row(), row(stars), row("Type 1 or 2 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def draw_lose_menu(gol):
    def row(text=""):
        return "|" + text.ljust(INNER)[:INNER] + "|"

    border = "+" + "=" * INNER + "+"
    stars = "*" * INNER

    lines = [border, row(f"  GOLD: {gold} [o]"), row()]
    lines += [row(l.center(INNER)) for l in block_text("YOU LOSE")]
    lines += [row(), row(stars), row()]

    buttons = [
        "|  1  [   RETRY   ]  |",
        "+======================+",
        "|  2  [    MENU   ]  |",
        "+======================+"
    ]
    
    portrait = portrait_box_single("KNOCKED OUT", get_player_frame(False))
    right_margin = 2
    left_w = INNER - BOX_W - 2 - right_margin
    box_left = (left_w - 24) // 2

    stats_line = f"HITS GAVE: {phit}   HITS TAKEN: {ehit}   CRITS: {crits}   GOLD: +{gol}G"

    for i, p in enumerate(portrait):
        b_str = ""
        if i == 0:
            b_str = " " * ((left_w - len(stats_line)) // 2) + stats_line
        elif 2 <= i <= len(buttons) + 1:
            b_idx = i - 2
            if b_idx < len(buttons):
                b_str = " " * box_left + buttons[b_idx]
        b_str = b_str.ljust(left_w)
        lines.append(row(b_str + p.ljust(BOX_W + 2) + " " * right_margin))

    lines += [row(), row(stars), row("Type 1 or 2 and press ENTER".center(INNER)), border]
    return "\n".join(lines)

def run_graphical_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(draw_main_menu())
        try:
            choice = input("INPUT: ").strip()
            if choice == "1":
                tick.play()
                os.system("cls" if os.name == "nt" else "clear")
                return int(choice)
            elif choice == "2":
                select.play()
                os.system("cls" if os.name == "nt" else "clear")
                return int(choice)
            elif choice == "3":
                back.play()
                os.system("cls" if os.name == "nt" else "clear")
                return int(choice)
            elif choice == "110":
                tick.play()
                os.system("cls" if os.name == "nt" else "clear")
                return int(choice)
            else:
                print("INVALID CHOICE. TYPE 1, 2 OR 3.")
                time.sleep(1)
        except (ValueError, EOFError):
            return 3


# --- YOUR ORIGINAL FUNCTIONS (UPDATED WIN/LOSE SCREENS) ---

def retry():
    global gold, gol, gg, x, player, enemy, ult, pdmg, next, map2, map3
    if enemy <= 0:
        win.play()
        if choice2 == 1: gol = 500; gold += 500
        elif choice2 == 2: gol = 800; gold += 800
        elif choice2 == 3: gol = 1000; gold += 1000

        note = ""
        if choice2 == 3:
            if choice4 == 1: map2 = 1; note = "CONGRATULATIONS, YOU'VE UNLOCKED UNDERGROUND MAP"
            elif choice4 == 2: map3 = 1; note = "CONGRATULATIONS, YOU'VE UNLOCKED BOXING RING MAP"
            elif choice4 == 3: note = "CONGRATULATIONS, YOU ARE THE CHAMPION!!!"

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(draw_win_menu(gol, note))
            try:
                lamon = int(input("INPUT: ").strip())
                if lamon in (1, 2):
                    if lamon == 1:
                        tick.play()
                    elif lamon == 2:
                        back.play()
                    break
            except ValueError:
                pass

        match lamon:
            case 1: gg = 1; player = 100; enemy = hp; pdmg = 30
            case 2: x = 1; gg = 0; player = 100; enemy = hp; pdmg = 30; bg.play(-1)

    if player <= 0:
        lose.play()
        if choice2 == 1: gol = 150; gold += 150
        elif choice2 == 2: gol = 300; gold += 300
        elif choice2 == 3: gol = 450; gold += 450
        gold += 50

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(draw_lose_menu(gol))
            try:
                ulit = int(input("INPUT: ").strip())
                if ulit in (1, 2):
                    if ulit == 1:
                        tick.play()
                    elif ulit == 2:
                        back.play()
                    break
            except ValueError:
                pass

        match ulit:
            case 1: gg = 1; player = 100; enemy = hp; pdmg = 30
            case 2: x = 1; gg = 0; player = 100; enemy = hp; pdmg = 30; bg.play(-1)


def shop():
    global a, b, c, gold
    shop = 1
    while shop == 1:
        os.system("cls" if os.name == "nt" else "clear")
        print(draw_shop_menu())
        try: 
            buy_choice = int(input("INPUT: ").strip())
        except ValueError: 
            continue
        os.system("cls" if os.name == "nt" else "clear")
        match buy_choice:
            case 1 | 2 | 3:
                select.play()
                if buy_choice == 1:
                    if gold >= 2500 and a == 0: 
                        buy.play()
                        print("YOU BOUGHT SPIKED GLOVES!")
                        a = 1; gold -= 2500
                    elif a == 1: print("YOU ALREADY HAVE THAT!!")
                    else: print("NOT ENOUGH MONEY")
                elif buy_choice == 2:
                    if gold >= 5000 and b == 0: 
                        buy.play()
                        print("YOU BOUGHT BOMB GLOVES!")
                        b = 1; gold -= 5000
                    elif b == 1: print("YOU ALREADY HAVE THAT!!")
                    else: print("NOT ENOUGH MONEY")
                elif buy_choice == 3:
                    if gold >= 10000 and c == 0: 
                        buy.play()
                        print("YOU BOUGHT LAVA GLOVES!")
                        c = 1; gold -= 10000
                    elif c == 1: print("YOU ALREADY HAVE THAT!!")
                    else: print("NOT ENOUGH MONEY")
                input("Press Enter to continue...")
            case 4:
                back.play()
                return


def gamemenu():
    global x, enemy, hp, dmg, edmg, choice6, choice2, gg, choice4
    gg = 0
    match choice1:
        case 1:
            os.system("cls" if os.name == "nt" else "clear")
            print(draw_difficulty_menu())
            try:
                choice2 = int(input("INPUT: ").strip())
            except ValueError:
                return
            
            if choice2 in (1, 2, 3):
                tick.play()
            elif choice2 == 4:
                back.play()
                return

            os.system("cls" if os.name == "nt" else "clear")
            match choice2:
                case 1:
                    enemy = 500; hp = 500; dmg = 10; edmg = 10
                    mappy = 1
                    while mappy == 1:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(draw_map_menu())
                        try:
                            choice4 = int(input("INPUT: ").strip())
                        except ValueError:
                            continue
                        
                        if choice4 in (1, 2, 3):
                            move.play()
                        elif choice4 == 4:
                            back.play()
                            return

                        os.system("cls" if os.name == "nt" else "clear")
                        repeat = 1
                        while repeat == 1:
                            if choice4 in (1, 2, 3): maps = 1
                            while maps == 1:
                                if choice4 == 1: print("YOU SELECTED STREET"); mapu = 1; mappy = 0; repeat = 0; maps = 0
                                if choice4 == 2:
                                    if map2 == 1: print("YOU SELECTED UNDERGROUND"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                                if choice4 == 3:
                                    if map3 == 1: print("YOU SELECTED BOXING RING"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                            if mapu == 1:
                                gg = 1; x = 0
                                os.system("cls" if os.name == "nt" else "clear")
                                print(draw_equipment_menu())
                                try:
                                    choice6 = int(input("INPUT: ").strip())
                                except ValueError:
                                    continue
                                
                                if choice6 in (1, 2, 3, 4):
                                    select.play()
                                elif choice6 == 5:
                                    back.play()
                                    x = 1; gg = 0; return

                                os.system("cls" if os.name == "nt" else "clear")
                                match choice6:
                                    case 1: print("NO GLOVES"); repeat = 0; mapu = 0
                                    case 2: 
                                        if a == 1: print("YOU EQUIPPED SPIKED GLOVES"); repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 3: 
                                        if b == 1: print("YOU EQUIPPED BOMB GLOVES"); repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 4: 
                                        if c == 1: print("YOU EQUIPPED LAVA GLOVES"); repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 5:
                                        back.play()
                                        x = 1; gg = 0; return

                case 2:
                    enemy = 1000; hp = 1000; dmg = 25; edmg = 25
                    mappy = 1
                    while mappy == 1:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(draw_map_menu())
                        try:
                            choice4 = int(input("INPUT: ").strip())
                        except ValueError:
                            continue
                        
                        if choice4 in (1, 2, 3):
                            move.play()
                        elif choice4 == 4:
                            back.play()
                            return

                        os.system("cls" if os.name == "nt" else "clear")
                        repeat = 1
                        while repeat == 1:
                            if choice4 in (1, 2, 3): maps = 1
                            while maps == 1:
                                if choice4 == 1: print("YOU SELECTED STREET"); mapu = 1; mappy = 0; repeat = 0; maps = 0
                                if choice4 == 2:
                                    if map2 == 1: print("YOU SELECTED UNDERGROUND"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                                if choice4 == 3:
                                    if map3 == 1: print("YOU SELECTED BOXING RING"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                            if mapu == 1:
                                gg = 1; x = 0
                                os.system("cls" if os.name == "nt" else "clear")
                                print(draw_equipment_menu())
                                try:
                                    choice6 = int(input("INPUT: ").strip())
                                except ValueError:
                                    continue
                                
                                if choice6 in (1, 2, 3, 4):
                                    select.play()
                                elif choice6 == 5:
                                    back.play()
                                    gg = 0; x = 1; return

                                os.system("cls" if os.name == "nt" else "clear")
                                match choice6:
                                    case 1: repeat = 0; mapu = 0
                                    case 2: 
                                        if a == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 3: 
                                        if b == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 4: 
                                        if c == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 5:
                                        back.play()
                                        gg = 0; x = 1; return

                case 3:
                    enemy = 1500; hp = 1500; dmg = 50; edmg = 50
                    mappy = 1
                    while mappy == 1:
                        os.system("cls" if os.name == "nt" else "clear")
                        print(draw_map_menu())
                        try:
                            choice4 = int(input("INPUT: ").strip())
                        except ValueError:
                            continue
                        
                        if choice4 in (1, 2, 3):
                            move.play()
                        elif choice4 == 4:
                            back.play()
                            return

                        os.system("cls" if os.name == "nt" else "clear")
                        repeat = 1
                        while repeat == 1:
                            if choice4 in (1, 2, 3): maps = 1
                            while maps == 1:
                                if choice4 == 1: print("YOU SELECTED STREET"); mapu = 1; mappy = 0; repeat = 0; maps = 0
                                if choice4 == 2:
                                    if map2 == 1: print("YOU SELECTED UNDERGROUND"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                                if choice4 == 3:
                                    if map3 == 1: print("YOU SELECTED BOXING RING"); maps = 0; mappy = 0; mapu = 1
                                    else: print("MAP NOT UNLOCKED YET"); maps = 0; repeat = 0; mapu = 0
                            if mapu == 1:
                                gg = 1; x = 0
                                os.system("cls" if os.name == "nt" else "clear")
                                print(draw_equipment_menu())
                                try:
                                    choice6 = int(input("INPUT: ").strip())
                                except ValueError:
                                    continue
                                
                                if choice6 in (1, 2, 3, 4):
                                    select.play()
                                elif choice6 == 5:
                                    back.play()
                                    gg = 0; x = 1; return

                                os.system("cls" if os.name == "nt" else "clear")
                                match choice6:
                                    case 1: repeat = 0; mapu = 0
                                    case 2: 
                                        if a == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 3: 
                                        if b == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 4: 
                                        if c == 1: repeat = 0; mapu = 0
                                        else: mapu = 1; repeat = 1
                                    case 5:
                                        back.play()
                                        gg = 0; x = 1; return


def draw_dual_battle(status_msg, punching=False, enemy_state="idle"):
    os.system("cls" if os.name == "nt" else "clear")
    
    diff_name = "EASY" if choice2 == 1 else ("MEDIUM" if choice2 == 2 else "HARD")
    enemy_names = {1: "STREET THUG", 2: "UNDERGROUND BRAWLER", 3: "HEAVYWEIGHT CHAMPION"}
    e_name = enemy_names.get(choice4, "STREET THUG")
    
    # Outer Border Top
    print("+" + "=" * (WIDTH - 2) + "+")
    
    # Enemy Header Bar
    e_ratio = max(0, min(1, enemy / hp))
    e_bar_len = 25
    e_filled = int(e_bar_len * e_ratio)
    e_bar = "#" * e_filled + "-" * (e_bar_len - e_filled)
    e_line = f" ENEMY: {e_name}   [{e_bar}] {enemy}/{hp} "
    print("|" + e_line.ljust(WIDTH - 2) + "|")
    
    # Subheader Info Line
    sub_line = f" -- {diff_name}   KEYS: {'QWERTY' if choice2==1 else ('QW/ASDF' if choice2==2 else 'ALL')}"
    print("|" + sub_line.ljust(WIDTH - 2) + "|")
    
    side_art = MAP_SIDE_ART.get(choice4, MAP_SIDE_ART[1])
    p_portrait = get_player_frame(punching)
    
    if choice4 == 1:
        raw_e = THUG_ATTACK if enemy_state == "attack" else (THUG_HURT if enemy_state == "hurt" else THUG_IDLE)
    elif choice4 == 2:
        raw_e = BRAWLER_ATTACK if enemy_state == "attack" else (BRAWLER_HURT if enemy_state == "hurt" else BRAWLER_IDLE)
    else:
        raw_e = CHAMP_ATTACK if enemy_state == "attack" else (CHAMP_HURT if enemy_state == "hurt" else CHAMP_IDLE)
        
    e_portrait = [l.center(BOX_W) for l in raw_e]
    
    p_box_top = " PLAYER ".center(BOX_W)
    e_box_top = " ENEMY ".center(BOX_W)
    
    row_top = f" {side_art[0]}  {p_box_top}    {e_box_top}  {side_art[0]} "
    print("|" + row_top.ljust(WIDTH - 2) + "|")
    
    for r in range(len(get_player_frame(False))):
        art_idx = (r + 1) % len(side_art)
        side_piece = side_art[art_idx]
        p_line = p_portrait[r]
        e_line = e_portrait[r]
        row_str = f" {side_piece}   {p_line}      {e_line}   {side_piece} "
        print("|" + row_str.ljust(WIDTH - 2) + "|")
        
    row_bot = f" {side_art[9 % len(side_art)]}    {' ' * BOX_W}        {' ' * BOX_W}    {side_art[9 % len(side_art)]} "
    print("|" + row_bot.ljust(WIDTH - 2) + "|")
    
    # Status Message Line
    print("|" + status_msg.center(WIDTH - 2) + "|")
    
    # Player Stats Bar & ULT Status Indicator
    p_ratio = max(0, min(1, player / 100))
    p_bar_len = 25
    p_filled = int(p_bar_len * p_ratio)
    p_bar = "#" * p_filled + "-" * (p_bar_len - p_filled)
    
    global ult_status_text
    req_ult = 5 if choice6 == 4 else 3
    if ult >= req_ult:
        ult_status_text = "READY!"
    else:
        ult_status_text = f"[{'#' * ult}{'-' * (req_ult - ult)}]"

    p_line = f" PLAYER: GEARLESS JOE   [{p_bar}] {player}/100   ULT:{ult_status_text} (0/3) "
    print("|" + p_line.ljust(WIDTH - 2) + "|")
    
    stats_line = f" HITS GAVE: {phit}  HITS TAKEN: {ehit}  WRONG: {wrong_count}  SLOW: {slow_count}  CRITS: {crits}  LAST: {last_action_text} "
    print("|" + stats_line.ljust(WIDTH - 2) + "|")
    
    prompt_line = f" Press the letter shown before the timer runs out! Wrong key = you get hit."
    print("|" + prompt_line.ljust(WIDTH - 2) + "|")
    
    # Outer Border Bottom
    print("+" + "=" * (WIDTH - 2) + "+")


def fight():
    global player, enemy, ult, gold, phit, ehit, pdamage, pdmg, crits, wrong_count, slow_count, last_action_text
    
    # Stop background music and play bell at the start of every fight
    bg.stop()
    bell.play()
    
    ult = 0; ehit = 0; phit = 0; wrong_count = 0; slow_count = 0; last_action_text = "None"

    while player > 0 and enemy > 0 and gg == 1:
        crit = random.randint(1, 100)

        if choice6 == 1:
            pdamage = 20
            if ult >= 3: 
                ult1.play()
                last_action_text = "ULT: TWIN!"; 
                if ult==3: 
                    roar.play(); 
                    pdamage *= 2

        if choice6 == 2:
            pdamage = 20
            if crit <= 25: 
                pdamage *= 3
                crits += 1
                criit.play()
            if ult >= 3:
                ult2.play() 
                last_action_text = "ULT: BERSERK!";
                if ult==3: roar.play; pdamage *= 2.5; ult = 2
                

        elif choice6 == 3:
            pdamage = 20 * 2
            if ult >= 3: 
                ult3.play()
                last_action_text = "ULT: BLOOD!"; 
                if ult==3: roar.play; pdamage *= 5; ult = 0; player += 5

        elif choice6 == 4:
            pdamage = 20 * 1.5
            if crit <= 30: 
                pdamage = pdmg * 3
                crits += 1
                criit.play()
            if ult >= 5:
                ult4.play() 
                last_action_text = "ULT: LAVA!"; 
                if ult==5: roar.play(); pdmg += 30 * .30; phit += 1; ult = 4

        letter = random.choice("QWERTY")
        letter2 = random.choice("QWERTYASDFGH")
        letter3 = random.choice("QWERTYASDFGHZXCVB")
        
        g = random.choice(["NICE!", "GOOD", "GREAT"])
        
        if choice2 == 1: time_limit = 3.0; target_letter = letter
        elif choice2 == 2: time_limit = 2.0; target_letter = letter2
        else: time_limit = 1.5; target_letter = letter3

        draw_dual_battle(f"PRESS KEY: [ {target_letter} ]  (LIMIT: {time_limit}s)", enemy_state="idle")
        
        start = time.time()
        answer = input("INPUT: ").upper().strip()
        end = time.time()
        duration = end - start

        if enemy <= hp * 0.25: dmg = edmg * 2
        else: dmg = 10 if choice2 == 1 else (25 if choice2 == 2 else 50)

        if duration <= time_limit:
            if answer == target_letter:
                ult += 1
                enemy -= pdamage
                phit += 1
                
                # Play correct input sound effect when the player presses the right key![cite: 15]
                punch.play()
                
                draw_dual_battle(f"{g} - DEAL {pdamage} DMG", punching=True, enemy_state="hurt")
                time.sleep(0.5)
                if not last_action_text.startswith("ULT"): last_action_text = f"+{pdamage}"
            else:
                wrong_count += 1
                player -= dmg
                ehit += 1
                ult = 0
                pdmg = 30
                last_action_text = f"-{dmg} (Wrong)"
                
                denied.play()
                hurt.play()
                
                draw_dual_battle(f"WRONG KEY! YOU GOT HIT! -{dmg}", punching=False, enemy_state="attack")
                time.sleep(0.5)
        else:
            slow_count += 1
            player -= dmg
            ehit += 1
            ult = 0
            pdmg = 30
            last_action_text = f"-{dmg} (Slow)"
            
            denied.play()
            hurt.play()
            
            draw_dual_battle(f"TOO SLOW ({duration:.2f}s)! -{dmg}", punching=False, enemy_state="attack")
            time.sleep(0.5)


if __name__ == "__main__":
    
    while x == 1:
        
        choice1 = run_graphical_menu()
        if choice1 == 2: shop()
        if choice1 == 1:
            gamemenu()
            while gg == 1:
                fight()
                retry()
        if choice1 == 3: print("THANK YOU!"); break
        if choice1 == 110:
            chet.play()
            print("YOU'VE UNLOCKED ALL GLOVES AND MAPS!")
            a = 1; b = 1; c = 1; map2 = 1; map3 = 1