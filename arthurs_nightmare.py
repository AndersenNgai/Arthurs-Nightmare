# Arthur's Nightmare

from random import randrange, choice, shuffle
from time import sleep
import tkinter
tk = tkinter.Tk()
tk.title("Arthur's Nightmare")
tk.resizable(0, 0)
canvas = tkinter.Canvas(tk, width = 965, height = 450, bg = "white", highlightthickness = 0)
canvas.pack()

class Game:

    def __init__(self):
        self.endscreen_active = False
        canvas.create_rectangle(828, 246, 958, 300, fill = "#ff9999")
        self.restart_button_text = canvas.create_text(893, 273, font = ("Times New Roman", 12), text = "Click here to restart")
        self.end_background = canvas.create_rectangle(-2, -2, 967, 452, fill = "#ffffff", state = "hidden")
        self.end_text = canvas.create_text(482, 170, font = ("Times New Roman", 35),
                                             state = "hidden")
        self.replay_text = canvas.create_text(482, 215, font = ("Times New Roman", 20),
                                              text = "Press the spacebar to play again", state = "hidden")

    def reset(self):
        self.deactivate_endscreen()
        Woogle.reset()
        player.goto(entrance)
        Room.reset()
        arthur.reset()
        player.reset()
        canvas.itemconfig(game.restart_button_text, text = "Click here to restart")

    def mainloop(self):
        while True:
            tk.update_idletasks()
            tk.update()
            sleep(0.1)

    def take_turn(self, player_moved = False):
        canvas.itemconfig(player.woogles_text, text = "Woogles: {} / 10".format(player.woogles()))
        player.noise -= 5
        if player.noise < 0:
            player.noise = 0
        arthur.action()
        arthur.random_detector()
        self.check_jumpscare()
        if player_moved and player.previous_room is arthur.room and arthur.previous_room is player.room: # Pass by
            arthur.detector()
            canvas.itemconfig(arthur.room.highlight, fill = "#ff6666")
            tk.update()
            sleep(1)
            if not arthur.show_position:
                canvas.itemconfig(arthur.room.highlight, fill = "")
        # I disabled Arthur being able to move after you move because it's too OP
        # Arthur has a 1 in 13 chance to move a 2nd time after you move
        # if randrange(117) < 11:
            # arthur.action() # c * (9 / 11) = (1 / 13)
            # self.check_jumpscare()

    def check_jumpscare(self):
        if arthur.room is player.room:
            player.lives -= 1
            canvas.itemconfig(arthur.room.highlight, fill = "#ff6666")
            canvas.itemconfig(player.lives_text, text = "Lives: " + str(player.lives))
            tk.update()
            sleep(2)
            if player.lives > 0:
                canvas.itemconfig(arthur.room.highlight, fill = "#99ffbb")
                arthur.room = choice((garage, entrance, foyer) if arthur.room in upstairs else (master_bedroom, bedroom_one))
                if arthur.show_position:
                    canvas.itemconfig(arthur.room.highlight, fill = "#ff6666")
                arthur.destination = None
                for r in Room.rooms:
                    r.absence_frequency = 0
            else:
                self.activate_endscreen(False)

    def activate_endscreen(self, win):
        self.endscreen_active = True
        canvas.itemconfig(self.end_text, text = "You escaped Arthur's house with all 10 Woogles." if win \
                          else "Arthur killed you at {} Woogle{}.".format(player.woogles(), "" if player.woogles() == 1 else "s"))
        canvas.itemconfig(self.end_background, state = "normal")
        canvas.itemconfig(self.end_text, state = "normal")
        canvas.itemconfig(self.replay_text, state = "normal")

    def deactivate_endscreen(self):
        self.endscreen_active = False
        canvas.itemconfig(self.end_background, state = "hidden")
        canvas.itemconfig(self.end_text, state = "hidden")
        canvas.itemconfig(self.replay_text, state = "hidden")

class Room(Game):
    rooms = []

    def __init__(self, name, *highlight_coords, absence_weight = 1):
        self.name = name
        self.x1, self.y1, self.x2, self.y2 = highlight_coords
        self.highlight = canvas.create_rectangle(*highlight_coords)
        self.texts = []
        self.woogles = []
        self.absence_frequency = 0
        self.absence_weight = absence_weight
        self.__class__.rooms.append(self)

    def __repr__(self):
        return "Room('{0.name}')".format(self)

    def __str__(self):
        return self.name

    def _draw_outline(self):
        pass

    def _draw_name(self, x = None, y = None, text = None, size = 20, vertical = False):
        if x is None:
            x = int((self.x1 + self.x2) / 2)
        if y is None:
            y = int((self.y1 + self.y2) / 2)
        if text is None:
            text = self.name
        self.texts.append(canvas.create_text(x, y, font = ("Times New Roman", size), text = text, angle = 90 if vertical else 0))

    @classmethod
    def reset(cls):
        for r in upstairs:
            r.absence_frequency = 0
            canvas.itemconfig(r.highlight, fill = "")
        for r in downstairs:
            r.absence_frequency = 7
            canvas.itemconfig(r.highlight, fill = "")

class Woogle(Game):
    woogles = []

    def __init__(self, number, room, x, y, size): # (x, y) is the center, not the nw corner
        self.number = number
        self.room = room
        room.woogles.append(self)
        self.has_woogle = False
        self.checked = False
        self.__class__.woogles.append(self)
        canvas.create_text(x, y, font = ("Times New Roman", size), text = str(self.number))
        radius = int(size / 2) + 5
        self.circle = canvas.create_oval(x - radius, y - radius, x + radius, y + radius)

    def __repr__(self):
        return "Woogle({0.number}, {0.room})".format(self)

    def __str__(self):
        return "Woogle " + str(self.number)

    @classmethod
    def reset(cls):
        shuffle(cls.woogles)
        for w in cls.woogles[:10]:
            w.has_woogle = True
            w.checked = False
            canvas.itemconfig(w.circle, fill = "")
        for w in cls.woogles[10:]:
            w.has_woogle = False
            w.checked = False
            canvas.itemconfig(w.circle, fill = "")
        cls.woogles.sort(key = lambda w: w.number)

    def check(self):
        "Search this location for any Woogle"
        self.checked = True
        canvas.itemconfig(self.circle, fill = "#000000")
        player.noise += 12 if self.has_woogle else 8

    def uncheck(self):
        "Reverse the check"
        self.checked = False
        canvas.itemconfig(self.circle, fill = "")

class Character(Game):
    
    pass

class Player(Character):

    def __init__(self):
        self.room = entrance
        self.lives = 3
        self.detector_uses = 0
        self.previous_room = None
        canvas.itemconfig(entrance.highlight, fill = "#99ffbb")
        self.lives_text = canvas.create_text(828, 8, font = ("Times New Roman", 12), text = "Lives: 3", anchor = "nw")
        self.woogles_text = canvas.create_text(827, 28, font = ("Times New Roman", 12), text = "Woogles: 0", anchor = "nw")
        self.detector_text = canvas.create_text(828, 48, font = ("Times New Roman", 12), text = "Detector uses: 0 / 20", anchor = "nw")
        canvas.create_text(512, 314, anchor = "nw", font = ("Times New Roman", 10),
                           text = "- Mouse click: Move to an adjacent room or look for Woogles in your current room.")
        canvas.create_text(512, 332, anchor = "nw", font = ("Times New Roman", 10),
                           text = "- Spacebar: Use the Detector to find out where Arthur is (limited uses).")
        canvas.create_text(512, 368, anchor = "nw", font = ("Times New Roman", 10),
                           text = "- To win, find all 10 Woogles, then go to the Garage, Entrance or the Indoor Garden.")
        canvas.create_text(513, 386, anchor = "nw", font = ("Times New Roman", 10),
                           text = "  Once there, click on the same room that you're in, and you escape Arthur's house.")
        canvas.create_text(512, 404, anchor = "nw", font = ("Times New Roman", 10),
                           text = "- Do not let Arthur catch you. If he catches you, he respawns somewhere else.")
        canvas.create_text(513, 422, anchor = "nw", font = ("Times New Roman", 10),
                           text = "  However, if he catches you and you have 0 lives, you die, which is sad.")
        canvas.bind_all("<Button-1>", self.click)
        canvas.bind_all("<KeyPress-space>", self.detector)
        canvas.bind_all("<KeyPress-1>", lambda x: self.check(1, take_turn = True))
        canvas.bind_all("<KeyPress-2>", lambda x: self.check(2, take_turn = True))

    def reset(self):
        self.lives = 3
        self.detector_uses = 0
        self.noise = 0
        self.goto(entrance)
        canvas.itemconfig(self.lives_text, text = "Lives: 3")
        canvas.itemconfig(self.woogles_text, text = "Woogles: 0 / 10")
        canvas.itemconfig(self.detector_text, text = "Detector uses: 0 / 20")

    def click(self, click, take_turn = True):
        if game.endscreen_active:
            return
        x = click.x
        y = click.y
        # Check for the quit button first
        if 828 < x and x < 958 and 246 < y and y < 300:
            if canvas.itemcget(game.restart_button_text, "text") == "Click again to restart":
                return game.reset()
            else:
                canvas.itemconfig(game.restart_button_text, text = "Click again to restart")
        else:
            canvas.itemconfig(game.restart_button_text, text = "Click here to restart")
        for r in Room.rooms:
            if r.x1 < x and x < r.x2 and r.y1 < y and y < r.y2:
                if r is self.room: # Staying in a room
                    self.previous_room = self.room
                    if self.woogles() == 10 and r in (garage, entrance, indoor_garden):
                        return game.activate_endscreen(True)
                    canvas.itemconfig(self.room.highlight, fill = "#99ffbb")
                    if take_turn:
                        game.take_turn(player_moved = False)
                else: # Moving
                    if r in self.room.connecting_rooms:
                        self.goto(r)
                        self.noise += 3
                        if take_turn:
                            game.take_turn(player_moved = True)

    def goto(self, room):
        "Teleport the player to a room"
        self.previous_room = self.room
        canvas.itemconfig(self.room.highlight, fill = "")
        self.room = room
        canvas.itemconfig(self.room.highlight, fill = "#99ffbb")

    def woogles(self):
        "Check how many Woogles the player has"
        return sum(1 for w in Woogle.woogles if w.checked and w.has_woogle)

    def check(self, woogles, take_turn = True):
        "Check x amount of Woogles in the current room"
        to_check = [w for w in self.room.woogles if not w.checked]
        if len(to_check) > woogles:
            to_check = to_check[:woogles]
        if to_check:
            for w in to_check:
                w.check()
            if take_turn:
                game.take_turn()

    def detector(self, evt = None):
        "Detect where Arthur is"
        canvas.itemconfig(game.restart_button_text, text = "Click here to restart")
        if game.endscreen_active:
            return game.reset()
        if self.detector_uses < 20 and canvas.itemcget(arthur.room.highlight, "fill") != "#ff6666":
            self.detector_uses += 1
            canvas.itemconfig(self.detector_text, text = "Detector uses: {} / 20".format(self.detector_uses))
            canvas.itemconfig(arthur.room.highlight, fill = "#ff6666")

class Arthur(Character):
    "Arthur behaves somewhat similar to a regular person"

    def __init__(self):
        self.show_position = False
        self.reset()

    def reset(self):
        self.room = master_bedroom if randrange(2) else upstairs_hallway
        self.previous_room = None
        self.destination = None
        if self.show_position:
            canvas.itemconfig(self.room.highlight, fill = "#ff6666")

    def action(self, allow_rest = True, highlight = None):
        canvas.itemconfig(self.room.highlight, fill = "#99ffbb" if player.room == self.room else "")
        if randrange(11) > (-1 if self.room in (hallway, upstairs_hallway) else 1) or not allow_rest:
            if isinstance(self.destination, Room):
                self.previous_room, self.room = self.room, self.next_room(self.destination)
            else:
                choices = self.room.connecting_rooms[:]
                if len(choices) > 1 and self.previous_room in choices:
                    choices.remove(self.previous_room)
                self.previous_room = self.room
                self.room = choice(choices)
            if self.room is self.destination:
                self.destination = None
            for r in Room.rooms:
                r.absence_frequency += r.absence_weight
            self.room.absence_frequency = 0
            self.random_destination()
        if highlight or (highlight is None and self.show_position):
            canvas.itemconfig(self.room.highlight, fill = "#ff6666")

    def random_destination(self):
        "Arthur is more likely to go to places he has not been to in a while"
        if isinstance(self.destination, Room):
            return
        candidates = [r for r in Room.rooms if r.absence_frequency > 6]
        raw_absence = int(sum(r.absence_frequency for r in candidates))
        if randrange(raw_absence + 1) > 13: # Choose a destination
            self.force_random_destination(candidates)

    def force_random_destination(self, candidates = None):
        "Force Arthur to choose a random destination"
        if candidates is None:
            candidates = Room.rooms
        n = randrange(int(sum(r.absence_frequency for r in candidates)) + 1)
        counter = 0
        for r in candidates:
            counter += r.absence_frequency
            if counter >= n:
                self.destination = r
                return r

    def next_room(self, destination = None):
        "Calculate the next room to a destination"
        if destination is None:
            destination = self.destination
        if destination is None:
            return
        # First, check to see if the room is adjacent
        possible = [r for r in self.room.connecting_rooms if r is not self.previous_room]
        if destination in possible:
            return destination
        mapper = [[r, [self.room]] for r in possible]
        if not mapper:
            return self.previous_room
        returns = set()
        while not returns:
            for n in range(len(mapper)):
                room, previous = mapper.pop(0)
                for c in room.connecting_rooms:
                    previous.append(room)
                    if c is destination:
                        returns.add(previous[1])
                    if c not in previous:
                        mapper.append([c, previous])
            if not len(mapper):
                return self.next_room(self.room)
        counter = 0
        target = randrange(int(sum(r.absence_frequency for r in returns)) + 1)
        for r in returns:
            counter += r.absence_frequency
            if counter >= target:
                return r

    def reset_absences(self):
        "Reset the absences for rooms"
        for r in Room.rooms:
            r.absence_frequency = 0

    def random_detector(self):
        "Arthur can randomly find the player's current location"
        chance = 20 - 80 / (player.noise + 6)
        if chance < 6:
            chance = 6
        if randrange(100) < chance: # The chance of this happening is between 6% and 20%
            self.detector()
            if not randrange(3): # 1 in 3 chance that the player is alerted
                canvas.itemconfig(player.room.highlight, fill = "#ffff99")

    def detector(self):
        "Find out the player's current location"
        self.destination = player.room
        self.reset_absences()

garage = Room("Garage", 15, 15, 500, 150, absence_weight = 2.1)
garage._draw_name(size = 30)
entrance = Room("Entrance", 15, 150, 50, 300, absence_weight = 0.1)
entrance._draw_name(size = 15, vertical = True)
dining_room = Room("Dining Room", 50, 160, 200, 270, absence_weight = 0.1)
dining_room._draw_name(125, 200, "Dining", 18)
dining_room._draw_name(125, 230, "Room", 18)
kitchen = Room("Kitchen", 200, 160, 310, 270, absence_weight = 2)
kitchen._draw_name(size = 20)
canvas.create_rectangle(310, 160, 315, 270, fill = "#000000")
storage_room = storage = Room("Storage", 315, 160, 450, 270, absence_weight = 2.2)
storage._draw_name(size = 20)
hallway = Room("Hallway", 50, 270, 660, 300)
hallway._draw_name(size = 14)
foyer = Room("Foyer", 15, 300, 125, 415, absence_weight = 0.1)
foyer._draw_name(size = 20)
canvas.create_rectangle(50, 300, 125, 305, fill = "#000000")
den = Room("Den", 125, 300, 300, 415, absence_weight = 0.1)
den._draw_name(y = 370)
canvas.create_rectangle(125, 300, 250, 330, fill = "#ffffff")
bathroom = Room("Bathroom", 125, 300, 250, 330, absence_weight = 2)
bathroom._draw_name(size = 10)
canvas.create_rectangle(250, 300, 255, 335, fill = "#000000")
canvas.create_rectangle(125, 330, 250, 335, fill = "#000000")
Room.rooms[-2], Room.rooms[-1] = bathroom, den
indoor_garden = garden = Room("Indoor Garden", 300, 300, 450, 435, absence_weight = 2)
indoor_garden._draw_name(y = 350, text = "Indoor", size = 18)
indoor_garden._draw_name(y = 380, text = "Garden", size = 18)
master_bedroom = Room("Master Bedroom", 510, 15, 660, 120)
master_bedroom._draw_name(y = 55, text = "Master", size = 17)
master_bedroom._draw_name(y = 85, text = "Bedroom", size = 17)
upstairs_hallway = Room("Upstairs Hallway", 660, 15, 690, 300)
upstairs_hallway._draw_name(size = 14, vertical = True)
guest_room = Room("Guest Room", 690, 15, 810, 105, absence_weight = 2.2)
guest_room._draw_name(y = 50, text = "Guest", size = 16)
guest_room._draw_name(y = 75, text = "Room", size = 16)
canvas.create_rectangle(690, 105, 810, 110, fill = "#000000")
bedroom_one = Room("Bedroom #1", 690, 110, 810, 200, absence_weight = 1.1)
bedroom_one._draw_name(size = 16)
connecting_bathroom = Room("Connecting Bathroom", 510, 120, 620, 170, absence_weight = 0.4)
connecting_bathroom._draw_name(y = 135, size = 10, text = "Connecting")
connecting_bathroom._draw_name(y = 150, size = 10, text = "Bathroom")
bedroom_two = Room("Bedroom #2", 510, 170, 660, 260)
bedroom_two._draw_name(size = 16)
upstairs_bathroom = Room("Upstairs Bathroom", 690, 200, 810, 270, absence_weight = 1.1)
upstairs_bathroom._draw_name(y = 225, size = 14, text = "Upstairs")
upstairs_bathroom._draw_name(y = 245, size = 14, text = "Bathroom")
canvas.create_rectangle(505, 308, 967, 452)
canvas.create_line(820, -2, 820, 308)
downstairs = Room.rooms[:10]
upstairs = Room.rooms[10:]

garage.connecting_rooms = [entrance]
entrance.connecting_rooms = [garage, foyer, dining_room, hallway]
dining_room.connecting_rooms = [hallway, entrance, kitchen]
kitchen.connecting_rooms = [hallway, dining_room]
storage.connecting_rooms = [hallway]
hallway.connecting_rooms = [dining_room, kitchen, storage, bathroom, den, indoor_garden, entrance, upstairs_hallway]
foyer.connecting_rooms = [entrance, bathroom, den]
bathroom.connecting_rooms = [hallway, foyer]
den.connecting_rooms = [hallway, foyer, indoor_garden]
indoor_garden.connecting_rooms = [hallway, den]
master_bedroom.connecting_rooms = [connecting_bathroom, upstairs_hallway]
upstairs_hallway.connecting_rooms = [hallway, master_bedroom, bedroom_two, guest_room, bedroom_one, upstairs_bathroom]
guest_room.connecting_rooms = [upstairs_hallway]
bedroom_one.connecting_rooms = [upstairs_bathroom, upstairs_hallway]
connecting_bathroom.connecting_rooms = [master_bedroom, bedroom_two]
bedroom_two.connecting_rooms = [connecting_bathroom, upstairs_hallway]
upstairs_bathroom.connecting_rooms = [bedroom_one, upstairs_hallway]

woogle1 = Woogle(1, garage, 35, 35, 16)
woogle2 = Woogle(2, garage, 67, 35, 16)
woogle3 = Woogle(3, garage, 99, 35, 16)
woogle4 = Woogle(4, garage, 131, 35, 16)
woogle5 = Woogle(5, entrance, 30, 165, 10)
woogle6 = Woogle(6, kitchen, 215, 175, 10)
woogle7 = Woogle(7, kitchen, 240, 175, 10)
woogle8 = Woogle(8, kitchen, 265, 175, 10)
woogle9 = Woogle(9, storage, 330, 175, 10)
woogle10 = Woogle(10, storage, 355, 175, 10)
woogle11 = Woogle(11, storage, 380, 175, 10)
woogle12 = Woogle(12, foyer, 32, 317, 14)
woogle13 = Woogle(13, bathroom, 140, 315, 10)
woogle14 = Woogle(14, den, 142, 352, 10)
woogle15 = Woogle(15, den, 167, 352, 10)
woogle16 = Woogle(16, master_bedroom, 527, 32, 10)
woogle17 = Woogle(17, guest_room, 707, 32, 10)
woogle18 = Woogle(18, bedroom_one, 707, 127, 10)
woogle19 = Woogle(19, bedroom_two, 527, 187, 10)
woogle20 = Woogle(20, upstairs_bathroom, 705, 215, 10)

player = Player()
arthur = Arthur()

def wander_test(times, prnt = True):
    a = arthur.action
    d = {r : 0 for r in Room.rooms}
    for x in range(times):
        a(False)
        d[arthur.room] += 1
    if prnt:
        total = sum(d.values())
        print("Total visits:", total)
        for r, v in d.items():
            percent = str(v / total * 100)
            if len(percent) > 5:
                percent = percent[:5]
            print(r.name, ": ", v, " visits (", percent, "%)", sep = "")
    else:
        return d

def wander_bind(show_position = True):
    arthur.show_position = show_position
    canvas.bind_all("<Button-1>", lambda x: arthur.action(False))
    canvas.bind_all("<KeyPress-space>", lambda x: arthur.action(False))

game = Game()
game.reset()
game.mainloop()
