from Xlib import display

class XInfo(object):
    def __init__(self):
        self.__display = display.Display()
    def Width  (self, screen=None): return self.__display.screen(screen).width_in_pixels
    def Height (self, screen=None): return self.__display.screen(screen).height_in_pixels
    def Screens(self)             : return self.__display.screen_count()
    def Screen (self)             : return self.__display.get_default_screen()

    def WarpPointer(self, xpos, ypos, screen=None):
        self.__display.screen(screen).root.warp_pointer(xpos, ypos)
        # 20081105: Xlib is broken - Pointer doesn't warp until queried
        self.__display.screen(screen).root.query_pointer().root_x
# vim:set ts=4 sw=4 et nu:
