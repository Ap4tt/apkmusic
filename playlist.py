from song import Song
from utils import format_duration

class Playlist:
    """Doubly Circular Linked List untuk menyimpan antrian lagu"""

    def __init__(self):
        self.head = None
        self.tail = None

    def add_song(self, title, artist, duration):
        """Tambah node baru di akhir linked list"""
        node = Song(title, artist, duration)

        if self.head is None:
            # Circular self-reference saat playlist masih kosong
            self.head = self.tail = node
            node.next = node.prev = node
        else:
            # Sambungkan node baru di belakang tail
            node.prev       = self.tail
            node.next       = self.head
            self.tail.next  = node
            self.head.prev  = node
            self.tail       = node

        return node

    def find_node(self, title):
        """Cari node berdasarkan judul (case-insensitive). Return None jika tidak ada."""
        if self.head is None:
            return None
        cur = self.head
        while True:
            if cur.title.lower() == title.lower():
                return cur
            cur = cur.next
            if cur == self.head:
                break
        return None

    def delete_song(self, node):
        """
        Hapus node yang sudah diketahui dari linked list.
        Menerima objek Song langsung (bukan judul) agar caller bisa
        mengambil node.next sebelum penghapusan untuk kebutuhan auto-play.
        """
        if self.head is None:
            return

        # Kasus 1: satu-satunya lagu
        if self.head == self.tail:
            self.head = self.tail = None
            return

        # Kasus 2: hapus head
        if node == self.head:
            self.head       = node.next
            self.head.prev  = self.tail
            self.tail.next  = self.head
            return

        # Kasus 3: hapus tail
        if node == self.tail:
            self.tail       = node.prev
            self.tail.next  = self.head
            self.head.prev  = self.tail
            return

        # Kasus 4: hapus node tengah
        node.prev.next = node.next
        node.next.prev = node.prev

    def display(self, current, is_playing, is_paused):
        if self.head is None:
            print("\n[!] Playlist kosong.")
            return

        print("\n═══════════════════ PLAYLIST ═══════════════════")
        cur, no = self.head, 1
        while True:
            status = ""
            if cur == current:
                status = " [PAUSED]" if is_paused else " [PLAYING]" if is_playing else ""
            print(f"  {no}. {cur.title} - {cur.artist} ({format_duration(cur.duration)}){status}")
            cur = cur.next
            no += 1
            if cur == self.head:
                break
        print("═════════════════════════════════════════════════\n")
