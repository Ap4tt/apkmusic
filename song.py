class Song:
    """Class Node untuk Doubly Circular Linked List"""
    def __init__(self, db_id, title, artist, duration):
        # Menyimpan referensi ID Database aslinya
        self.db_id = db_id
        self.playlist_id = db_id + 1000
        
        self.title = title
        self.artist = artist
        self.duration = duration
        
        # Doubly Linked List memiliki 2 arah pointer
        self.next = None
        self.prev = None
