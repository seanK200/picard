import pygame
from typing import List, Tuple, Union, Optional
from .const import *
from .ui import Element, ImageElement, UIElement
from .base import State


class PiCardApp:
    def __init__(
        self, 
        screen_size: Optional[Union[Tuple[int], List[int]]] = None,
        fps: int = 30,
    ) -> None:
        # Validate args
        if type(screen_size) not in [list, tuple]:
            raise TypeError(f"screen_size must be list or tuple, not {type(screen_size)}")
        if len(screen_size) != 2:
            raise ValueError(f"screen_size must be a list or tuple of (width, height) in pixels")
        self.screen_size = screen_size
        self.fps = fps
        self.running = True
        self.locked = False

        self.header_left = State('PiCard')
        self.header_right = State('Home')
        self.header_hr = State(True)
        self.footer_left = State('03:58')
        self.footer_right = State('1.4G/1024G')
        self.footer_hr = State(True)


        # pygame
        pygame.init()
        if screen_size:
            self.screen = pygame.display.set_mode(screen_size)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Arial", size=14)
    

    @property
    def screen_w(self):
        return self.screen_size[0]


    @property
    def screen_h(self):
        return self.screen_size[1]


    def run(self):
        self.render(True)
        while self.running:
            self.handle_events()
            # TODO self.update()
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


    def render(self, flip: bool = False):
        updated_rects: List[pygame.Rect] = []

        # Header
        if self.header_left.changed:
            text = self.font.render(self.header_left.get(), False, COLOR_WHITE)
            self.screen.blit(text, (PADDING_LEFT, PADDING_TOP))
            updated_rects.append(text.get_rect())
        
        if self.header_right.changed:
            text = self.font.render(self.header_right.get(), False, COLOR_WHITE)
            self.screen.blit(text, (
                self.screen_w - text.get_width() - PADDING_RIGHT, 
                PADDING_TOP
            ))
            updated_rects.append(text.get_rect())

        
        # Footer
        if self.footer_left.changed:
            text = self.font.render(self.footer_left.get(), False, COLOR_WHITE)
            self.screen.blit(text, (
                PADDING_LEFT, 
                self.screen_h - text.get_height() - PADDING_BOTTOM,
            ))
            updated_rects.append(text.get_rect())
        
        if self.footer_right.changed:
            text = self.font.render(self.footer_right.get(), False, COLOR_WHITE)
            self.screen.blit(text, (
                self.screen_w - text.get_width() - PADDING_RIGHT,
                self.screen_h - text.get_height() - PADDING_BOTTOM,
            ))
            updated_rects.append(text.get_rect())
        
        if flip:
            pygame.display.flip()
        else:
            pygame.display.update(updated_rects)



class PiCardTest:
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

