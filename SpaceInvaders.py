import uvage
import random

camera = uvage.Camera(800, 600)
projectile = uvage.from_color(400, 500, "blue", 5, 5)
enemy_projectile1 = uvage.from_color(-10, 500, "red", 10, 10)
enemy_projectile2 = uvage.from_color(-10, 500, "red", 10, 10)
enemy_projectile3 = uvage.from_color(-10, 500, "red", 10, 10)
enemy_projectile_list = [enemy_projectile3, enemy_projectile2, enemy_projectile1]
EProjectile_status = [0, 0, 0]

player=uvage.from_image(400,500,r"SpaceInvadersShip.jpg")
player.width/=3.5
player.height/=3.5
placeholder = uvage.from_color(400, 300, "black", 1, 1)
enemy0 = uvage.from_image(200, 100, r"SpaceInvadersEnemy.png")
enemy1 = uvage.from_image(400, 100, r"SpaceInvadersEnemy.png")
enemy2 = uvage.from_image(600, 100, r"SpaceInvadersEnemy.png")
enemy3 = uvage.from_image(200, 200, r"SpaceInvadersEnemy.png")
enemy4 = uvage.from_image(400, 200, r"SpaceInvadersEnemy.png")
enemy5 = uvage.from_image(600, 200, r"SpaceInvadersEnemy.png")
enemy6 = uvage.from_image(200, 300, r"SpaceInvadersEnemy.png")
enemy7 = uvage.from_image(400, 300, r"SpaceInvadersEnemy.png")
enemy8 = uvage.from_image(600, 300, r"SpaceInvadersEnemy.png")
enemy8 = uvage.from_image(600, 300, r"SpaceInvadersEnemy.png")

enemies = [enemy0, enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8]
for enemy in enemies:
    enemy.width /= 5
    enemy.height /= 5

dead_enemies = [0, 1, 2, 3, 4, 5, 6, 7, 8]
score_tracker = 0
question = uvage.from_text(400, 300, "Press N to go to Next Level", 50, "white", True)
game_over_message = uvage.from_text(400, 300, "Game Over", 100, "white", True)

enemy_speed = 3
player_speed = 3.5
projectile_status = 0
enemy_projectile_speed = 3
health = 5
frames = 0
projectile_speed = 10
game_over = 0


def tick():
    global enemy_speed, player_speed, projectile_status, dead_enemies
    global score_tracker, player, enemies, health, enemy_projectile_speed
    global projectile, frames, projectile_speed, game_over

    # Frame counter/Clock
    frames += 1

    # Projectile movement
    if projectile_status == 1:
        projectile.y -= projectile_speed
    if projectile.y < 0:
        projectile_status = 0
        projectile.x = 400
        projectile.y = 500

    for E_projectile in enemy_projectile_list:
        if EProjectile_status[enemy_projectile_list.index(E_projectile)] == 1:
            E_projectile.y += enemy_projectile_speed

    # Enemy projectile control
    if frames % 30 == 0:
        for E_projectile in enemy_projectile_list:
            position = enemy_projectile_list.index(E_projectile)
            if EProjectile_status[position] == 0:
                EProjectile_status[position] = 1
                number = random.randint(0, 8)
                if enemies[number].width >10:
                    E_projectile.x = enemies[number].x
                    E_projectile.y = enemies[number].y
            elif E_projectile.y > 600:
                EProjectile_status[position] = 0

    # Player movement
    if uvage.is_pressing("right arrow"):
        player.x += player_speed

    if uvage.is_pressing("left arrow"):
        player.x -= player_speed

    if uvage.is_pressing("up arrow"):
        if projectile_status == 0:
            projectile_status = 1
            projectile.x = player.x
            projectile.y = 500

    # Collisions
    enemy_counter = 0
    for enemy in enemies:
        if enemy.x < 55 or enemy.x > 745:
            if enemy.width > 1:
                enemy_counter += 1
    if enemy_counter > 0:
        enemy_speed *= -1

    if player.x < 30:
        player.x += player_speed
    elif player.x > 770:
        player += player_speed

    for enemy_projectile in enemy_projectile_list:
        if enemy_projectile.touches(player):
            if EProjectile_status[enemy_projectile_list.index(enemy_projectile)] == 1:
                health -= 1
                EProjectile_status[enemy_projectile_list.index(enemy_projectile)] = 0

    # Reset
    type_counter = 9
    for enemy in dead_enemies:
        if type(enemy) is not int:
            type_counter -= 1
    if type_counter == 0:
        camera.draw(question)
        if uvage.is_pressing('n'):
            enemies = dead_enemies
            dead_enemies = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            position_x = 200
            position_y = 100
            enemy_speed = abs(enemy_speed)+2
            counter = 0

            for enemy in enemies:
                enemy.x = position_x
                enemy.y = position_y
                counter += 1
                if counter % 3 == 0:
                    position_y += 100
                    position_x = 200
                else:
                    position_x += 200

    # Enemy movement
    for enemy in enemies:
        enemy.x += enemy_speed

    # Game over
    if health <= 0:
        enemy_speed = 0
        player_speed = 0
        projectile_speed = 0
        game_over = 1
        health=0

    # Camera
    score = uvage.from_text(50, 100, str(score_tracker), 100, "white")
    health_display = uvage.from_text(750, 100, str(health), 100, "pink")
    camera.clear("black")
    for enemy in enemies:
        if projectile.touches(enemy):
            score_tracker += 1
            position = enemies.index(enemy)
            dead_enemies[position] = enemy
            enemies[position] = placeholder
            projectile_status = 0
            projectile.x = 400
            projectile.y = 500

        else:
            camera.draw(enemy)

    if projectile_status == 1:
        camera.draw(projectile)
    type_counter = 9
    for enemy in dead_enemies:
        if type(enemy) is not int:
            type_counter -= 1
    if type_counter == 0:
        camera.draw(question)
    for E_projectile in enemy_projectile_list:
        position = enemy_projectile_list.index(E_projectile)
        if EProjectile_status[position] == 1:
            camera.draw(E_projectile)

    if game_over:
        camera.draw(game_over_message)
        final_score = uvage.from_text(400, 400, "Your final score is: "+str(score_tracker), 50, "white", True)
        camera.draw(final_score)

    camera.draw(health_display)
    camera.draw(score)
    camera.draw(player)
    camera.display()


uvage.timer_loop(30, tick)
