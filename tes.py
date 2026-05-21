import time
import threading
import os

# Menginisialisasi dukungan ANSI Escape Codes pada terminal (khusus Windows)
os.system('')

class Song:
    def __init__(self, title, artist, duration):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.next = None

class MusicPlayerPlaylist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

        self.is_playing = False
        self.is_paused = False
        self.repeat = False
        self.current_time = 0
        self.manual_skip = False

    # ====================================
    # UTILITY: VALIDASI DATA LINKED LIST
    # ====================================
    def get_length(self):
        """Menghitung jumlah lagu dalam playlist"""
        if self.head is None:
            return 0
        count = 1
        temp = self.head
        while temp.next != self.head:
            count += 1
            temp = temp.next
        return count

    def is_song_exist(self, title):
        """Mengecek apakah lagu dengan judul tertentu ada di playlist"""
        if self.head is None:
            return False
        temp = self.head
        while True:
            if temp.title.lower() == title.lower():
                return True
            temp = temp.next
            if temp == self.head:
                break
        return False

    # ====================================
    # TAMBAH LAGU
    # ====================================
    def add_song(self, title, artist, duration):
        new_song = Song(title, artist, duration)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            new_song.next = self.head
        else:
            self.tail.next = new_song
            self.tail = new_song
            self.tail.next = self.head

        print(f"\n[+] Lagu '{title}' oleh '{artist}' berhasil ditambahkan!")

    # ====================================
    # DISPLAY PLAYLIST
    # ====================================
    def display_playlist(self):
        if self.head is None:
            print("\n[!] Playlist kosong.")
            return

        print("\n==================== PLAYLIST ====================")
        temp = self.head
        no = 1

        while True:
            menit = temp.duration // 60
            detik = temp.duration % 60
            status = ""

            if temp == self.current:
                if self.is_paused:
                    status = " [PAUSED]"
                elif self.is_playing:
                    status = " [PLAYING]"

            print(f"{no}. {temp.title} - {temp.artist} ({menit}:{detik:02d}){status}")

            temp = temp.next
            no += 1
            if temp == self.head:
                break
        print("==================================================")

    # ====================================
    # PLAY DARI NOMOR
    # ====================================
    def play_from_song(self, position):
        if self.is_playing:
            self.is_playing = False
            time.sleep(0.3)

        temp = self.head
        count = 1

        while True:
            if count == position:
                self.current = temp
                break
            temp = temp.next
            count += 1
            if temp == self.head:
                break

        self.play_song()

    # ====================================
    # PLAY SONG (THREAD STARTER)
    # ====================================
    def play_song(self):
        self.is_playing = True
        self.is_paused = False
        self.manual_skip = False

        thread = threading.Thread(target=self.run_player)
        thread.daemon = True
        thread.start()

    # ====================================
    # ENGINE PLAYER (THREAD RUNNER)
    # ====================================
    def run_player(self):
        while self.is_playing and self.current is not None:
            song = self.current
            self.current_time = 0

            while self.current_time < song.duration:
                if not self.is_playing:
                    return

                if self.manual_skip:
                    self.manual_skip = False
                    self.is_paused = False
                    if song == self.tail and not self.repeat:
                        self.clear_status_line("Playlist Selesai")
                        self.is_playing = False
                        self.current = None
                        return
                    else:
                        self.current = song.next
                        break

                if self.is_paused:
                    self.update_status_display(song, "PAUSED")
                    time.sleep(0.2)
                    continue

                self.update_status_display(song, "PLAYING")
                time.sleep(1)
                
                if self.is_playing and not self.is_paused and not self.manual_skip:
                    self.current_time += 1
            else:
                if not self.manual_skip:
                    if song == self.tail:
                        if self.repeat:
                            self.current = self.head
                        else:
                            self.clear_status_line("Selesai")
                            self.is_playing = False
                            self.current = None
                            print(f"\n\nLagu '{song.title}' selesai. Playlist telah berakhir.")
                            return
                    else:
                        self.current = song.next

    # ====================================
    # REAL-TIME UI UPDATE
    # ====================================
    def update_status_display(self, song, status):
        menit_jalan = self.current_time // 60
        detik_jalan = self.current_time % 60
        menit_total = song.duration // 60
        detik_total = song.duration % 60
        repeat_status = "ON" if self.repeat else "OFF"

        status_line = f" [{status}] {song.title} - {song.artist} [{menit_jalan}:{detik_jalan:02d} / {menit_total}:{detik_total:02d}] | Repeat: {repeat_status}"
        print(f"\033[s\033[A\r\033[K{status_line}\033[u", end="", flush=True)

    def clear_status_line(self, message):
        print(f"\033[s\033[A\r\033[K [{message}]\033[u", end="", flush=True)

    # ====================================
    # KONTROL PEMUTAR
    # ====================================
    def pause_song(self):
        if self.is_playing: self.is_paused = True

    def resume_song(self):
        if self.is_playing and self.is_paused: self.is_paused = False

    def next_song(self):
        if self.is_playing: self.manual_skip = True

    def toggle_repeat(self):
        self.repeat = not self.repeat

    def stop_player(self):
        self.is_playing = False
        self.is_paused = False
        self.current = None

    # ====================================
    # HAPUS LAGU
    # ====================================
    def delete_song(self, title):
        current_node = self.head
        prev_node = self.tail

        while True:
            if current_node.title.lower() == title.lower():
                break
            prev_node = current_node
            current_node = current_node.next

        is_deleting_current = (current_node == self.current)

        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.current = None
            self.is_playing = False
        else:
            if current_node == self.head:
                self.head = self.head.next
                self.tail.next = self.head
                if is_deleting_current: self.current = self.head
            elif current_node == self.tail:
                prev_node.next = self.head
                self.tail = prev_node
                if is_deleting_current:
                    self.current = self.head if self.repeat else None
                    if not self.repeat: self.is_playing = False
            else:
                prev_node.next = current_node.next
                if is_deleting_current: self.current = current_node.next

        print(f"\n[-] Lagu '{current_node.title}' berhasil dihapus!")
        if is_deleting_current and self.is_playing:
            print("[Sistem] Mengalihkan pemutar ke lagu berikutnya...")
            self.play_song()


# ====================================
# FUNGSI BANTUAN VALIDASI INPUT
# ====================================
def input_integer(prompt, min_val):
    """
    Validasi agar user wajib memasukkan angka (integer).
    Mencegah error ValueError (crash) jika user memasukkan huruf.
    """
    while True:
        try:
            val = int(input(prompt))
            if val < min_val:
                print(f"  [!] Invalid: Angka tidak boleh kurang dari {min_val}.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid: Masukkan format angka yang benar (contoh: 1, 2, 3).")

def input_string(prompt):
    """Validasi agar string tidak boleh dikosongkan (hanya enter/spasi)"""
    while True:
        val = input(prompt).strip()
        if not val:
            print("  [!] Invalid: Input tidak boleh kosong.")
            continue
        return val


# ====================================
# MAIN INTERFACE LOOP
# ====================================
playlist = MusicPlayerPlaylist()

while True:
    if not playlist.is_playing:
        print("\n=============================================")
        print("            MUSIC PLAYER PLAYLIST")
        print("=============================================")
        print("1. Tambah Lagu")
        print("2. Tampilkan Playlist")
        print("3. Play Dari Lagu Keberapa")
        print("8. Hapus Lagu")
        print("0. Keluar")
        choice = input("Pilih menu: ").strip()
    else:
        # UI khusus saat memutar lagu (mencegah user input menu lain saat play)
        print("\n--------------------------------------------------")
        print(" [Status Pemutar Real-Time]")
        choice = input(" KONTROL -> (4:Pause, 5:Resume, 6:Next, 7:Repeat, 0:Stop): ").strip()

    # Evaluasi Pilihan Menu (Beserta Validasi)
    if choice == "1":
        title = input_string("Judul lagu  : ")
        artist = input_string("Nama artist : ")
        menit = input_integer("Durasi menit: ", min_val=0)
        detik = input_integer("Durasi detik: ", min_val=0)
        
        playlist.add_song(title, artist, (menit * 60) + detik)

    elif choice == "2":
        playlist.display_playlist()

    elif choice == "3":
        if playlist.head is None:
            print("\n[!] Playlist kosong. Silakan tambah lagu terlebih dahulu.")
            continue
            
        length = playlist.get_length()
        while True:
            nomor = input_integer("Mulai dari lagu keberapa: ", min_val=1)
            if nomor > length:
                print(f"  [!] Nomor tidak valid. Playlist hanya memiliki {length} lagu.")
            else:
                playlist.play_from_song(nomor)
                break

    elif choice == "4":
        playlist.pause_song()
    elif choice == "5":
        playlist.resume_song()
    elif choice == "6":
        playlist.next_song()
    elif choice == "7":
        playlist.toggle_repeat()

    elif choice == "8":
        if playlist.head is None:
            print("\n[!] Playlist kosong. Tidak ada lagu yang bisa dihapus.")
            continue
            
        while True:
            title = input("Masukkan judul lagu yang ingin dihapus (ketik 'batal' untuk kembali): ").strip()
            if title.lower() == 'batal':
                print("\nBatal menghapus lagu.")
                break
            if not title:
                print("  [!] Input tidak boleh kosong.")
                continue

            if playlist.is_song_exist(title):
                playlist.delete_song(title)
                break
            else:
                print(f"  [!] Lagu '{title}' tidak ditemukan di playlist. Coba lagi.")

    elif choice == "0":
        if playlist.is_playing:
            playlist.stop_player()
            print("\n[+] Musik dihentikan.")
        else:
            print("\nTerima kasih telah menggunakan Music Player Playlist.")
            break
            
    else:
        print("\n[!] Pilihan menu tidak valid. Silakan coba lagi.")
