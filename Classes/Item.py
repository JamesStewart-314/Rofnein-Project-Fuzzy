import pygame

from typing import Union

from Assets import Items_Images
from Assets import Sound_Effects
from Assets import Weapon_Images
from Assets import Worlds
from Constants import Game_Constants
from Classes import Character
from Classes import DamageText
from Classes import ShowText

pygame.init()


class Item(pygame.sprite.Sprite):
    items_dict = dict(red_potion=Items_Images.Red_Potion, coin=Items_Images.Coin,
                      silver_coin=Items_Images.Silver_Coin, red_coin=Items_Images.Red_Coin,
                      emerald=Items_Images.Emerald, static_coin=Items_Images.Static_Coin,
                      steel_bow=[Weapon_Images.Steel_Bow_Img], gold_bow=[Weapon_Images.Gold_Bow_Img],
                      ataque_upgrade = [Weapon_Images.ataque_img], vida_upgrade= [Weapon_Images.vida_img])

    def __init__(self, coordinate_x: Union[int, float], coordinate_y: Union[int, float],
                 item_type: str, can_collect: bool = True):

        assert (item_type in Item.items_dict), f"Given item name doesn't exist. Try these: " \
                                               f"{list(Item.items_dict.keys())}"

        self.can_collect = can_collect

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.animation = Item.items_dict.__getitem__(self.item_type)
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (coordinate_x, coordinate_y)

    def update(self, current_player: Character, text_group: object) -> None:

        # Check to see if item has been collected by the player :
        if self.can_collect:
            if self.rect.colliderect(current_player.hitbox):
                if self.item_type == "coin":
                    Sound_Effects.Coin_Collect.play()
                    current_player.money += 10
                    text_group.add(ShowText.ShowText(self.rect.centerx, self.rect.centery,
                                                     str(10), Game_Constants.YELLOW_COLOR, "Micro"))
                    self.kill()

                elif self.item_type == "silver_coin":
                    Sound_Effects.Silver_Coin_Collect.play()
                    current_player.money += 30
                    text_group.add(ShowText.ShowText(self.rect.centerx, self.rect.centery,
                                                     str(30), Game_Constants.SILVER_COLOR, "Micro"))
                    self.kill()

                elif self.item_type == "red_coin":
                    Sound_Effects.Red_Coin_Collect.play()
                    current_player.money += 50
                    text_group.add(ShowText.ShowText(self.rect.centerx, self.rect.centery,
                                                     str(50), Game_Constants.RED_COLOR, "Micro"))
                    self.kill()

                elif self.item_type == "emerald":
                    Sound_Effects.Emerald_Collect.play()
                    current_player.money += 100
                    text_group.add(ShowText.ShowText(self.rect.centerx, self.rect.centery,
                                                     str(100), Game_Constants.GREEN_COLOR, "Micro"))
                    self.kill()

                elif self.item_type == "red_potion":
                    Sound_Effects.Red_Potion_Collect.play()
                    current_player.health += Game_Constants.potion_heal
                    text_group.add(ShowText.ShowText(self.rect.centerx, self.rect.centery,
                                                     "+ " + str(Game_Constants.potion_heal),
                                                     Game_Constants.CRIMSON_RED_COLOR, "Micro"))
                    self.kill()
                    if current_player.health > 100:
                        current_player.health = 100

                elif self.item_type == "steel_bow" and current_player.money>=20:
                    current_player.weapons_inventory.append("Steel_bow")
                    current_player.money-= 20
                    Game_Constants.steel_coletado = True
                    Sound_Effects.Weapon_Collect.play_loop()
                    self.kill()
                    text_group.add(ShowText.ShowText(self.rect.centerx + 28, self.rect.centery, "Steel Bow Acquired",
                                                     Game_Constants.SILVER_COLOR, "Micro", kill_time=1100, speed=0.6))

                elif self.item_type == "gold_bow" and current_player.money>=30:
                    current_player.weapons_inventory.append("Gold_bow")
                    current_player.money-= 30
                    Game_Constants.gold_coletado = True
                    Sound_Effects.Weapon_Collect.play_loop()

                    text_group.add(ShowText.ShowText(self.rect.centerx + 28, self.rect.centery, "Gold Bow Acquired",
                                                     Game_Constants.YELLOW_COLOR, "Micro", kill_time=1100, speed=0.6))

                    
                    self.kill()
                    

        left_mouse_click = pygame.mouse.get_pressed()[0]
        if left_mouse_click and self.item_type=="ataque_upgrade":
            Game_Constants.ataque_upgrade+=1  
        if left_mouse_click and self.item_type=="vida_upgrade":
            Game_Constants.vida_upgrade+=1      

        # Handle Animation :
        self.image = self.animation[self.frame_index]

        # Check if enough time has passed since the last update :
        if pygame.time.get_ticks() - self.update_time > Game_Constants.animation_items_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animation)

    def draw(self, surface: object) -> None:
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, Game_Constants.WHITE_COLOR, self.rect, 1)
