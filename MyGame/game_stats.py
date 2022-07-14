class GameStats(object):
    """跟踪游戏统计信息"""

    def __init__(self, ai_settings):
        """记录统计信息"""
        self.ai_settings = ai_settings
        self.ships_left = 2
        self.reset_stats()
        # 游戏刚刚开始处于活动状态
        self.game_active = True

    def reset_stats(self):
        """初始化游戏在运行期间可能变化的统计信息"""
        self.ships_left = self.ai_settings.ships_limits
