class GameState:
    def __init__(self):
        self.APP_RUN = True
        self.INIT_MENU = True
        self.MOD_CHRONO = True
        self.MOD_TRAINING = False
        self.run_game = False
        self.run_menu = True
        self.run_game_result = False
        self.time_start_game = 0
        # Add any other variables you need here

    def quit(self):
        self.APP_RUN = False