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
        opacity: Union[int, None] = None,
        init_image: bool = True,
    ) -> None:
        super().__init__(x, y, width, height, colorkey=colorkey, focusable=focusable, background=None, opacity=opacity, init_image=False)
        self.src = src
        self.scale_by = scale_by
        if init_image:
            self.init_image()
    

    def init_image(self):
        self.load_image()
        self.render(True)
    
    
    def load_image(self):
        self.image = pygame.image.load(self.src).convert()
        self.image.set_colorkey(self.colorkey if self.colorkey else (0, 0, 0), pygame.RLEACCEL)
        if self.scale_by != 1:
            original_rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (original_rect.w * self.scale_by, original_rect.h * self.scale_by))
        self.rect = self.image.get_rect(left=self.x, top=self.y)
        self.original_image = self.image


    def render(self, force: bool = False):
        if not force and not self.changed:
            return
        
        self.updated = True
        if force or self._w.changed or self._h.changed:
            w = self._w.get()
            h = self._h.get()

            if not w and h:
                w = math.floor(h * self.rect.w / self.rect.h)
            if not h and w:
                h = math.floor(w * self.rect.h / self.rect.w)
            
            if w and h:
                self.image = pygame.transform.scale(self.original_image, (w, h))
                self.rect = self.image.get_rect(left=self.x, top=self.y)
        
        self.render_opacity()


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
        opacity: Union[int, None] = None
    ) -> None:
        super().__init__(x, y, width, height, src=src, scale_by=scale_by, colorkey=colorkey, focusable=focusable, opacity=opacity, init_image=False)
        if type(scale_boundary) == tuple:
            if 4 % len(scale_boundary) == 0:
                self.scale_boundary: Tuple[int] = scale_boundary * (4 // len(scale_boundary))
            else:
                raise ValueError('scale_boundary length should be either 1, 2, 4')
        elif type(scale_boundary) == int:
            self.scale_boundary: Tuple[int] = [scale_boundary] * 4
        elif scale_boundary == None:
            self.scale_boundary = (0, 0, 0, 0)
        else:
            raise TypeError('Unexpected scale_boundary type: ' + str(type(scale_boundary)))
        
        if scale_by != 1:
            self.scale_boundary = tuple(i * self.scale_by for i in self.scale_boundary)

        print(self.scale_boundary)

        self.init_image()


    def load_image(self):
        super().load_image()
        bn = self.scale_boundary
        ow = self.rect.w
        oh = self.rect.h
        self.interior_rect = pygame.Rect(bn[3], bn[0], ow - bn[3] - bn[1], oh - bn[0] - bn[2])
        self.corner_rects = (
            pygame.Rect(0, 0, bn[3], bn[0]) if bn[0] and bn[3] else None,
            pygame.Rect(ow - bn[1], 0, bn[1], bn[0]) if bn[0] and bn[1] else None,
            pygame.Rect(ow - bn[1], oh - bn[2], bn[1], bn[2]) if bn[1] and bn[2] else None,
            pygame.Rect(0, oh - bn[2], bn[3], bn[2]) if bn[2] and bn[3] else None,
        )

        iw = self.interior_rect.w
        ih = self.interior_rect.h
        self.edge_rects = (
            pygame.Rect(bn[3], 0, iw, bn[0]) if bn[0] else None,
            pygame.Rect(ow - bn[1], bn[0], bn[1], ih) if bn[1] else None,
            pygame.Rect(bn[3], oh - bn[2], iw, bn[2]) if bn[2] else None,
            pygame.Rect(0, bn[0], bn[3], ih) if bn[3] else None,
        )
    

    def render(self, force: bool = False):
        if not force and not self.changed:
            return
        
        self.updated = True
        self.image = pygame.Surface((self.w, self.h))
        self.image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.image.get_rect(left=self.x, top=self.y)

        bn = self.scale_boundary

        # Corners
        corner_dests = (
            (0, 0),
            (self.w - bn[1], 0),
            (self.w - bn[1], self.h - bn[2]),
            (0, self.h - bn[2]),
        )
        for i, corner_rect in enumerate(self.corner_rects):
            if corner_rect:
                self.image.blit(self.original_image, corner_dests[i], corner_rect)
        
        # Edges
        edge_sizes = (
            (self.w - bn[3] - bn[1], bn[0]),
            (bn[1], self.h - bn[0] - bn[2]),
            (self.w - bn[3] - bn[1], bn[2]),
            (bn[3], self.h - bn[0] - bn[2]),
        )
        edge_dests = (
            (bn[3], 0),
            (self.w - bn[1], bn[0]),
            (bn[3], self.h - bn[2]),
            (0, bn[0])
        )
        for i, edge_rect in enumerate(self.edge_rects):
            if edge_rect:
                edge_surf = pygame.Surface((edge_rect.w, edge_rect.h))
                edge_surf.blit(self.original_image, (0, 0), edge_rect)
                edge_surf = pygame.transform.scale(edge_surf, edge_sizes[i])
                self.image.blit(edge_surf, edge_dests[i])
        
        # Interior
        interior_size = (self.w - bn[3] - bn[1], self.h - bn[0] - bn[2])
        if interior_size[0] > 0 and interior_size[1] > 0:
            interior_surf = pygame.Surface((self.interior_rect.w, self.interior_rect.h))
            interior_surf.blit(self.original_image, (0, 0), self.interior_rect)
            interior_surf = pygame.transform.scale(interior_surf, interior_size)
            self.image.blit(interior_surf, (bn[3], bn[0]))

        self.render_opacity()
