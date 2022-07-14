import sys
import pygame
from time import sleep
from alien import Alien
from bullet import Bullet


def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上图像，并切换到新屏幕"""
    # 每次循环时都重新绘制图像
    screen.fill(ai_settings.bg_color)
    # 在外星人和飞船后面重新绘制子弹
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def check_keyup_events(ship, event):
    """松开按键"""
    print(event)
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_top = False
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = False


def check_keydown_event(ai_settings, screen, bullets, ship, event):
    """响应按键"""
    print(event)
    if event.key == pygame.K_RIGHT:
        # ship.rect.centerx += 1
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_top = True
    elif event.key == pygame.K_DOWN:
        ship.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        # # 创建一颗子弹
        # new_bullet = Bullet(ai_settings, screen, ship)
        # bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_events(ai_settings, screen, bullets, ship):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(ai_settings, screen, bullets, ship, event)
            # if event.key == pygame.K_RIGHT:
            #     # ship.rect.centerx += 1
            #     ship.moving_right = True
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = True
            # elif event.key == pygame.K_UP:
            #     ship.moving_top = True
            # elif event.key == pygame.K_DOWN:
            #     ship.moving_bottom = True
        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)

            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # elif event.key == pygame.K_LEFT:
            #     ship.moving_left = False
            # elif event.key == pygame.K_UP:
            #     ship.moving_top = False
            # elif event.key == pygame.K_DOWN:
            #     ship.moving_bottom = False


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """更新子弹的位置，删除消失的子弹"""
    # 更新子弹位置
    bullets.update()
    # 删除消失子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collection(ai_settings, screen, ship, aliens, bullets)
    # 检查是否有子弹击中了外星人
    # 如果是这样就删除对应的子弹和外星人
    # collections = pygame.sprite.groupcollide(bullets, aliens, True, True)
    # if len(aliens) == 0:
    #     # 删除现有子弹并新建一群外星人
    #     bullets.empty()
    #     create_fleet(ai_settings, screen, ship, aliens)


def check_bullet_alien_collection(ai_settings, screen, ship, aliens, bullets):
    """响应子弹和外星人的碰撞"""
    collections = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行容纳多少人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - ship_height - 3 * alien_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # 创建一个外星人，并计算一行可以创造多少个外星人
    # 外星人间距位外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # alien_width = alien.rect.width
    # available_space_x = ai_settings.screen_width - 2 * alien_width
    # number_aliens_x = int(available_space_x / (2 * alien_width))

    for row_number in range(number_rows):
        # 创建外星人群
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            # alien = Alien(ai_settings, screen)
            # alien.x = alien_width + 2 * alien_width * alien_number
            # alien.rect.x = alien.x
            # aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """外星人到达边界时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变他们的方向"""
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # 暂停
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """检查外星人是否到达底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样处理
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    检查是否有外星人位于屏幕边缘
    并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检查外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        print('ship hit!!!')
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
