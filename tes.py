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
    # TAMBAH LAGU
    # ====================================
    def add_song(self, title, artist, duration):
        new_song = Song(title, artist, duration)
        if self.head is None:
            self.head = new_song
            self.tail = new_song
            new_song.next = self.head  # Circular: menunjuk ke diri sendiri
        else:
            self.tail.next = new_song
            self.tail = new_song
            self.tail.next = self.head  # Circular: tail selalu menunjuk ke head

        print(f"\nLagu '{title}' oleh '{artist}' berhasil ditambahkan!")

    # ====================================
    # DISPLAY PLAYLIST
    # ====================================
    def display_playlist(self):
        if self.head is None:
            print("\nPlaylist kosong.")
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
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        # Jika sedang memutar, matikan thread lama terlebih dahulu secara aman
        if self.is_playing:
            self.is_playing = False
            time.sleep(0.3)

        temp = self.head
        count = 1
        found = False

        while True:
            if count == position:
                self.current = temp
                found = True
                break

            temp = temp.next
            count += 1
            if temp == self.head:
                break

        if not found:
            print("\nNomor lagu tidak valid.")
            return

        self.play_song()

    # ====================================
    # PLAY SONG (THREAD STARTER)
    # ====================================
    def play_song(self):
        if self.current is None:
            print("\nTidak ada lagu dipilih.")
            return

        self.is_playing = True
        self.is_paused = False
        self.manual_skip = False

        # Inisialisasi Thread agar UI Utama tidak membeku saat timer berjalan
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
                # Proteksi jika playlist dihentikan dari luar
                if not self.is_playing:
                    return

                # Kondisi jika lagu di-skip manual saat status Pause
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

                # Kondisi jika lagu sedang di-pause
                if self.is_paused:
                    self.update_status_display(song, "PAUSED")
                    time.sleep(0.2)
                    continue

                # Perbarui tampilan status bar real-time
                self.update_status_display(song, "PLAYING")
                
                time.sleep(1)
                
                # Tambah timer hanya jika tidak dalam kondisi skip/pause setelah jeda 1 detik
                if self.is_playing and not self.is_paused and not self.manual_skip:
                    self.current_time += 1

            else:
                # Bagian ini dieksekusi jika durasi lagu habis secara alami (bukan di-skip)
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
    # REAL-TIME UI UPDATE (ANTI-COLLISION)
    # ====================================
    def update_status_display(self, song, status):
        menit_jalan = self.current_time // 60
        detik_jalan = self.current_time % 60
        menit_total = song.duration // 60
        detik_total = song.duration % 60
        repeat_status = "ON" if self.repeat else "OFF"

        status_line = f" [{status}] {song.title} - {song.artist} [{menit_jalan}:{detik_jalan:02d} / {menit_total}:{detik_total:02d}] | Repeat: {repeat_status}"
        
        # \033[s = Simpan posisi kursor ketikan user
        # \033[A = Naikkan kursor 1 baris ke atas (area status bar)
        # \r     = Kembalikan kursor ke ujung kiri baris
        # \033[K = Bersihkan teks sisa sebelumnya pada baris tersebut
        # \033[u = Kembalikan posisi kursor asli tempat user mengetik menu
        print(f"\033[s\033[A\r\033[K{status_line}\033[u", end="", flush=True)

    def clear_status_line(self, message):
        print(f"\033[s\033[A\r\033[K [{message}]\033[u", end="", flush=True)

    # ====================================
    # KONTROL PEMUTAR
    # ====================================
    def pause_song(self):
        if not self.is_playing:
            return
        self.is_paused = True

    def resume_song(self):
        if not self.is_playing or not self.is_paused:
            return
        self.is_paused = False

    def next_song(self):
        if not self.is_playing:
            return
        self.manual_skip = True

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
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        current_node = self.head
        prev_node = self.tail
        found = False

        while True:
            if current_node.title.lower() == title.lower():
                found = True
                break
            prev_node = current_node
            current_node = current_node.next
            if current_node == self.head:
                break

        if not found:
            print("\nLagu tidak ditemukan.")
            return

        # Cek apakah lagu yang dihapus adalah lagu yang sedang aktif diputar
        is_deleting_current = (current_node == self.current)

        # Kasus 1: Hanya ada 1 lagu di playlist
        if self.head == self.tail:
            self.head = None
            self.tail = None
            self.current = None
            self.is_playing = False
        else:
            # Kasus 2: Menghapus head
            if current_node == self.head:
                self.head = self.head.next
                self.tail.next = self.head
                if is_deleting_current:
                    self.current = self.head
            # Kasus 3: Menghapus tail
            elif current_node == self.tail:
                prev_node.next = self.head
                self.tail = prev_node
                if is_deleting_current:
                    if self.repeat:
                        self.current = self.head
                    else:
                        self.current = None
                        self.is_playing = False
            # Kasus 4: Menghapus data di tengah
            else:
                prev_node.next = current_node.next
                if is_deleting_current:
                    self.current = current_node.next

        print(f"\nLagu '{current_node.title}' berhasil dihapus!")
        if is_deleting_current and self.is_playing:
            print("[Sistem] Mengalihkan pemutar ke lagu berikutnya...")
            self.play_song()


# ====================================
# MAIN INTERFACE LOOP
# ====================================
playlist = MusicPlayerPlaylist()

# Pre-populate data lagu agar user langsung bisa mencoba tanpa mengetik panjang di awal
playlist.add_song("Bohemian Rhapsody", "Queen", 15)  # disingkat untuk testing
playlist.add_song("Hati-Hati di Jalan", "Tulus", 10)
playlist.add_song("As It Was", "Harry Styles", 12)

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
        choice = input("Pilih menu: ")
    else:
        # Tampilan Menu Ringkas Khusus saat Lagu Sedang Berputar
        print("\n--------------------------------------------------")
        print(" [Status Pemutar Real-Time]") # Baris penahan tempat kedudukan ANSI pointer
        choice = input(" KONTROL -> (4:Pause, 5:Resume, 6:Next, 7:Repeat, 0:Stop): ")

    # Evaluasi Pilihan Menu
    if choice == "1":
        title = input("Judul lagu  : ")
        artist = input("Nama artist : ")
        menit = int(input("Durasi menit: "))
        detik = int(input("Durasi detik: "))
        playlist.add_song(title, artist, (menit * 60) + detik)
    elif choice == "2":
        playlist.display_playlist()
    elif choice == "3":
        nomor = int(input("Mulai dari lagu keberapa: "))
        playlist.play_from_song(nomor)
    elif choice == "4":
        playlist.pause_song()
    elif choice == "5":
        playlist.resume_song()
    elif choice == "6":
        playlist.next_song()
    elif choice == "7":
        playlist.toggle_repeat()
    elif choice == "8":
        title = input("Masukkan judul lagu yang ingin dihapus: ")
        playlist.delete_song(title)
    elif choice == "0":
        if playlist.is_playing:
            playlist.stop_player()
            print("\nMusik dihentikan.")
        else:
            print("\nTerima kasih telah menggunakan Music Player Playlist.")
            break
    else:
        print("\nPilihan tidak valid.")
