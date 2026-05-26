from song import Song

class Playlist:
    """Class untuk mengelola struktur Doubly Circular Linked List"""
    def __init__(self):
        self.head = None
        self.tail = None

    def get_length(self):
        if self.head is None: return 0
        count = 1
        temp = self.head
        while temp.next != self.head:
            count += 1
            temp = temp.next
        return count

    def is_db_id_exist(self, target_db_id):
        """Mengecek apakah lagu dari database sudah ada di dalam playlist"""
        if self.head is None: return False
        temp = self.head
        while True:
            if temp.db_id == target_db_id: return True
            temp = temp.next
            if temp == self.head: break
        return False

    def is_song_exist(self, target_playlist_id):
        """Mencari node lagu berdasarkan Playlist ID (Untuk fitur delete)"""
        if self.head is None: return False
        temp = self.head
        while True:
            if temp.playlist_id == target_playlist_id: return True
            temp = temp.next
            if temp == self.head: break
        return False

    def add_song(self, db_id, title, artist, duration):
        """Menambahkan lagu dengan logika Doubly Circular"""
        # Pengamanan ganda untuk mencegah duplikasi
        if self.is_db_id_exist(db_id):
            return None
            
        # Membuat Node baru (Playlist ID otomatis digenerate di dalam class Song)
        new_song = Song(db_id, title, artist, duration)

        if self.head is None:
            # Jika kosong, head dan tail menunjuk ke diri sendiri (Circular)
            self.head = new_song
            self.tail = new_song
            new_song.next = self.head
            new_song.prev = self.tail
        else:
            # Kaitkan lagu baru di belakang tail saat ini
            new_song.prev = self.tail
            new_song.next = self.head
            
            # Perbarui pointer tail lama dan head agar menunjuk ke lagu baru
            self.tail.next = new_song
            self.head.prev = new_song
            
            # Pindahkan status tail ke lagu baru
            self.tail = new_song

        return new_song

    def delete_song(self, target_playlist_id):
        """Menghapus node dengan memperbaiki sinkronisasi next dan prev"""
        if self.head is None: return

        current_node = self.head
        # Cari node yang akan dihapus menggunakan Playlist ID
        while current_node.playlist_id != target_playlist_id:
            current_node = current_node.next
            if current_node == self.head:
                return # Tidak ditemukan

        # Kasus 1: Jika hanya ada 1 lagu di playlist
        if self.head == self.tail:
            self.head = None
            self.tail = None
            
        # Kasus 2: Menghapus Head
        elif current_node == self.head:
            self.head = self.head.next
            self.head.prev = self.tail
            self.tail.next = self.head
            
        # Kasus 3: Menghapus Tail
        elif current_node == self.tail:
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail
            
        # Kasus 4: Menghapus node di tengah
        else:
            current_node.prev.next = current_node.next
            current_node.next.prev = current_node.prev

    def get_song_by_position(self, position):
        if self.head is None: return None
        temp = self.head
        count = 1
        while True:
            if count == position: return temp
            temp = temp.next
            count += 1
            if temp == self.head: break
        return None

    def display_playlist(self, current_song, is_playing, is_paused):
        if self.head is None:
            print("\n[!] Playlist kosong.")
            return

        print("\n========================= PLAYLIST =========================")
        temp = self.head
        no = 1
        while True:
            menit = temp.duration // 60
            detik = temp.duration % 60
            status = ""
            if temp == current_song:
                if is_paused: status = " [PAUSED]"
                elif is_playing: status = " [PLAYING]"

            # Format Output
            print(f"{no}. [Playlist ID:{temp.playlist_id}] {temp.title} - {temp.artist} ({menit}:{detik:02d}){status}")

            temp = temp.next
            no += 1
            if temp == self.head: break
        print("============================================================")
