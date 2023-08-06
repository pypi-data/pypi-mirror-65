from dataclasses import dataclass

import cv2


@dataclass
class TargetArea:
    corner_1: (int, int)
    corner_2: (int, int)
    midi_nr: int
    is_active: bool=False

    def get_sorted_cords(self):
        xmin, xmax = sorted((self.corner_1[0], self.corner_2[0]))
        ymin, ymax = sorted((self.corner_1[1], self.corner_2[1]))
        return (xmin, ymin), (xmax, ymax)

class AreaManager:

    def __init__(self):
        self.areas = []
        self._selected_area_id = None
        self.area_being_created = None
        self.selected_area = None

    def on_mouse_event(self, event, x, y):
        if self.area_being_created is not None:
            self.area_being_created.corner_2 = (x, y)
            if event == cv2.EVENT_LBUTTONUP:
                self.areas.append(self.area_being_created)
                self.area_being_created = None
        else:
            if event == cv2.EVENT_LBUTTONDOWN:
                self.unselect()
                self.start_area_creation(x, y)

    def start_area_creation(self, x, y):
        midi_no = 80 # first generic use on/off
        while midi_no in [a.midi_nr for a in self.areas]:
            midi_no += 1
        self.area_being_created = TargetArea((x,y), (x,y), midi_no)

    def unselect(self):
        self.selected_area = None
        self._selected_area_id = None

    def select_next(self):
        if not self.areas:
            return
        if self.selected_area is None:
            self._selected_area_id = -1
        self._selected_area_id = (self._selected_area_id+1) % len(self.areas)
        self.selected_area = self.areas[self._selected_area_id]

    def delete_selected(self):
        if self._selected_area_id is None:
            return
        del self.areas[self._selected_area_id]
        self.unselect()
