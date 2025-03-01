import math

class AnimationMixin:
    def init_animation(self):
        self.original_size = (self.rect.width, self.rect.height)
        self.original_pos = (self.rect.centerx, self.rect.centery)
        self.is_animating = False
        self.animation_time = 0
        self.animation_duration = 0.4
        self.scales = {
            'normal': 1.0,
            'compress': 0.8,
            'expand': 1.1
        }

    def update_animation(self, dt):
        if not self.is_animating:
            return
            
        self.animation_time += dt
        progress = self.animation_time / self.animation_duration
        
        if progress >= 1.0:
            self.is_animating = False
            current_scale = self.scales['normal']
        else:
            if progress < 0.2:
                t = progress / 0.2
                current_scale = self._lerp(self.scales['normal'], self.scales['compress'], t)
            elif progress < 0.5:
                t = (progress - 0.2) / 0.3
                current_scale = self._lerp(self.scales['compress'], self.scales['expand'], t)
            else:
                t = (progress - 0.5) / 0.5
                current_scale = self._lerp(self.scales['expand'], self.scales['normal'], t)
        
        self.rect.width = self.original_size[0] * current_scale
        self.rect.height = self.original_size[1] * current_scale
        self.rect.centerx = self.original_pos[0]
        self.rect.centery = self.original_pos[1]
    
    def _lerp(self, start, end, t):
        return start + (end - start) * t