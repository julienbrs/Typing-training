from .constants import *

class UIManager:
    def __init__(self, window):
        self.WIN = window

    def display_wpm(self, wpm):
        str_hud = "WPM : " + wpm
        text_wpm = FONT_ARABOTO_50.render(str_hud, 1, DARK_PURPLE)
        self.WIN.blit(text_wpm, (WIDTH * 0.95 -
                      text_wpm.get_width(), HEIGHT * 0.08))

    def display_next_text(self, next_text):
        next_text_game = FONT_HELVETICA.render(next_text, 1, DARK_PURPLE)
        next_text_game.set_alpha(180)
        self.WIN.blit(next_text_game, (WIDTH * 0.5 -
                      next_text_game.get_width() / 2, HEIGHT * 0.57))

    def draw_current_text(self, font, text_manager, current_index, test_letter, last_key_wrong):
        M_ADV_X = 4  # todo ??? Madv_x

        # calculate how big the entire line of text is
        text_surf_rect = font.get_rect(text_manager.current_text)
        text_surf_rect.size = (
            text_surf_rect.size[0] * 1.1,
            text_surf_rect.size[1]
        )  # todo more elegant?

        # This rect's y property is the baseline since we use the origin mode
        baseline = text_surf_rect.y

        # Create a surface to render the text on and center it on the screen
        text_surf = pygame.Surface(text_surf_rect.size)
        text_surf_rect.center = self.WIN.get_rect().center

        # Calculate the width (and other stuff) for each letter of the text
        metrics = font.get_metrics(text_manager.current_text)

        # Fill the surface
        text_surf.fill(YELLOW_ORANGE)

        x = 0
        for (idx, (letter, metric)) in enumerate(zip(text_manager.current_text, metrics)):
            # Set default color
            color = DARK_PURPLE

            # select the right color
            if idx == current_index:
                start_pos = (
                    text_surf_rect.x + x + 3,
                    text_surf_rect.y + text_surf_rect.height - 5,
                )
                end_pos = (
                    text_surf_rect.x + x + metric[M_ADV_X] - 5,
                    text_surf_rect.y + text_surf_rect.height - 5,
                )

                if test_letter in [KeyPressResponse.NO_TEST, KeyPressResponse.NO_ACTION]:
                    color = RED_WRONG if last_key_wrong else "lightblue"
                elif test_letter == KeyPressResponse.WRONG:
                    color = RED_WRONG
                elif test_letter == KeyPressResponse.CORRECT:
                    color = GREEN_RIGHT

                else:
                    print(f"Error: {test_letter} not in enum")

                color_line = color
            elif idx < current_index:
                color = GREEN_RIGHT
            else:
                color = DARK_PURPLE

            # render the single letter
            font.render_to(text_surf, (x, baseline), letter, color)
            # and move the start position
            x += metric[M_ADV_X]

        self.WIN.blit(text_surf, text_surf_rect)
        self.draw_line_under_text(start_pos, end_pos, color_line)

    def draw_line_under_text(self, start_pos, end_pos, color):
        pygame.draw.line(self.WIN, color, start_pos, end_pos, width=5)
