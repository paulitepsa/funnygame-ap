import sys
import string
import random
import pygame
import asyncio
import threading
import json
from apclient import APClient


class Game:
    def __init__(self, conn_info):
        self.ability_to_answer = False
        self.wincon_achieved = False
        self.user_text = ""
        self.prompt_text = "Waiting for the ability to answer..."
        self.r_items: dict
        self.conn_info = conn_info
        self.init_text_created = False
        self.run_game()

    def start_ap_client(self, loop, future, ap, conn_info):
        loop.run_until_complete(ap.run_archipelago(future, conn_info))

    def stop_ap_client(self, loop, future) -> None:
        loop.call_soon_threadsafe(future.set_result, None)

    def create_text(self, text, screen):
        # white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        black = (0, 0, 0)
        X = 600
        Y = 100

        font = pygame.font.Font("freesansbold.ttf", 32)
        pygame.display.set_caption("Funny gaem haha")
        text = font.render(text, True, green, blue)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)

        screen.blit(text, textRect)

    def check_ap_event(self, event, can_answer, wincon, ap):
        e_dict = event.message
        p_info = ap.get_player_info()
        if e_dict["cmd"] == "ReceivedItems":
            r_items = e_dict["items"]
            for item in r_items:
                if item == 3550:
                    can_answer = True
                if item == 3551:
                    print("You win :D")

    def run_game(self):

        loop = asyncio.get_event_loop()
        future = loop.create_future()
        ap = APClient()
        thread = threading.Thread(
            target=self.start_ap_client, args=(loop, future, ap, self.conn_info)
        )
        thread.start()

        pygame.init()
        pygame.fastevent.init()

        screen = pygame.display.set_mode((600, 400))
        clock = pygame.time.Clock()

        dt = 0
        input_active = False
        current_color = pygame.Color("chartreuse4")
        base_font = pygame.font.Font(None, 32)
        color_active = pygame.Color("lightskyblue3")
        input_rect = pygame.Rect(100, 200, 500, 40)
        user_text = ""
        random_letter = random.choice(string.ascii_uppercase)

        self.r_items = ap.get_received_items()
        running = True
        while running:
            for event in pygame.fastevent.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == ap.AP_EVENT:
                    print("EVENT GET", event)

                    if event.message["cmd"] == "ReceivedItems":
                        print("YO")
                        self.r_items = event.message["items"]
                        print("ITEMS", self.r_items)
                        for item in self.r_items:
                            print("ITERATED ITEM", item)
                            if item["item"] == 3550:
                                print("HAS 3550")
                                self.ability_to_answer = True

                                print("Text created?")
                            if item["item"] == 3551:
                                print("You win :D")

                if self.ability_to_answer is True:

                    self.prompt_text = f"Give me a letter {random_letter}!"
                    self.create_text(self.prompt_text, screen)

                if event.type == pygame.KEYDOWN:
                    if user_text.lower() == "quit" or user_text.lower() == "exit":
                        pygame.quit()
                        sys.exit()

                    if event.key == pygame.K_RETURN and self.ability_to_answer is True:

                        if self.wincon_achieved is False:
                            if user_text == random_letter:
                                print("CORRECT")
                                self.wincon_achieved = True

                                ap.handle_message(
                                    json.dumps(
                                        [
                                            {
                                                "cmd": "LocationChecks",
                                                "locations": [3551],
                                            },
                                            {"cmd": "StatusUpdate", "status": 30},
                                        ]
                                    )
                                )
                                #      pygame.fastevent.post(
                                #         pygame.event.Event(
                                #             ap.AP_LOCATION_CHECK_EVENT,
                                #              message=json.dumps([{"cmd": "W"}]),
                                #          )
                                #      )
                                self.prompt_text = "Correct! You win!"

                            else:
                                print("WRONG", user_text, random_letter)
                                self.prompt_text = "False! Try again."

                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]

                    else:
                        user_text += event.unicode

            screen.fill("purple")

            color = color_active
            pygame.draw.rect(screen, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            input_rect.w = max(200, text_surface.get_width() + 10)
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

            # if r_items:
            #    prompt_text = f"Give me a letter {random_letter}!"
            if not self.init_text_created:
                self.create_text(self.prompt_text, screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
