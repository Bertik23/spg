from tkinter import Tk, Canvas
from random import randint, choice

fire_rate = 5


def positiveOrNegative(n):
    if n == 0:
        return 0
    elif n < 0:
        return -1
    else:
        return 1


class Empty():
    pass


class Player:
    def __init__(self, up, down, left, right):
        self.x, self.y = 500, 350
        self.size = 20
        self.speed = 10
        self.look = canvas.create_oval(self.x-self.size, self.y-self.size,
                                       self.x+self.size, self.y+self.size,
                                       fill="red")
        self.up, self.down, self.left, self.right = up, down, left, right
        self.shooting = False
        self.move()
        self.shoot()

    def move(self):
        for powerup in powerups:
            if ((self.x-powerup.x)**2
                    + (self.y-powerup.y)**2) <= (self.size+powerup.size)**2:
                powerup.use()
        if self.up in pressedKeys:
            self.y -= self.speed
        if self.down in pressedKeys:
            self.y += self.speed
        if self.left in pressedKeys:
            self.x -= self.speed
        if self.right in pressedKeys:
            self.x += self.speed

        self.x = max(min(self.x, canvas.winfo_width()), 0)
        self.y = max(min(self.y, canvas.winfo_height()), 0)

        canvas.coords(self.look, self.x-self.size, self.y-self.size,
                      self.x+self.size, self.y+self.size)
        window.after(10, self.move)

    def shoot(self):
        if self.shooting:
            x = mouse.x-self.x
            y = mouse.y-self.y
            z = (x**2+y**2)**0.5
            dx = x/z * 30
            dy = y/z * 30
            shots.append(Shot(self.x, self.y, dx, dy))

        window.after(1000//fire_rate, self.shoot)

    def toggleShooting(self, e):
        mouse.x, mouse.y = e.x, e.y
        self.shooting = not self.shooting


class Zombie:
    def __init__(self):
        side = randint(0, 3)
        if side < 2:
            if side == 0:
                self.x = -20
            else:
                self.x = 1020
            self.y = randint(0, 700)
        elif side >= 2:
            if side == 2:
                self.y = -20
            else:
                self.y = 720
            self.x = randint(0, 1000)
        self.size = 20
        self.speed = 5
        self.maxHealth = 50
        self.health = 50
        self.look = canvas.create_rectangle(self.x-self.size, self.y-self.size,
                                            self.x+self.size, self.y+self.size,
                                            fill="green")
        self.healthbarBase = canvas.create_rectangle(self.x-self.size,
                                                     self.y-10-self.size,
                                                     self.x+self.size,
                                                     self.y-5-self.size,
                                                     fill="red")
        self.healthbar = canvas.create_rectangle(self.x-self.size,
                                                 self.y-10-self.size,
                                                 self.x+self.size,
                                                 self.y-5-self.size,
                                                 fill="green")
        self.move()

    def move(self):
        if self.health <= 0:
            zombies.remove(self)
            return
        self.x += (positiveOrNegative(player.x-self.x)*self.speed
                   + randint(-3, 3))
        self.y += (positiveOrNegative(player.y-self.y)*self.speed
                   + randint(-3, 3))
        canvas.coords(self.look, self.x-self.size, self.y-self.size,
                      self.x+self.size, self.y+self.size)
        canvas.coords(self.healthbarBase,
                      self.x-self.size,
                      self.y-10-self.size,
                      self.x+self.size,
                      self.y-5-self.size)
        canvas.coords(self.healthbar,
                      self.x-self.size,
                      self.y-10-self.size,
                      self.x-self.size
                      + (2*self.size*self.health/self.maxHealth),
                      self.y-5-self.size)
        window.after(10, self.move)

    def __del__(self):
        canvas.delete(self.look, self.healthbar, self.healthbarBase)


class Shot:
    def __init__(self, x, y, dx, dy):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.look = canvas.create_line(x, y, x+dy*10, y+dy*10)
        self.move()

    def move(self):
        remove = False
        for zombie in zombies:
            if (zombie.x-zombie.size < self.x < zombie.x+zombie.size and
                    zombie.y-zombie.size < self.x < zombie.y+zombie.size):
                zombie.health -= 10
                remove = True
        self.x += self.dx
        self.y += self.dy
        canvas.coords(self.look, self.x, self.y,
                      self.x+self.dx*10, self.y+self.dy*10)
        if not 0 < self.x < 1000 or not 0 < self.y < 700 or remove:
            shots.remove(self)
            return
        window.after(10, self.move)

    def __del__(self):
        canvas.delete(self.look)


class PowerUp:
    def __init__(self, color):
        self.x, self.y = randint(0, 1000), randint(0, 700)
        self.size = 5
        self.look = canvas.create_oval(self.x-self.size,
                                       self.y-self.size,
                                       self.x+self.size,
                                       self.y+self.size,
                                       fill=color)

    def use(self):
        self.used()
        newPowerUp()
        powerups.remove(self)

    def used():
        pass

    def __del__(self):
        canvas.delete(self.look)


class SpeedPowerUp(PowerUp):
    def __init__(self):
        super().__init__("orange")

    def used(self):
        player.speed += 10
        window.after(10000,
                     lambda: setattr(player, "speed", player.speed - 10))


class MinigunPowerUp(PowerUp):
    def __init__(self):
        super().__init__("magenta")

    def used(self):
        global fire_rate
        fire_rate += 50
        window.after(5000,
                     lambda: exec("global fire_rate; fire_rate -= 50"))


def newZombie(n):
    for i in range(n):
        zombies.append(Zombie())


def newPowerUp():
    powerups.append(choice([SpeedPowerUp(), MinigunPowerUp()]))


powerups = []
pressedKeys = []
zombies = []
shots = []
window = Tk()
window.title("Zombie Hra")
canvas = Canvas(window, width=1000, height=700)
canvas.pack()
player = Player("w", "s", "a", "d")
mouse = Empty()
mouse.x = 0
mouse.y = 0


newZombie(2)

for i in range(2):
    newPowerUp()


window.bind("<KeyPress>", lambda e: [pressedKeys.append(e.keysym)]
            if e.keysym not in pressedKeys else None)
window.bind("<KeyRelease>", lambda e: [pressedKeys.remove(e.keysym)]
            if e.keysym in pressedKeys else None)
window.bind("<ButtonPress-1>", player.toggleShooting)
window.bind("<ButtonRelease-1>", player.toggleShooting)
window.bind("<Motion>", lambda e: [setattr(mouse, "x", e.x),
            setattr(mouse, "y", e.y)])


def printKeys():
    print(pressedKeys)


window.mainloop()
