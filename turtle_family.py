import turtle
import time
import random

class Snake():
    
    def __init__(self):
        self.screen = self.game_screen()
        self.pointer = self.create_pointer()
        self.pointer_body = []
        self.food = self.create_food()
        self._score = 0
        self._highest_score = 0
        self.points = self.points()
        self.dev = self.dev_by()
        self.update_points()
        self._direction = None
        self._delay = 0.01
        self.screen.listen()
        self.draw_bounds()
        self.positions = []
        self.headings = []
        self.follow_distance = 12
        self.last_move_time = time.time()
        self.move_interval = 0.08
        self.screen.onkeypress(self.arriba, "w")
        self.screen.onkeypress(self.abajo, "s")
        self.screen.onkeypress(self.izquierda, "a")
        self.screen.onkeypress(self.derecha, "d")

    def random_int(self):
        return random.randint(-192, 192)

    def new_highest(self):
        if self._score > self._highest_score:
            self._highest_score = self._score

    def game_screen(self):
        screen = turtle.Screen()
        screen.title("Tortugas")
        screen.bgcolor("#B3DBC5")
        screen.setup(width=500, height=500)
        screen.tracer(0)
        return screen

    def create_pointer(self):
        pointer = turtle.Turtle()
        pointer.color("green")
        pointer.shape("turtle")
        pointer.speed(0)
        pointer.hideturtle()
        pointer.penup()
        pointer.goto(0, 0)  
        pointer.showturtle()
        return pointer

    def child_pointer(self):
        child = turtle.Turtle()
        child.color("#649865")
        child.shape("turtle")
        child.speed(0)
        child.hideturtle()
        child.penup()
        # child.showturtle()
        child.shapesize(stretch_wid=0.7, stretch_len=0.7)
        self.pointer_body.append(child)

    def create_food(self):
        food = turtle.Turtle()
        food.color("white")
        food.shape("square")
        food.hideturtle()
        food.speed(0)
        food.penup()
        food.goto(self.random_int(), self.random_int())
        food.showturtle()
        food.shapesize(stretch_wid=0.5, stretch_len=0.5)
        return food

    def crash(self):
        pointer_position = self.pointer.position()
        food_position = self.food.position()
        absolute_x = abs(pointer_position[0] - food_position[0])
        absolute_y = abs(pointer_position[1] - food_position[1])
        if absolute_x < 10 and absolute_y < 10:
            self.food.goto(self.random_int(), self.random_int())
            self._delay -= 0.0003
            self._score += 10
            self.update_points()
            self.child_pointer()
        
    def points(self):
        points = turtle.Turtle()
        points.penup()
        points.goto(0, 220)
        points.color("white")
        points.hideturtle()
        return points

    def update_points(self):
        self.points.clear()  
        self.points.write(f"Points: {self._score}   Record: {self._highest_score}", align="center", font=("Courier", 16, "bold"))

    def dev_by(self):
        dev = turtle.Turtle()
        dev.penup()
        dev.goto(0, -240)
        dev.color("white")
        dev.hideturtle()
        dev.write("Developed by: Rob Tovar", align="left", font=("Courier", 12, "bold"))
        return dev
        
    def arriba(self):
        if self._direction != "abajo" and (time.time() - self.last_move_time) > self.move_interval:
            self._direction = "arriba"
            self.pointer.setheading(90)
            self.last_move_time = time.time()  

    def abajo(self):
        if self._direction != "arriba" and (time.time() - self.last_move_time) > self.move_interval:
            self._direction = "abajo"
            self.pointer.setheading(270)
            self.last_move_time = time.time()  

    def izquierda(self):
        if self._direction != "derecha" and (time.time() - self.last_move_time) > self.move_interval:
            self._direction = "izquierda"
            self.pointer.setheading(180)
            self.last_move_time = time.time()  

    def derecha(self):
        if self._direction != "izquierda" and (time.time() - self.last_move_time) > self.move_interval:
            self._direction = "derecha"
            self.pointer.setheading(0)
            self.last_move_time = time.time() 

    def move(self):
        
        self.positions.append(self.pointer.position())
        self.headings.append(self.pointer.heading())
    
        max_positions = len(self.pointer_body) * self.follow_distance
        if len(self.positions) > max_positions:
            self.positions.pop(0)
            self.headings.pop(0)
    
        for i in range(len(self.pointer_body)):
            pos_index = -(i * self.follow_distance + self.follow_distance)
            if abs(pos_index) <= len(self.positions):  
                x, y = self.positions[pos_index]
                self.pointer_body[i].goto(x, y) 
                self.pointer_body[i].setheading(self.headings[pos_index])
                if self.pointer_body[i].xcor() == 0 and self.pointer_body[i].ycor() == 0:
                    self.pointer_body[i].hideturtle()
                else:
                    self.pointer_body[i].showturtle()
        
        if self._direction == "arriba":
            self.pointer.sety(self.pointer.ycor() + 2)
        elif self._direction == "abajo":
            self.pointer.sety(self.pointer.ycor() - 2)
        elif self._direction == "izquierda":
            self.pointer.setx(self.pointer.xcor() - 2)
        elif self._direction == "derecha":
            self.pointer.setx(self.pointer.xcor() + 2)

        self.pointer.hideturtle()
        self.pointer.showturtle()

    def borders_crash(self):

        if self.pointer.xcor() >= 192 or self.pointer.ycor() >= 192 or self.pointer.xcor() <= -192 or self.pointer.ycor() <= -192:
            self.reset()

    def body_crash(self):
                 
        for child in self.pointer_body:
            if self.pointer.distance(child) < 15:  
                self.reset()

    def reset(self):
        
            time.sleep(1)
            self.pointer.goto(0, 0)
            self._direction = None
            self.new_highest()
            self._delay = 0.01
            self._score = 0
            self.food.goto(self.random_int(), self.random_int())
            self.update_points()
            for child in self.pointer_body:
                child.hideturtle()
            self.pointer_body = []       

    def draw_bounds(self):
            bounds = turtle.Turtle()
            bounds.penup()
            bounds.goto(-210, 210)  
            bounds.pendown()
            bounds.color("black")
            bounds.pensize(2)
            
            for _ in range(4):
                bounds.forward(420)  
                bounds.right(90)  
    
            bounds.hideturtle()  

    def game_play(self):

        while True:
            self.screen.update()
            self.borders_crash()
            self.body_crash()
            self.crash()
            self.move()
            time.sleep(self._delay)
        self.screen.mainloop()
                  
snake_game = Snake()
snake_game.game_play()
        