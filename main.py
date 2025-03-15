import pygame
import random
import time
import sys
import json
import os
from pygame.locals import *
MUSIC_PATH = "/mnt/data/InMotionFromTheSocialNetworkSoundtrack-TrentReznorTrentReznor-3271093.wav"


# Initialize Pygame
try:
    pygame.init()
except pygame.error as e:
    print(f"Pygame initialization failed: {e}")
    sys.exit(1)

# Game Configuration
class GameConfig:
    def __init__(self):
        self.difficulty_settings = {
            "easy": {"time": 120, "mistakes": 10, "stress_factor": 0.4, "bandwidth": 80, "ai_evolve_rate": 0.15},
            "medium": {"time": 90, "mistakes": 7, "stress_factor": 0.7, "bandwidth": 60, "ai_evolve_rate": 0.25},
            "hard": {"time": 60, "mistakes": 5, "stress_factor": 1.0, "bandwidth": 40, "ai_evolve_rate": 0.35}
        }
        self.colors = {
            "WHITE": (255, 255, 255),
            "BLACK": (20, 20, 20),
            "RED": (255, 100, 100),
            "GREEN": (0, 255, 150),
            "BLUE": (100, 200, 255),
            "GRAY": (70, 70, 70),
            "LIGHT_GRAY": (200, 200, 200),
            "ACCENT": (255, 220, 50),
            "PURPLE": (200, 100, 255),
            "DARK_GREEN": (0, 100, 0),
            "DARK_BLUE": (0, 0, 100)
        }
        # Fallback to default font if specified font fails
        try:
            self.FONT = pygame.font.Font(None, 44)
            self.SMALL_FONT = pygame.font.Font(None, 32)
            self.TITLE_FONT = pygame.font.Font(None, 68)
            self.TERM_FONT = pygame.font.Font(None, 36)
        except pygame.error:
            print("Warning: Font not found. Using default.")
            self.FONT = pygame.font.SysFont(None, 44)
            self.SMALL_FONT = pygame.font.SysFont(None, 32)
            self.TITLE_FONT = pygame.font.SysFont(None, 68)
            self.TERM_FONT = pygame.font.SysFont(None, 36)

config = GameConfig()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("CyberHeist: Codebreaker")
actual_width, actual_height = screen.get_size()

# Global Variables
current_difficulty = "medium"
time_limit = config.difficulty_settings[current_difficulty]["time"]
max_mistakes = config.difficulty_settings[current_difficulty]["mistakes"]
stress_factor = config.difficulty_settings[current_difficulty]["stress_factor"]
bandwidth = config.difficulty_settings[current_difficulty]["bandwidth"]
ai_evolve_rate = config.difficulty_settings[current_difficulty]["ai_evolve_rate"]
player_progress = {"mission": 1, "score": 0, "cred": 0, "username": "", "achievements": []}

# Utility Functions
def draw_background():
    screen.fill(config.colors["BLACK"])
    for i in range(0, actual_width, 50):
        pygame.draw.line(screen, config.colors["DARK_GREEN"], (i, 0), (i, actual_height), 1)
    for i in range(0, actual_height, 50):
        pygame.draw.line(screen, config.colors["DARK_GREEN"], (0, i), (actual_width, i), 1)
    pygame.draw.rect(screen, config.colors["GRAY"], (10, 10, actual_width - 20, actual_height - 20), 3)

def draw_button(rect, color, text, hovered=False, locked=False):
    btn_color = config.colors["GRAY"] if locked else (color if not hovered else config.colors["LIGHT_GRAY"])
    shadow_rect = rect.move(5, 5)
    pygame.draw.rect(screen, config.colors["BLACK"], shadow_rect, border_radius=8)
    pygame.draw.rect(screen, btn_color, rect, border_radius=8)
    pygame.draw.rect(screen, config.colors["DARK_BLUE"], rect, 2, border_radius=8)
    text_surface = config.TERM_FONT.render(text, True, config.colors["WHITE"])
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_story_text(messages):
    draw_background()
    story_rect = pygame.Rect(50, 50, actual_width - 100, actual_height - 100)
    pygame.draw.rect(screen, config.colors["GRAY"], story_rect, border_radius=8)
    for i, msg in enumerate(messages):
        color = config.colors["ACCENT"] if i == 0 else config.colors["WHITE"]
        text = config.TERM_FONT.render(msg, True, color)
        screen.blit(text, (70, 70 + i * 50))
    enter_button = pygame.Rect(actual_width // 2 - 120, actual_height - 120, 240, 70)
    draw_button(enter_button, config.colors["GREEN"], "Hit Enter, Ace!")
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:
                waiting = False

def save_progress():
    try:
        with open("progress.json", "w") as f:
            json.dump(player_progress, f)
    except Exception as e:
        print(f"Error saving progress: {e}")

def load_progress():
    try:
        if os.path.exists("progress.json"):
            with open("progress.json", "r") as f:
                loaded_progress = json.load(f)
                if not isinstance(loaded_progress, dict):
                    raise ValueError("Invalid progress data")
                defaults = {"mission": 1, "score": 0, "cred": 0, "username": "", "achievements": []}
                return {**defaults, **loaded_progress}
        else:
            print("No progress file found. Starting fresh.")
            return player_progress
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error loading progress: {e}. Starting fresh.")
        return player_progress

# AI and Filesystem
class SysDefender:
    def __init__(self, difficulty):
        self.alert_level = 0
        self.difficulty = difficulty
        self.filesystem = {
            "/net": ["scan.dat", "ping.log"],
            "/grid": ["map.bin", "access.txt"],
            "/vault": ["data.zip", "keylog.txt"],
            "/core": ["auth.sys", "virus.exe"],
            "/hub": ["control.sh", "backdoor.key"]
        }
        self.defenses = {"ports": [80, 443, 8080], "dirs": ["/open", "/hidden"], "passwords": ["codeX", "breaker99"]}
        self.taunts = [
            "Nice try, script kiddie—too slow!",
            "I see you... but you don’t see me!",
            "This firewall’s got your number!",
            "[VORTEX] Catch up, scrub!"
        ]

    def react(self, command, mission):
        self.alert_level += random.uniform(0.2, 0.4) * self.difficulty
        if self.alert_level > 0.7 and random.random() < stress_factor:
            if mission == 1 and self.defenses["ports"]:
                self.defenses["ports"].append(random.randint(1000, 9999))
                return random.choice(self.taunts) + " Added a decoy port!"
            elif mission == 2:
                self.defenses["dirs"] = ["/trap"]
                return random.choice(self.taunts) + " Directory rerouted!"
            elif mission == 3 and "data.zip" in self.filesystem["/vault"]:
                self.filesystem["/vault"] = ["locked.zip"]
                return "[VORTEX] Data’s locked—deal with it!"
            elif mission == 4:
                self.defenses["passwords"].append(f"fake{random.randint(100, 999)}")
                return random.choice(self.taunts) + " Password scrambled!"
            elif mission == 5 and "backdoor.key" in self.filesystem["/hub"]:
                self.filesystem["/hub"] = ["vortex.trace"]
                return "[VORTEX] Flipped the script—hub’s mine!"
        return None

    def evolve(self):
        if random.random() < ai_evolve_rate:
            self.alert_level += 0.15
            return "[SYSDEFENDER] Rerouting traffic—keep up!" if random.random() < 0.5 else "[SYSDEFENDER] Your bandwidth’s a joke!"

def generate_mission_challenge(mission):
    missions = {
        1: {
            "desc": "Ping the Network",
            "objective": "Crack the entry code by scanning ports.",
            "task": "List /net, read scan.dat, ping and scan",
            "correct_sequence": ["ls /net", "cat scan.dat", "ping 80", "nmap -p 443"],
            "bandwidth_cost": 10,
            "steps": 4,
            "briefing": [
                "[MISSION 1: Ping the Network]",
                "Objective: Crack NexTech’s grid like a ghost.",
                "Intel: SysDefender’s sloppy—ports are open season.",
                "Steps:",
                "- 'ls /net' to scan the turf.",
                "- 'cat scan.dat' for the port scoop.",
                "- 'ping 80' to test the pulse.",
                "- 'nmap -p 443' to slip inside.",
                "Cred Tip: Speed’s your cred ticket!"
            ]
        },
        2: {
            "desc": "Race the Grid",
            "objective": "Outpace Vortex to map the servers.",
            "task": "List /grid, read map.bin, race to dirs",
            "correct_sequence": ["ls /grid", "cat map.bin", "curl /open", "curl /hidden"],
            "bandwidth_cost": 15,
            "steps": 4,
            "briefing": [
                "[MISSION 2: Race the Grid]",
                "Objective: Beat Vortex to the server map.",
                "Intel: That punk’s fast—dirs are your shot.",
                "Steps:",
                "- 'ls /grid' to eyeball the loot.",
                "- 'cat map.bin' for dir intel.",
                "- 'curl /open' to poke the grid.",
                "- 'curl /hidden' to flex on Vortex.",
                "Cred Tip: Clock him for bonus cred!"
            ]
        },
        3: {
            "desc": "Vault Heist",
            "objective": "Steal NexTech’s data stash.",
            "task": "List /vault, read keylog.txt, grab and dodge",
            "correct_sequence": ["ls /vault", "cat keylog.txt", "grab data.zip", "dodge trap"],
            "bandwidth_cost": 20,
            "steps": 4,
            "briefing": [
                "[MISSION 3: Vault Heist]",
                "Objective: Snag NexTech’s stash before it’s gone.",
                "Intel: Vortex laid traps—stay sharp!",
                "Steps:",
                "- 'ls /vault' to scope the haul.",
                "- 'cat keylog.txt' for the play.",
                "- 'grab data.zip' to swipe it.",
                "- 'dodge trap' to ghost out.",
                "Cred Tip: Clean run, fat cred!"
            ]
        },
        4: {
            "desc": "Core Clash",
            "objective": "Plant a virus in the core.",
            "task": "List /core, read auth.sys, auth and plant",
            "correct_sequence": ["ls /core", "cat auth.sys", "auth codeX", "plant virus.exe"],
            "bandwidth_cost": 15,
            "steps": 4,
            "briefing": [
                "[MISSION 4: Core Clash]",
                "Objective: Drop a virus on NexTech’s core.",
                "Intel: SysDefender’s got eyes—auth’s tight.",
                "Steps:",
                "- 'ls /core' to map it out.",
                "- 'cat auth.sys' for the key.",
                "- 'auth codeX' to breach it.",
                "- 'plant virus.exe' to burn it down.",
                "Cred Tip: Style nets you cred!"
            ]
        },
        5: {
            "desc": "Backdoor Blitz",
            "objective": "Own NexTech with a backdoor.",
            "task": "List /hub, read control.sh, spoof and lock",
            "correct_sequence": ["ls /hub", "cat control.sh", "spoof vortex@nextech.com", "lock backdoor.key"],
            "bandwidth_cost": 25,
            "steps": 4,
            "briefing": [
                "[MISSION 5: Backdoor Blitz]",
                "Objective: Lock NexTech down and punk Vortex.",
                "Intel: Endgame—make it legendary!",
                "Steps:",
                "- 'ls /hub' to nab the key.",
                "- 'cat control.sh' for the hack.",
                "- 'spoof vortex@nextech.com' to flex.",
                "- 'lock backdoor.key' to own it.",
                "Cred Tip: Max cred for the win!"
            ]
        }
    }
    return missions.get(mission, missions[1])

# Storyline
def storyline():
    intro = [
        "[Codebreaker’s Call]",
        "You’re the slickest shadow in the net—NexTech’s your turf.",
        "SysDefender’s their smug AI gatekeeper. Vortex is the rival punk sniffing your trail.",
        "Time to outhack ‘em both—start with a ping and burn the grid down!",
        "Let’s roll, ace!"
    ]
    draw_story_text(intro)

# Game Elements
def front_page():
    while True:
        draw_background()
        title = config.TITLE_FONT.render("CyberHeist: Codebreaker", True, config.colors["ACCENT"])
        subtitle = config.SMALL_FONT.render("Hack Hard, Win Big!", True, config.colors["WHITE"])
        play_button = pygame.Rect(actual_width // 2 - 140, actual_height // 2 + 40, 280, 80)
        mouse_pos = pygame.mouse.get_pos()
        hovered = play_button.collidepoint(mouse_pos)
        screen.blit(title, (actual_width // 2 - title.get_width() // 2, actual_height // 3 - 30))
        screen.blit(subtitle, (actual_width // 2 - subtitle.get_width() // 2, actual_height // 2))
        draw_button(play_button, config.colors["GREEN"], "Hack In", hovered)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and play_button.collidepoint(event.pos):
                return

def main_menu():
    global player_progress
    player_progress = load_progress()
    buttons = [
        {"text": "Missions", "color": config.colors["GREEN"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 - 110, 360, 80)},
        {"text": "Difficulty", "color": config.colors["BLUE"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 - 20, 360, 80)},
        {"text": "Cred", "color": config.colors["PURPLE"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 + 70, 360, 80)},
        {"text": "Exit", "color": config.colors["RED"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 + 160, 360, 80)},
    ]
    while True:
        draw_background()
        title = config.TITLE_FONT.render("Codebreaker HQ", True, config.colors["ACCENT"])
        mission_num = player_progress.get("mission", 1)
        cred = player_progress.get("cred", 0)
        progress_text = config.SMALL_FONT.render(f"Mission: {mission_num} | Cred: {cred}", True, config.colors["WHITE"])
        screen.blit(title, (actual_width // 2 - title.get_width() // 2, actual_height // 4 - 40))
        screen.blit(progress_text, (actual_width // 2 - progress_text.get_width() // 2, actual_height // 3 + 20))
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            hovered = button["rect"].collidepoint(mouse_pos)
            draw_button(button["rect"], button["color"], button["text"], hovered)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if buttons[0]["rect"].collidepoint(event.pos):
                    storyline()
                    if not player_progress["username"]:
                        player_progress["username"] = get_username()
                    mission_selection()
                elif buttons[1]["rect"].collidepoint(event.pos):
                    difficulty_selection()
                elif buttons[2]["rect"].collidepoint(event.pos):
                    display_cred()
                elif buttons[3]["rect"].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def get_username():
    username = ""
    input_active = True
    while input_active:
        draw_background()
        pygame.draw.rect(screen, config.colors["GRAY"], (actual_width // 4, actual_height // 2 - 100, actual_width // 2, 200), border_radius=8)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and username:
                    input_active = False
                elif event.key == K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        prompt = config.FONT.render("Your Hacker Tag:", True, config.colors["WHITE"])
        input_text = config.TERM_FONT.render(username, True, config.colors["GREEN"])
        tip = config.SMALL_FONT.render("Enter to lock it in!", True, config.colors["LIGHT_GRAY"])
        screen.blit(prompt, (actual_width // 4 + 20, actual_height // 2 - 70))
        screen.blit(input_text, (actual_width // 4 + 20, actual_height // 2 - 20))
        screen.blit(tip, (actual_width // 4 + 20, actual_height // 2 + 40))
        pygame.display.update()
    return username

def difficulty_selection():
    global time_limit, max_mistakes, current_difficulty, stress_factor, bandwidth, ai_evolve_rate
    buttons = [
        {"text": "Script Kiddie", "color": config.colors["GREEN"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 - 110, 360, 80), "difficulty": "easy"},
        {"text": "Code Cracker", "color": config.colors["BLUE"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 - 20, 360, 80), "difficulty": "medium"},
        {"text": "Hack Master", "color": config.colors["RED"], "rect": pygame.Rect(actual_width // 2 - 180, actual_height // 2 + 70, 360, 80), "difficulty": "hard"},
    ]
    while True:
        draw_background()
        title = config.FONT.render("Pick Your Game", True, config.colors["ACCENT"])
        screen.blit(title, (actual_width // 2 - title.get_width() // 2, actual_height // 4))
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            hovered = button["rect"].collidepoint(mouse_pos)
            draw_button(button["rect"], button["color"], button["text"], hovered)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        current_difficulty = button["difficulty"]
                        time_limit = config.difficulty_settings[current_difficulty]["time"]
                        max_mistakes = config.difficulty_settings[current_difficulty]["mistakes"]
                        stress_factor = config.difficulty_settings[current_difficulty]["stress_factor"]
                        bandwidth = config.difficulty_settings[current_difficulty]["bandwidth"]
                        ai_evolve_rate = config.difficulty_settings[current_difficulty]["ai_evolve_rate"]
                        return

def mission_selection():
    buttons = [
        {"text": "1: Ping the Network", "rect": pygame.Rect(150, 220, 340, 70), "mission": 1},
        {"text": "2: Race the Grid", "rect": pygame.Rect(150, 300, 340, 70), "mission": 2},
        {"text": "3: Vault Heist", "rect": pygame.Rect(150, 380, 340, 70), "mission": 3},
        {"text": "4: Core Clash", "rect": pygame.Rect(150, 460, 340, 70), "mission": 4},
        {"text": "5: Backdoor Blitz", "rect": pygame.Rect(150, 540, 340, 70), "mission": 5},
    ]
    back_rect = pygame.Rect(50, 50, 160, 70)
    while True:
        draw_background()
        title = config.FONT.render("Mission Drop", True, config.colors["ACCENT"])
        screen.blit(title, (actual_width // 2 - title.get_width() // 2, 120))
        mouse_pos = pygame.mouse.get_pos()
        hovered = back_rect.collidepoint(mouse_pos)
        draw_button(back_rect, config.colors["BLUE"], "Back", hovered)
        for button in buttons:
            locked = button["mission"] > player_progress["mission"]
            hovered = button["rect"].collidepoint(mouse_pos)
            draw_button(button["rect"], config.colors["GREEN"], button["text"], hovered, locked)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    return
                for button in buttons:
                    if button["rect"].collidepoint(event.pos) and button["mission"] <= player_progress["mission"]:
                        mission_challenge(button["mission"])

def mission_challenge(mission):
    challenge = generate_mission_challenge(mission)
    draw_story_text(challenge["briefing"])
    sys_defender = SysDefender(stress_factor)
    score = 100
    cred = 0
    mistakes = 0
    current_bandwidth = bandwidth
    start_time = time.time()
    stress_event = False
    stress_timer = random.randint(10, 25)
    completed_steps = 0
    typed_command = ""
    log_messages = ["[SYS] You’re jacked in—move fast!"]
    command_history = []
    history_index = -1
    cursor_visible = True
    cursor_timer = 0
    bandwidth_deplete_timer = 0
    random_event = random.randint(20, 40)

    while True:
        draw_background()
        pygame.draw.rect(screen, config.colors["GRAY"], (20, 20, actual_width - 40, actual_height - 40), border_radius=8)

        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, time_limit - elapsed_time)

        # Bandwidth depletion
        bandwidth_deplete_timer += 1
        if bandwidth_deplete_timer >= 25:
            current_bandwidth -= 1
            bandwidth_deplete_timer = 0
            if current_bandwidth <= 0:
                game_over("Bandwidth’s toast—you’re out!")
                return

        # AI and Vortex events
        evolve_msg = sys_defender.evolve()
        if evolve_msg:
            log_messages.append(f"{evolve_msg}")
        if elapsed_time >= stress_timer and not stress_event:
            stress_event = True
            alert = sys_defender.react(typed_command, mission)
            if alert:
                log_messages.append(f"{alert}")
                score -= 10
        if elapsed_time == random_event:
            event = random.choice(["Bandwidth spike!", "[VORTEX] You’re slipping, ace!", "Cred stash found!"])
            log_messages.append(f"[EVENT] {event}")
            if event == "Bandwidth spike!":
                current_bandwidth += 20
            elif event == "Cred stash found!":
                cred += 50

        # UI Elements
        title = config.FONT.render(challenge["desc"], True, config.colors["ACCENT"])
        objective = config.TERM_FONT.render(f"Objective: {challenge['objective']}", True, config.colors["WHITE"])
        stats = config.SMALL_FONT.render(f"Score: {score} | Cred: {cred} | Time: {remaining_time}s | BW: {current_bandwidth}", True, config.colors["WHITE"])
        controls = config.SMALL_FONT.render("ESC: Bail | Enter: Run | ↑↓: History | ?: Recap", True, config.colors["LIGHT_GRAY"])
        screen.blit(title, (40, 40))
        screen.blit(objective, (40, 100))
        screen.blit(stats, (40, actual_height - 80))
        screen.blit(controls, (40, actual_height - 50))

        # Command input with blinking cursor
        pygame.draw.rect(screen, config.colors["BLACK"], (40, 160, actual_width - 80, 60), border_radius=5)
        command_surface = config.TERM_FONT.render(f"$ {typed_command}", True, config.colors["GREEN"])
        screen.blit(command_surface, (50, 170))
        cursor_timer += 1
        if cursor_timer >= 15:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        if cursor_visible:
            cursor_x = 50 + command_surface.get_width()
            pygame.draw.line(screen, config.colors["GREEN"], (cursor_x, 170), (cursor_x, 200), 3)

        # Log window
        pygame.draw.rect(screen, config.colors["BLACK"], (actual_width - 360, 160, 320, actual_height - 240), border_radius=5)
        for i, msg in enumerate(log_messages[-7:]):
            screen.blit(config.SMALL_FONT.render(msg, True, config.colors["WHITE"]), (actual_width - 350, 170 + i * 40))

        # Status panel
        pygame.draw.rect(screen, config.colors["BLACK"], (40, 230, 320, 160), border_radius=5)
        status_text = [
            f"Ports: {', '.join(map(str, sys_defender.defenses['ports']))}",
            f"Dirs: {', '.join(sys_defender.defenses['dirs'])}",
            f"Alert: {int(sys_defender.alert_level * 100)}%"
        ]
        for i, line in enumerate(status_text):
            screen.blit(config.SMALL_FONT.render(line, True, config.colors["WHITE"]), (50, 240 + i * 45))

        # Mission Recap panel
        pygame.draw.rect(screen, config.colors["BLACK"], (380, 230, actual_width - 760, 160), border_radius=5)
        recap_text = ["Next Move:", challenge["task"].split(", ")[completed_steps], f"Steps: {completed_steps}/{challenge['steps']}"]
        for i, line in enumerate(recap_text):
            screen.blit(config.SMALL_FONT.render(line, True, config.colors["LIGHT_GRAY"]), (390, 240 + i * 45))

        # Bandwidth progress bar
        pygame.draw.rect(screen, config.colors["DARK_GREEN"], (40, actual_height - 100, 300, 20), border_radius=5)
        bw_percentage = current_bandwidth / bandwidth
        pygame.draw.rect(screen, config.colors["GREEN"], (40, actual_height - 100, 300 * bw_percentage, 20), border_radius=5)

        pygame.display.update()

        # Win/Lose Conditions
        if mistakes >= max_mistakes:
            game_over("SysDefender smoked you—retry!")
            return
        if completed_steps >= challenge["steps"]:
            player_progress["mission"] = max(player_progress["mission"], mission + 1)
            player_progress["score"] += score
            player_progress["cred"] += cred + (remaining_time * 2)
            if mission == 1 and "Ping Pro" not in player_progress["achievements"]:
                player_progress["achievements"].append("Ping Pro")
                log_messages.append("[CRED] Ping Pro earned—50 cred!")
                player_progress["cred"] += 50
            if mission == 5:
                show_finale()
            save_progress()
            if check_high_score(player_progress["username"], player_progress["score"]):
                display_leaderboard()
            else:
                show_result(score, cred)
            return
        if remaining_time == 0:
            game_over("Time’s up—NexTech’s laughing!")
            return

        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    typed_command = typed_command[:-1]
                elif event.key == K_RETURN and typed_command:
                    if current_bandwidth >= challenge["bandwidth_cost"]:
                        current_bandwidth -= challenge["bandwidth_cost"]
                        command_history.append(typed_command)
                        log_messages.append(f"$ {typed_command}")
                        # Flexible command parsing
                        cmd = ' '.join(typed_command.strip().lower().split())
                        correct_cmd = ' '.join(challenge["correct_sequence"][completed_steps].strip().lower().split())
                        if cmd == correct_cmd:
                            completed_steps += 1
                            log_messages.append(f"[+] Step {completed_steps}—you’re in deep!")
                            score += 25
                            cred += 10
                        else:
                            mistakes += 1
                            score -= 10
                            log_messages.append("[-] Wrong move—SysDefender’s on you!")
                        typed_command = ""
                        history_index = -1
                    else:
                        log_messages.append("[-] Bandwidth’s dry—hold up!")
                elif event.key == K_UP and command_history:
                    history_index = min(history_index + 1, len(command_history) - 1)
                    typed_command = command_history[len(command_history) - 1 - history_index]
                elif event.key == K_DOWN and command_history:
                    history_index = max(history_index - 1, -1)
                    typed_command = command_history[len(command_history) - 1 - history_index] if history_index >= 0 else ""
                elif event.key == K_SLASH:  # "?" key
                    log_messages.append(f"[RECAP] {challenge['task']}")
                else:
                    typed_command += event.unicode

def game_over(message):
    draw_background()
    pygame.draw.rect(screen, config.colors["RED"], (actual_width // 4, actual_height // 2 - 60, actual_width // 2, 120), border_radius=8)
    text = config.FONT.render(message, True, config.colors["WHITE"])
    screen.blit(text, (actual_width // 2 - text.get_width() // 2, actual_height // 2 - 20))
    pygame.display.update()
    time.sleep(3)

def show_result(score, cred):
    draw_background()
    pygame.draw.rect(screen, config.colors["GREEN"], (actual_width // 4, actual_height // 2 - 60, actual_width // 2, 120), border_radius=8)
    text1 = config.FONT.render(f"Hack Win! Score: {score}", True, config.colors["WHITE"])
    text2 = config.SMALL_FONT.render(f"Cred: {cred}", True, config.colors["WHITE"])
    screen.blit(text1, (actual_width // 2 - text1.get_width() // 2, actual_height // 2 - 40))
    screen.blit(text2, (actual_width // 2 - text2.get_width() // 2, actual_height // 2 + 10))
    pygame.display.update()
    time.sleep(3)

def show_finale():
    finale = [
        "[HACKER’S ENDGAME]",
        "NexTech’s fried—backdoor’s locked, Vortex is toast!",
        "You’re the grid’s kingpin—cred’s overflowing.",
        "SysDefender’s offline, and the net’s yours.",
        "Cash out, Codebreaker—you’re legend!"
    ]
    draw_story_text(finale)

def check_high_score(username, score):
    progress = load_progress()
    if progress and progress["username"] == username:
        return score > progress["score"]
    return score > 150

def display_leaderboard():
    draw_background()
    pygame.draw.rect(screen, config.colors["BLUE"], (actual_width // 4, actual_height // 2 - 60, actual_width // 2, 120), border_radius=8)
    text = config.FONT.render(f"Top Score: {player_progress['score']}", True, config.colors["WHITE"])
    screen.blit(text, (actual_width // 2 - text.get_width() // 2, actual_height // 2 - 20))
    pygame.display.update()
    time.sleep(3)

def display_cred():
    draw_background()
    pygame.draw.rect(screen, config.colors["PURPLE"], (actual_width // 4, actual_height // 2 - 60, actual_width // 2, 120), border_radius=8)
    text1 = config.FONT.render(f"Hacker Cred: {player_progress['cred']}", True, config.colors["WHITE"])
    text2 = config.SMALL_FONT.render("Hit the dark web for upgrades!", True, config.colors["WHITE"])
    screen.blit(text1, (actual_width // 2 - text1.get_width() // 2, actual_height // 2 - 40))
    screen.blit(text2, (actual_width // 2 - text2.get_width() // 2, actual_height // 2 + 10))
    pygame.display.update()
    time.sleep(3)

if __name__ == "__main__":
    front_page()
    main_menu()
make
