import time
import threading

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
        self.skipped = False

    # ====================================
    # TAMBAH LAGU
    # ====================================

    def add_song(self, title, artist, duration):
        new_song = Song(
            title,
            artist,
            duration
        )
        if self.head is None:
            self.head = new_song
            self.tail = new_song

            new_song.next = self.head

        else:
            self.tail.next = new_song
            self.tail = new_song

            self.tail.next = self.head

        print(f"\nLagu '{title}' berhasil ditambahkan!")

    # ====================================
    # DISPLAY PLAYLIST
    # ====================================

    def display_playlist(self):
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        print("\n========== PLAYLIST ==========")
        temp = self.head
        no = 1

        while True:
            menit = temp.duration // 60
            detik = temp.duration % 60
            status = ""

            if temp == self.current:
                status = " <-- CURRENT"
            print(
                f"{no}. "
                f"{temp.title} - {temp.artist} "
                f"({menit}:{detik:02d})"
                f"{status}"
            )

            temp = temp.next
            no += 1
            if temp == self.head:
                break

    # ====================================
    # PLAY DARI NOMOR
    # ====================================

    def play_from_song(self, position):
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        if self.is_playing:
            print("\nMusic sedang diputar.")
            return

        temp = self.head
        count = 1

        while True:
            if count == position:
                self.current = temp
                break

            temp = temp.next
            count += 1

            if temp == self.head:
                print("\nNomor lagu tidak valid.")
                return

        self.play_song()

    # ====================================
    # PLAY SONG
    # ====================================

    def play_song(self):
        if self.current is None:
            print("\nTidak ada lagu dipilih.")
            return

        self.is_playing = True
        self.is_paused = False

        thread = threading.Thread(
            target=self.run_player
        )

        thread.daemon = True
        thread.start()

    # ====================================
    # ENGINE PLAYER
    # ====================================

    def run_player(self):
        while self.is_playing:
            song = self.current
            self.current_time = 0

            print("\n===================================")
            print(f"Memutar: {song.title} - {song.artist}")
            print("===================================")

            while self.current_time < song.duration:
                # pause
                if self.is_paused:
                    time.sleep(1)
                    continue

                # next manual
                if self.manual_skip:
                    self.manual_skip = False
                    self.skipped = True
                    self.current = song.next

                    print(
                        f"\n\nNext song: "
                        f"{self.current.title}"
                    )
                    break

                menit_jalan = self.current_time // 60
                detik_jalan = self.current_time % 60
                menit_total = song.duration // 60
                detik_total = song.duration % 60

                print(
                    f"\rPLAYING | "
                    f"{song.title} "
                    f"[{menit_jalan}:{detik_jalan:02d}"
                    f" / "
                    f"{menit_total}:{detik_total:02d}]",
                    end=""
                )
                time.sleep(1)
                self.current_time += 1

            # ====================================
            # JIKA SKIP MANUAL
            # ====================================

            if self.skipped:
                self.skipped = False
                continue

            print(f"\n\nLagu '{song.title}' selesai.")

            # ====================================
            # LAGU TERAKHIR
            # ====================================

            if song == self.tail:
                # repeat ON
                if self.repeat:
                    self.current = self.head

                # repeat OFF
                else:
                    print("\nPlaylist selesai.")
                    self.is_playing = False
                    self.current = None
                    break

            # ====================================
            # NEXT OTOMATIS
            # ====================================
            
            else:
                self.current = song.next

    # ====================================
    # PAUSE
    # ====================================

    def pause_song(self):
        if not self.is_playing:
            print("\nTidak ada lagu diputar.")
            return

        if self.is_paused:
            print("\nLagu sudah dipause.")
            return

        self.is_paused = True
        print("\nLagu dipause.")

    # ====================================
    # RESUME
    # ====================================

    def resume_song(self):
        if not self.is_playing:
            print("\nTidak ada lagu diputar.")
            return
        
        if not self.is_paused:
            print("\nLagu tidak sedang pause.")
            return

        self.is_paused = False
        print("\nLagu dilanjutkan.")

    # ====================================
    # NEXT SONG
    # ====================================

    def next_song(self):
        if not self.is_playing:
            print("\nTidak ada lagu diputar.")
            return

        self.manual_skip = True

    # ====================================
    # TOGGLE REPEAT
    # ====================================

    def toggle_repeat(self):
        self.repeat = not self.repeat
        if self.repeat:
            print("\nRepeat ON")
        else:
            print("\nRepeat OFF")

    # ====================================
    # HAPUS LAGU
    # ====================================

    def delete_song(self, title):
        if self.head is None:
            print("\nPlaylist kosong.")
            return

        current = self.head
        previous = self.tail

        while True:
            if current.title.lower() == title.lower():
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                    self.current = None
                elif current == self.head:
                    self.head = self.head.next
                    self.tail.next = self.head
                elif current == self.tail:
                    previous.next = self.head
                    self.tail = previous
                else:
                    previous.next = current.next
                print(f"\nLagu '{title}' berhasil dihapus!")
                return

            previous = current
            current = current.next

            if current == self.head:
                break

        print("\nLagu tidak ditemukan.")

playlist = MusicPlayerPlaylist()

while True:
    if not playlist.is_playing:
        print("\n===================================")
        print("       MUSIC PLAYER PLAYLIST")
        print("===================================")
        print("1. Tambah Lagu")
        print("2. Tampilkan Playlist")
        print("3. Play Dari Lagu Keberapa")
        print("4. Pause Lagu")
        print("5. Resume Lagu")
        print("6. Next Lagu")
        print("7. Repeat ON/OFF")
        print("8. Hapus Lagu")
        print("0. Keluar")
    choice = input("Pilih menu: ")

    if choice == "1":
        title = input("Judul lagu  : ")
        artist = input("Nama artist : ")
        menit = int(input("Durasi menit: "))
        detik = int(input("Durasi detik: "))

        total_detik = (menit * 60) + detik
        
        playlist.add_song(
            title,
            artist,
            total_detik
        )
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
        title = input(
            "Masukkan judul lagu yang ingin dihapus: "
        )
        playlist.delete_song(title)
    elif choice == "0":
        print(
            "\nTerima kasih telah menggunakan "
            "Music Player Playlist."
        )
        break
    else:
        print("\nMenu tidak valid.")