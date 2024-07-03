import uvage
import random

camera = uvage.Camera(800,600)
character = uvage.from_color(400,100,"green",50,50)
character_speed = 8
s_height = 600
s_width = 800
left_wall = uvage.from_color(6, s_height / 2, "black", 50, s_height)
right_wall = uvage.from_color(s_width-6, s_height / 2, "black", 50, s_height)
bottom_wall = uvage.from_color(400, s_height, 'black', 800, 1)
top_wall = uvage.from_color(400, 0, 'black', 800, 1)
score = 0

floor_height = 300
floors = []
for x in range(1000):
    hole = random.randint(50,750)
    left_floor = uvage.from_color(0, floor_height, 'black', hole*1.75, 25)
    right_floor = uvage.from_color(750, floor_height, 'black', 800-hole, 25)
    floor_height += 100
    floors.append(left_floor)
    floors.append(right_floor)
playing = True



def tick():
    global character_speed
    global playing
    global score
    if playing == True:
        if uvage.is_pressing('right arrow'):
            character.x += character_speed
        if uvage.is_pressing('left arrow'):
            character.x -= character_speed
        character.move_speed()

        camera.clear('white')
        camera.draw(right_wall)
        camera.draw(left_wall)
        camera.draw(character)

        if character.touches(top_wall):
            playing = False
        if character.touches(bottom_wall):
            character.move_to_stop_overlapping(bottom_wall)
        if character.touches(left_wall) and uvage.is_pressing('right arrow') == False:
            character_speed = 0
        elif character.touches(right_wall) and uvage.is_pressing('left arrow') == False:
            character_speed = 0
        else:
            character_speed = 8

        camera.clear('white')
        camera.draw(right_wall)
        camera.draw(left_wall)

        character.yspeed += 1

        for floor in floors:
            camera.draw(floor)
            if character.touches(floor):
                character.move_to_stop_overlapping(floor)
            floor.yspeed = -3
            floor.move_speed()


        score += .05
        camera.draw(uvage.from_text(700, 100, str(int(score)), 50, 'Green'))

    if playing == False:
        camera.draw(uvage.from_text(400, 200, 'Game Over!', 50, "Red", bold=True))

    camera.draw(character)
    camera.display()

uvage.timer_loop(30,tick)