import pygame
import math
from typing import List, Tuple, Optional, Union, TypeVar, Generic


T = TypeVar('T')


class State(Generic[T]):
    def __init__(self, init_value: T, state_collection: Optional[List]):
        self.value: T = init_value
        self.changed = True
        if state_collection:
            state_collection.append(self)
    
    def get(self):
        self.changed = False
        return self.value

    def set(self, new_value: T):
        # Check change
        if type(self.value) == type(new_value):
            if type(self.value) in [list, tuple]:
                if len(self.value) == len(new_value):
                    for before, after in zip(self.value, new_value):
                        if before != after:
                            self.changed = True
                            break
                else:
                    self.changed = True
            elif type(self.value) == dict:
                if len(self.value) == len(new_value):
                    for k, v in self.value.items():
                        if k not in new_value or v != new_value[k]:
                            self.changed = True
                            break
                    for k, v in new_value.items():
                        if k not in self.value:
                            self.changed = True
                            break
                else:
                    self.changed = True
            elif type(self.value) == set:
                if len(self.value) == len(new_value):
                    for before in self.value:
                        if before not in new_value:
                            self.changed = True
                            break
                    for after in new_value:
                        if after not in self.value:
                            self.changed = True
                            break
                else:
                    self.changed = True
            else:
                if new_value != self.value:
                    self.changed = True
        else:
            self.changed = True
        
        # If something changed, update the value
        if self.changed:
            self.value = new_value


class Element(pygame.sprite.Sprite):
    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int = 0, 
        height: int = 0, 
        *, 
        colorkey: Union[Tuple[int], None] = None,
        focusable: bool = False,
        background: Union[Tuple[int], None] = None, 
        opacity: Union[int, None] = None,
        init_image: bool = True,
    ) -> None:
        super().__init__()
        self.all_states: List[State] = []
        self._x = State(x, self.all_states)
        self._y = State(y, self.all_states)
        self._w = State(width, self.all_states)
        self._h = State(height, self.all_states)
        self._colorkey = State(colorkey, self.all_states)
        self._background = State(background, self.all_states)
        self._opacity = State(opacity, self.all_states)
        self._focused = State(False, self.all_states)
        self._focusable = focusable
        self.updated = True

        if init_image:
            self.init_image()


    @property
    def x(self):
        return self._x.value

    @x.setter
    def x(self, value: int):
        return self._x.set(value)

    @property
    def y(self):
        return self._y.value
    
    @y.setter
    def y(self, value: int):
        return self._y.set(value)

    @property
    def w(self):
        return self._w.value
    
    @w.setter
    def w(self, value: int):
        return self._w.set(value)
    
    @property
    def h(self):
        return self._h.value
    
    @h.setter
    def h(self, value: int):
        return self._h.set(value)
    
    @property
    def colorkey(self):
        return self._colorkey.value
    
    @colorkey.setter
    def colorkey(self, value: Union[Tuple[int], None]):
        return self._colorkey.set(value)
    
    @property
    def background(self):
        return self._background.value
    
    @background.setter
    def background(self, value: Union[Tuple[int], None]):
        return self._background.set(value)
    
    @property
    def opacity(self):
        return self._opacity.value
    
    @opacity.setter
    def opacity(self, value: Union[Tuple[int], None]):
        return self._opacity.set(value)
    
    @property
    def focused(self):
        return self._focused.value
    
    @focused.setter
    def focused(self, value: bool):
        return self._focused.set(value)

    @property
    def focusable(self) -> bool:
        return self._focusable
    

    @focusable.setter
    def focusable(self, value):
        if not value:
            self.focused.set(False)
        self._focusable = value


    @property
    def changed(self) -> bool:
        for state in self.all_states:
            if state.changed:
                return True
        return False
    

    def init_image(self):
        self.image = pygame.Surface((self.w, self.h))
        if self.colorkey:
            self.image.set_colorkey(self.colorkey, pygame.RLEACCEL)
        self.rect = self.image.get_rect(left=self.x, top=self.y)
        self.render(True)
    

    def render(self, force: bool = False):
        if not force and not self.changed:
            return
        
        self.updated = True
        self.render_background()
        self.render_opacity()
        

    def render_background(self):
        if self.background:
            self.image.fill(self._background.get())
    
    
    def render_opacity(self):
        if self.opacity != None:
            self.image.set_alpha(self._opacity.get())

        
    def get_updated_rect(self) -> Union[pygame.Rect, None]:
        if self.updated:
            self.updated = False
            return self.rect
        else:
            return None
    

class ImageElement(Element):
    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int = 0, 
        height: int = 0, 
        *, 
        src: str,
        scale_by: float = 1.0,
        colorkey: Union[Tuple[int], None] = None, 
        focusable: bool = False, 
        background: Union[Tuple[int], None] = None, 
        opacity: Union[int, None] = None
    ) -> None:
        super().__init__(x, y, width, height, colorkey=colorkey, focusable=focusable, background=background, opacity=opacity, init_image=False)
        self.src = src
        self._scale_by = State(scale_by, self.all_states)
        self.init_image()
    

    @property
    def scale_by(self):
        return self._scale_by.value
    

    @scale_by.setter
    def scale_by(self, value: float):
        self._scale_by.set(value)
    

    def init_image(self):
        self.load_image()
        self.scale_image()
        self.render(True)
    
    
    def load_image(self):
        self.image = pygame.image.load(self.src).convert()
        self.image.set_colorkey(self.colorkey if self.colorkey else (0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect(left=self.x, top=self.y)
        self.original_image = self.image


    def scale_image(self):
        scaled = True
        if self.w and self.h:
            self.image = pygame.transform.scale(self.original_image, (self.w, self.h))
        elif self.w:
            h = math.floor(self.w * self.rect.h / self.rect.w)
            self.image = pygame.transform.scale(self.original_image, (self.w, h))
        elif self.h:
            w = math.floor(self.h * self.rect.w / self.rect.h)
            self.image = pygame.transform.scale(self.original_image, (w, self.h))
        elif self.scale_by != 1:
            self.image = pygame.transform.scale(self.original_image, (self.rect.w * self.scale_by, self.rect.h * self.scale_by))
        else:
            scaled = False
        
        if scaled:
            self.rect = self.image.get_rect(left=self.x, top=self.y)


class UIElement(ImageElement):
    def __init__(
        self, 
        x: int, 
        y: int, 
        width: int = 0, 
        height: int = 0, 
        *, 
        src: str, 
        scale_by: int = 1,
        scale_boundary: Union[Tuple[int], None] = None,
        colorkey: Union[Tuple[int], None] = None, 
        focusable: bool = False, 
        background: Union[Tuple[int], None] = None, 
        opacity: Union[int, None] = None
    ) -> None:
        super().__init__(x, y, width, height, src=src, scale_by=scale_by, colorkey=colorkey, focusable=focusable, background=background, opacity=opacity)
        if type(scale_boundary) == tuple:
            if 4 % len(scale_boundary) == 0:
                self.scale_boundary: Tuple[int] = scale_boundary * (4 // len(scale_boundary))
            else:
                raise ValueError('scale_boundary length should be either 1, 2, 4')
        elif type(scale_boundary) == int:
            self.scale_boundary: Tuple[int] = [scale_boundary] * 4
        else:
            raise TypeError('Unexpected scale_boundary type: ' + str(type(scale_boundary)))
        self.init_image()


    def load_image(self):
        super().load_image()
        # self.repeat_rect = pygame.Rect(
        #     self.scale_boundary[3], 
        #     self.scale_boundary[0],
        #     self.rect.w - self.scale_boundary[3] - self.scale_boundary[1], 
        #     self.rect.h - self.scale_boundary[0] - self.scale_boundary[2]
        # )
    
    def scale_image(self):
        if self.scale_by != 1:
            self.image = pygame.transform.scale(self.original_image, (self.rect.w * self.scale_by, self.rect.h * self.scale_by))
        
        

# class UIElement(ImageElement):
#     def __init__(
#         self, 
#         x: int, 
#         y: int, 
#         width: int = 0, 
#         height: int = 0, 
#         *, 
#         scale_boundary: Union[int, Tuple[int]], 
#         src: str = '', 
#         scale_by: int = 1, 
#         colorkey: Union[Tuple[int], None] = None,
#         focusable: bool = False, 
#         background: Union[Tuple[int], None] = None, 
#         opacity: Union[int, None] = None
#     ) -> None:
#         if type(scale_boundary) == tuple:
#             if 4 % len(scale_boundary) == 0:
#                 self.scale_boundary: Tuple[int] = scale_boundary * (4 // len(scale_boundary))
#             else:
#                 raise ValueError('scale_boundary length should be either 1, 2, 4')
#         elif type(scale_boundary) == int:
#             self.scale_boundary: Tuple[int] = [scale_boundary] * 4
#         else:
#             raise TypeError('Unexpected scale_boundary type: ' + str(type(scale_boundary)))
#         self.corners: Union[pygame.Surface, None] = None

#         super().__init__(
#             x, 
#             y, 
#             width, 
#             height, 
#             src=src, 
#             scale_by=scale_by, 
#             colorkey=colorkey, 
#             focusable=focusable, 
#             background=background, 
#             opacity=opacity
#         )

#     def scale_image(self):
#         boundary = self.scale_boundary
#         if self.scale_by != 1:
#             self.scale_boundary = tuple(i * self.scale_by for i in self.scale_boundary)
        
#         # Scaled size
#         if self._w and self._h:
#             scaled_w = self._w
#             scaled_h = self._h
#         elif self._w:
#             scaled_w = self._w
#             scaled_h = self._w
#         elif self._h:
#             scaled_w = self._h
#             scaled_h = self._h
#         elif self.scale_by == 1:
#             self.image = self.original_image
            

#         # Create corners Surface
#         if not self.corners:
#             chop_w = self.rect.w * self.scale_by - boundary[3] - boundary[1]
#             chop_h = self.rect.h * self.scale_by - boundary[0] - boundary[2]
#             self.corners = pygame.transform.chop(self.original_image, pygame.Rect(boundary[3], boundary[0], chop_w, chop_h))
            






# if self.scale_boundary:
#     if self.scale_by != 1:
#         self.scale_boundary = tuple(i * self.scale_by for i in self.scale_boundary)
    
#     boundary = self.scale_boundary
#     if not self.corners:
        # chop_w = self.rect.w * self.scale_by - boundary[3] - boundary[1]
        # chop_h = self.rect.h * self.scale_by - boundary[0] - boundary[2]
        # self.corners = pygame.transform.chop(self.original_image, pygame.Rect(boundary[3], boundary[0], chop_w, chop_h))
    
#     # Scaled
    # if self._w and self._h:
    #     scaled_w = self._w
    #     scaled_h = self._h
    # elif self._w:
    #     scaled_w = self._w
    #     scaled_h = self._h
    # elif self._h:
        


#     # Blit corners





# class Resizable(pygame.sprite.Sprite):
#     def __init__(
#         self, 
#         src: str, 
#         rect: pygame.Rect, 
#         boundary: Optional[Union[List[int], Tuple[int], int]] = None,
#         scale: int = 1,
#     ) -> None:
#         super().__init__()

#         # Boundary condition
#         self.boundary: List[int] = []
#         if boundary != None:
#             if type(boundary) == int:
#                 self.boundary.append(boundary)
#             elif type(boundary) == list or type(boundary) == tuple:
#                 for v in boundary:
#                     self.boundary.append(v)
#             else:
#                 raise TypeError('Expected List[int]')
#             if 4 % len(self.boundary) == 0:
#                 self.boundary *= 4 // len(self.boundary)
#             else:
#                 raise ValueError('Invalid boundary length: ' + str(len(self.boundary)))
            
#         if scale != 1:
#             for i, b in enumerate(self.boundary):
#                 self.boundary[i] = b * scale
            
#         # Size
#         self.rect = rect
#         min_w = self.boundary[1] + self.boundary[3]
#         min_h = self.boundary[0] + self.boundary[2]
#         if self.rect.w < min_w:
#             self.rect.w = min_w
#         if self.rect.h < min_h:
#             self.rect.h = min_h
            
#         # Load image
#         self.img_surf = pygame.image.load(src).convert()
#         if scale != 1:
#             img_rect = self.img_surf.get_rect()
#             self.img_surf = pygame.transform.scale(
#                 self.img_surf, 
#                 (img_rect.w * scale, img_rect.h * scale)
#             )
#         self.img_surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
#         img_rect = self.img_surf.get_rect()
#         img_w = img_rect.width
#         img_h = img_rect.height

#         # Get x, y, w, h for repeatable Area
#         repeat_rect = pygame.Rect(
#             self.boundary[3], 
#             self.boundary[0],
#             img_w - self.boundary[3] - self.boundary[1], 
#             img_h - self.boundary[0] - self.boundary[2]
#         )

#         # Get x, y, w, h for corners (topleft, topright, bottomright, bottomleft)
#         if self.boundary[0] and self.boundary[3]:
#             corner_tl = pygame.Rect(
#                 0, 
#                 0,
#                 self.boundary[3], 
#                 self.boundary[0], 
#             )
#         else:
#             corner_tl = None
        
#         if self.boundary[0] and self.boundary[1]:
#             corner_tr = pygame.Rect(
#                 img_w - self.boundary[1], 
#                 0,
#                 self.boundary[1], 
#                 self.boundary[0], 
#             )
#         else:
#             corner_tr = None
        
#         if self.boundary[1] and self.boundary[2]:
#             corner_br = pygame.Rect(
#                 img_w - self.boundary[1], 
#                 img_h - self.boundary[2],
#                 self.boundary[1], 
#                 self.boundary[2], 
#             )
#         else:
#             corner_br = None
        
#         if self.boundary[2] and self.boundary[3]:
#             corner_bl = pygame.Rect(
#                 0, 
#                 img_h - self.boundary[2],
#                 self.boundary[3], 
#                 self.boundary[2], 
#             )
#         else:
#             corner_bl = None

#         # Get x, y, w, h for edges (top, right, bottom, left)
#         if self.boundary[0]:
#             edge_t = pygame.Rect(
#                 self.boundary[3], 
#                 0,
#                 repeat_rect.w, 
#                 self.boundary[0], 
#             )
#         else:
#             edge_t = None
        
#         if self.boundary[1]:
#             edge_r = pygame.Rect(
#                 img_w - self.boundary[1], 
#                 self.boundary[0],
#                 self.boundary[1], 
#                 repeat_rect.h, 
#             )
#         else:
#             edge_r = None
        
#         if self.boundary[2]:
#             edge_b = pygame.Rect(
#                 self.boundary[3], 
#                 img_h - self.boundary[2],
#                 repeat_rect.w, 
#                 self.boundary[2], 
#             )
#         else:
#             edge_b = None
        
#         if self.boundary[3]:
#             edge_l = pygame.Rect(
#                 0, 
#                 self.boundary[0],
#                 self.boundary[3], 
#                 repeat_rect.h, 
#             )
#         else:
#             edge_l = None

#         self.repeat_rect = repeat_rect
#         self.corner_rects = (corner_tl, corner_tr, corner_br, corner_bl)
#         self.edge_rects = (edge_t, edge_r, edge_b, edge_l)

#         print("REPEAT")
#         print(repeat_rect)
#         print("\nCORNERS")
#         for c in self.corner_rects:
#             if c:
#                 print(c.w, c.h, c.x, c.y)
#             else:
#                 print("None")
#         print("\nEDGES")
#         for e in self.edge_rects:
#             if e:
#                 print(e.w, e.h, e.x, e.y)
#             else:
#                 print("None")
        
#         self.draw()

    
#     def draw(self):
#         self.surf = pygame.Surface((self.rect.w, self.rect.h))
#         self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
#         self.rect = self.surf.get_rect(
#             x=self.rect.x,
#             y=self.rect.y
#         )

#         # Blit corners
#         corner_dests = (
#             (0, 0),
#             (self.rect.w - self.boundary[1], 0),
#             (self.rect.w - self.boundary[1], self.rect.h - self.boundary[2]),
#             (0, self.rect.h - self.boundary[2]),
#         )
#         for i, corner_rect in enumerate(self.corner_rects):
#             if corner_rect:
#                 self.surf.blit(self.img_surf, corner_dests[i], corner_rect)
        
#         edge_w = self.rect.w - self.boundary[3] - self.boundary[0]
#         edge_h = self.rect.h - self.boundary[0] - self.boundary[2]

#         for i, edge_rect in enumerate(self.edge_rects):
#             if edge_rect:
#                 if i % 2 == 0:
#                     if edge_w:
#                         pass
#                 else:
#                     if edge_h:
#                         pass

        
    




# class Element:
#     def __init__(self, focusable: bool = True, tabindex: int = -1) -> None:
#         self.focusable = focusable
#         self.focused = False
#         pass


# class Button(Element):
#     IDLE = 0
#     PRESS = 1
#     LOCK = 2
#     RELEASE = 3


#     def __init__(self, focusable: bool = True, tabindex: int = -1, latch: bool = False) -> None:
#         super().__init__(focusable, tabindex)
#         self.latch = latch
#         self.disabled = False
        
#         # For animations
#         self.frame = 0
