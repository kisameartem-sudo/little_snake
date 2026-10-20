

class SnakeRenderer:
    def __init__(self, surface, cell_size, num_cells):
        self.surface = surface
        self.cell_size = cell_size
        self.num_cells = num_cells

    def get_state(self,seg_prev, seg_cur, seg_next):
        """Определяем состояние сегментов тела"""
        prev_state = 'vert' if seg_prev[0] == seg_cur[0] else 'hor'
        next_state = 'vert' if seg_next[0] == seg_cur[0] else 'hor'
        if prev_state == next_state:
            cur_state = prev_state
        else:
            prev_state = self.get_side(seg_cur, seg_prev)
            next_state = self.get_side(seg_cur, seg_next)
            cur_state = 'corner'
        return prev_state, cur_state, next_state

    def get_side(self, cur, neighbour):
        """Определяем направление сегментов для угла"""
        if cur[0] == neighbour[0]:
            return 'UP' if (cur[1] - neighbour[1]) % self.num_cells == 1 else 'DOWN'
        else:
            return 'LEFT' if (cur[0] - neighbour[0]) % self.num_cells == 1 else 'RIGHT'