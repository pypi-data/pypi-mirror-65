import cv2
import webbrowser

from blacksock.VideoSource import VideoSource
from blacksock.AreaManager import AreaManager
from blacksock.MidiManager import MidiManager
import blacksock.ImageProcessing as ImageProcessing

BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
RED = (0, 0, 255)

KEY_UNSELECT = 27 # Esc
KEY_CAM_NEXT = 110 # n
KEY_SELECT_NEXT = 100 # d
KEY_QUIT = 113 # q
KEY_DELETE = 8 # backspace
KEY_HELP = 104 # h

class App:
    def __init__(self):
        cv2.namedWindow("main")
        cv2.setMouseCallback("main", self.on_mouse_event)
        self.midi_manager = MidiManager()
        self.video_source = VideoSource()
        self.area_manager = AreaManager()
        self.key_callbacks = {
            KEY_CAM_NEXT: self.video_source.select_next_input,
            KEY_QUIT: self.quit,
            KEY_SELECT_NEXT: self.area_manager.select_next,
            KEY_UNSELECT: self.area_manager.unselect,
            KEY_DELETE: self.area_manager.delete_selected,
            KEY_HELP: self.show_help
            }

    def on_mouse_event(self, event, x, y, flags, param):
        self.area_manager.on_mouse_event(event, x, y)

    def mainloop(self):
        while True:
            self.handle_key_input()
            frame = self.video_source.get_frame()
            self.check_area_events(frame)
            self.render_areas(frame)
            cv2.imshow("main", frame)

    def handle_key_input(self):
        c = cv2.waitKey(1)
        if c > 0:
            print(c)
        self.key_callbacks.get(c, lambda: None)()

    def render_areas(self, frame):
        for area in self.area_manager.areas:
            co1, co2 = area.get_sorted_cords()
            color = GREEN
            if area == self.area_manager.selected_area:
                color = RED
            elif area.is_active:
                color = BLUE
            cv2.rectangle(frame, co1, co2, color=color, thickness=3)
            cv2.putText(frame, str(area.midi_nr), co1,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)

        if self.area_manager.area_being_created is not None:
            co1, co2 = self.area_manager.area_being_created.get_sorted_cords()
            cv2.rectangle(frame, co1, co2, color=GREEN, thickness=3)


    def check_area_events(self, frame):
        for area in self.area_manager.areas:
            is_active = ImageProcessing.area_is_active(area, frame)
            if area.is_active != is_active:
                if is_active:
                    self.midi_manager.turn_on(area.midi_nr)
                else:
                    self.midi_manager.turn_off(area.midi_nr)
                area.is_active = is_active

    def show_help(self):
        webbrowser.open("docs/help.html", new=2)

    def quit(self):
        self.video_source.release_input()
        cv2.destroyAllWindows()
        exit(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()
