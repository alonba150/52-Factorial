"""
Name: Map
Author: Ran Perry
"""
import io
from tkinter import *

import tkintermapview.canvas_position_marker
from PIL import Image, ImageTk
import tkintermapview
from PROJECT.Utils.Event import Event


class Map(tkintermapview.TkinterMapView):
    def __init__(self, root, start_coords, *args, **kwargs):
        # Set TkinterMapView Settings
        super().__init__(root, corner_radius=20, *args, **kwargs)
        self.root: Tk = root

        # Initialize map and variables
        self.set_position(*start_coords)
        self.markers: [tkintermapview.canvas_position_marker.CanvasPositionMarker] = []
        self.attractions: [tkintermapview.canvas_position_marker.CanvasPositionMarker] = []
        self.marker_click_event = Event()
        self.selected_marker = None

    def add_marker(self, offer):
        """
        Adds a marker to the map following many checks according to the offer that is supplied
        :param offer: offer which the marker will be added on
        """
        marker = self.set_marker(
            float(offer['x']), float(offer['y']), text=offer['name'],
            command=lambda m: self.marker_click(m) if offer['Triggered'] else None,
            text_color="blue" if offer['Triggered'] else '#3e403e',
            marker_color_circle="#696e6a" if not offer['Triggered'] else '#eb8202' if offer['Selected'] else
            "red" if offer['Taken'] else "#508f51",
            marker_color_outside="#1e211e" if offer['Triggered'] else "#3e403e"
        )
        self.markers.append(marker)

    def remove_marker(self, marker: tkintermapview.canvas_position_marker.CanvasPositionMarker):
        """
        Removes a marker from the map
        :param marker: marker to remove
        """
        if marker not in self.markers: return
        marker.delete()
        self.markers.remove(marker)

    def update_markers(self, offers):
        """
        Updates all markers in accordance to the offers
        :param offers: offers supplied by the server
        """
        current_markers = self.markers[:]
        for offer in offers: self.add_marker(offer)
        for marker in current_markers: self.remove_marker(marker)

    def marker_click(self, marker):
        """
        Calls an event supplied by the client in case a marker has been pressed
        :param marker: marker which was clicked
        """
        self.selected_marker = marker
        self.marker_click_event(marker)

    def remove_selected(self):
        """
        Removes the selected marker by setting it to None
        """
        self.selected_marker = None

    def add_attraction(self, attraction):
        """
        Adds an attraction to the map
        :param attraction: attraction which the marker will be added on
        """
        marker = self.set_marker(
            float(attraction['x']), float(attraction['y']), text=attraction['name'],
            command=lambda m: m.hide_image(not m.image_hidden),
            text_color='blue',
            marker_color_circle="blue",
            marker_color_outside="#1e211e",
            image=ImageTk.PhotoImage(Image.open(io.BytesIO(attraction['image'])).resize((200, 200))),
            image_zoom_visibility=(0, float('inf'))
        )
        marker.hide_image(True)
        self.attractions.append(marker)

    def remove_attraction(self, attraction: tkintermapview.canvas_position_marker.CanvasPositionMarker):
        """
        Removes an attraction from the map
        :param attraction: attraction to remove
        """
        if attraction not in self.attractions: return
        attraction.delete()
        self.attractions.remove(attraction)

    def update_attractions(self, attractions):
        """
        Updates all markers in accordance to the attractions
        :param attractions: attractions supplied by the server
        """
        current_attractions = self.attractions[:]
        for attraction in attractions: self.add_attraction(attraction)
        for marker in current_attractions: self.remove_attraction(marker)
