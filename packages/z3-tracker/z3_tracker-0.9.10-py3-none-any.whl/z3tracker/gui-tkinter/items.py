'''
Item display
'''

import tkinter as tk
import tkinter.ttk as ttk
import typing

from ..config import CONFIG
from .. import items

from . import misc

__all__ = 'start',


class ItemWindow(tk.Toplevel):
    '''
    Inventory item display

    Instance variables:
        tracker: item tracker object
        layout: item layout in display
        helpertext: helper text variable
        scaling: scaling factor of individual buttons
        buttons: {'item identifier': button object}
    '''

    def __init__(self, tracker: items.ItemTracker):
        '''
        Args:
            tracker: item tracker object
        '''

        super().__init__()
        self.title('Items')

        self.tracker = tracker

        self.frame = ttk.Frame(self)
        self.frame.grid(column=0, row=0, sticky=misc.A)
        self.helpertext = tk.StringVar()
        self.helper = ttk.Label(
            self, textvariable=self.helpertext)
        self.helper.grid(column=0, row=1, sticky=tk.S)

        self.scaling = _scale_factors()

        self.buttons = {}
        for item in self.tracker:
            if (
                    self.tracker[item].location and
                    self.tracker[item].displayname and
                    self.tracker[item].icon):
                self._item_display(self.tracker[item])

    def _item_display(self, item) -> None:
        '''
        Make and place single item display object.

        Args:
            item: item object
        Writes:
            buttons
        '''

        button = ItemButton(item, self.frame, self.scaling)
        button.bind(
            '<Enter>', lambda _: self.helpertext.set(item.display()))
        button.bind(
            '<Leave>', lambda _: self.helpertext.set(''))
        button.bind('<ButtonRelease-1>', item.increase)
        button.bind('<ButtonRelease-3>', item.decrease)
        button.bind(
            '<ButtonRelease-1>',
            lambda _: self.helpertext.set(item.display()),
            add='+')
        button.bind(
            '<ButtonRelease-3>',
            lambda _: self.helpertext.set(item.display()),
            add='+')
        button.bind(
            '<ButtonRelease-1>',
            lambda _: self.tracker.save(),
            add='+')
        button.bind(
            '<ButtonRelease-3>',
            lambda _: self.tracker.save(),
            add='+')
        button.bind(
            '<ButtonRelease-1>',
            lambda _: button.check_state(item),
            add='+')
        button.bind(
            '<ButtonRelease-3>',
            lambda _: button.check_state(item),
            add='+')
        button.grid(column=item.location[1], row=item.location[0])
        self.buttons[item.identifier] = button
        

    def reset(self) -> None:
        '''
        Reset items to default.
        '''

        self.tracker.reset()
        for item in self.tracker:
            if self.tracker[item].icon:
                self.buttons[item].check_state(self.tracker[item])


class ItemButton(tk.Canvas):
    '''
    Single item display object.
    '''

    def __init__(
            self, item, parent: ttk.Frame, scaling: (int, int)):
        '''
        item: item object
        parent: parent widget for object
        scaling: button up- and downscale
        '''

        super().__init__(
            parent, height=64 * scaling[0] / scaling[1],
            width=64 * scaling[0] / scaling[1])
        self.scaling = scaling
        self.img = None
        self.icon = None
        self.check_state(item)

    def check_state(self, item) -> None:
        '''
        Check button state and make adjustments if necessary.

        Args:
            item: item object
        '''        

        self.delete(self.img)
        icon = tk.PhotoImage(
            file=item.icon[item.index()], master=self.master)
        if self.scaling[0] != 1:
            icon = icon.zoom(self.scaling[0], self.scaling[0])
        if self.scaling[1] != 1:
            icon = icon.subsample(self.scaling[1], self.scaling[1])
        if not item.state():
            for x in range(icon.width()):
                for y in range(icon.height()):
                    bw = sum(icon.get(x, y)) // item.disabled[0]
                    if bw in (0, 255):
                        continue
                    bw *= item.disabled[1]
                    bw = 255 if bw > 255 else int(bw)
                    icon.put('#{0:02x}{0:02x}{0:02x}'.format(bw), (x, y))
        self.img = self.create_image(0, 0, anchor=tk.NW, image=icon)
        self.icon = icon


def _scale_factors() -> (int, int):
    '''
    Calculate up- and downscale factor.

    Returns:
        int: upscale factor
        int: downscale factor
    '''

    scaling = CONFIG['icon_size']
    for up in range(1, 1000):
        if not (scaling * up) % 1:
            upscale = int(scaling * up)
            downscale = up
            break
    else:
        CONFIG.set('icon_size', 1)
        assert False
    return upscale, downscale


def start(worldtracker) -> ItemWindow:
    '''
    Initialise item tracker window.

    Args:
        worldtracker: world state tracker
    '''

    return ItemWindow(items.ItemTracker(worldtracker))
