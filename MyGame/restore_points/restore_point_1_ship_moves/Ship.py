import pygame


class Ship(object):
    def __init__(self, ai_settings, screen):
        """初始化飞船的初始位置"""
        self.ai_settings = ai_settings
        self.screen = screen
        # 加载飞船的图片并加载其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的center属性中存储小数值，最后再把center转换成centerx
        self.center = float(self.rect.centerx)
        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # self.rect.centerx += 1
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            # self.rect.centerx -= 1
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_top and self.rect.top > self.screen_rect.top:
            self.rect.bottom -= 1
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.rect.bottom += 1
        self.rect.centerx = self.center

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕居中"""
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
