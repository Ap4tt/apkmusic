class Song:
    """Node untuk Doubly Circular Linked List"""
    def __init__(self, title, artist, duration):
        self.title    = title
        self.artist   = artist
        self.duration = duration
        self.next     = None
        self.prev     = None
