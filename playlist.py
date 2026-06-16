from song import Song
from utils import format_duration

class Playlist:
    def __init__(self, name="Playlist"):
        self.name = name
        self.head = None
        self.tail = None

    def add_song(self, title, artist, duration):
        node = Song(title, artist, duration)

        if self.head is None:            # playlist masih kosong
            self.head = self.tail = node
            node.next = node.prev = node # circular ke diri sendiri
        else:
            node.prev       = self.tail # sambung ke belakang (tail)
            node.next       = self.head  # sambung ke depan (head)
            self.tail.next  = node # sambung tail lama ke node baru
            self.head.prev  = node # sambung head lama ke node baru
            self.tail       = node # update tail ke node baru

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

    def get_by_index(self, index):
        """Cari node berdasarkan nomor urut (1-based). Return None jika tidak ada."""
        if self.head is None or index < 1:
            return None
        cur, no = self.head, 1
        while True:
            if no == index:
                return cur
            cur = cur.next
            no += 1
            if cur == self.head:
                return None

    def find(self, query):
        """Cari lagu berdasarkan nomor urut ATAU judul, tergantung input user."""
        query = query.strip()
        if query.isdigit():
            return self.get_by_index(int(query))
        return self.find_node(query)

    def count(self):
        """Hitung jumlah lagu dalam playlist."""
        if self.head is None:
            return 0
        cur, total = self.head, 0
        while True:
            total += 1
            cur = cur.next
            if cur == self.head:
                break
        return total

    def delete_song(self, node):
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

    def display(self, current=None, is_playing=False, is_paused=False):
        if self.head is None:
            print(f"\n[!] '{self.name}' kosong.")
            return

        print(f"\n═══════════════ {self.name} ═══════════════")
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
        print("════════════════════════════════════════\n")
