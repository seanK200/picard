import pygame
from typing import List
from .const import *
from .ui import Element, ImageElement, UIElement

class PiCard:
    def __init__(self, is_dev: bool, fps: int) -> None:
        self.running = True
        pygame.init()
        if is_dev:
            self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.all_elements: List[Element] = []
        self.needs_flip = True

        # square = Element(10, 20, 100, 50, background=(128, 34, 0))
        # self.all_elements.append(square)

        frame = ImageElement(10, 10, src="assets/UI_Flat_Frame_01_Lite.png")
        self.all_elements.append(frame)
        
        frame2 = UIElement(60, 10, 100, 80, src="assets/UI_Flat_Frame_01_Lite.png", scale_by=2, scale_boundary=(5, 4, 5, 4))
        self.all_elements.append(frame2)



    def start(self):
        pygame.display.flip()
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.fps)
        
        pygame.quit()

    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    
    def update(self):
        for element in self.all_elements:
            element.update()


    def render(self):
        updated_rects = []
        self.screen.fill(COLOR_SKYBLUE)
        for element in self.all_elements:
            element.render()
            self.screen.blit(element.image, element.rect)
            updated_rects.append(element.get_updated_rect())
        
        if self.needs_flip:
            pygame.display.flip()
            self.needs_flip = False
        else:
            pygame.display.update(updated_rects)

