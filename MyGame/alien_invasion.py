import sys
import pygame
from Settings import Settings
from restore_points.restore_point_1_ship_moves.Ship import Ship
import game_functions as gf
from pygame.sprite import Group
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


def run_game():
    # 初始化游戏，创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # 创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # # 设置背景色
    # bg_color = (230, 230, 230)
    # 创建一个外星人
    alien = Alien(ai_settings, screen)
    # 创建一个用来存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    # 开始游戏的主循环
    while True:
        # 监视鼠标和键盘事件
        gf.check_events(ai_settings, screen, bullets, ship)
        # # 每次循环都重新绘制屏幕
        # screen.fill(ai_settings.bg_color)
        # ship.blitme()
        # # 让最近绘制的屏幕可见
        # pygame.display.flip()
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        # bullets.update()
        # # 删除消失的子弹
        # for bullet in bullets:
        #     if bullet.rect.bottom <= 0:
        #         bullets.remove(bullet)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()
