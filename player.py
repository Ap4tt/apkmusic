import time
import threading

class Player:
    """Engine player dengan multithreading dan navigasi Doubly Circular"""
    def __init__(self, playlist):
        self.playlist = playlist
        self.current = None
        self.is_playing = False
        self.is_paused = False
        self.repeat = False
        self.current_time = 0
        
        self.manual_skip = False
        self.manual_prev = False

    def play_from_song(self, song):
        if self.is_playing:
            self.is_playing = False
            time.sleep(0.3) 

        self.current = song
        self.start_playback()

    def start_playback(self):
        if self.current is None: return
        self.is_playing = True
        self.is_paused = False
        self.manual_skip = False
        self.manual_prev = False

        thread = threading.Thread(target=self.run_player)
        thread.daemon = True
        thread.start()

    def run_player(self):
        while self.is_playing and self.current is not None:
            song = self.current
            # Di sinilah lagu direset ke 0:00 setiap kali loop ini mengulang
            self.current_time = 0

            while self.current_time < song.duration:
                if not self.is_playing: return

                # Handle Next Manual
                if self.manual_skip:
                    self.manual_skip = False
                    self.is_paused = False
                    if song == self.playlist.tail and not self.repeat:
                        self.clear_status_line("Playlist Selesai")
                        self.is_playing = False
                        self.current = None
                        return
                    else:
                        self.current = song.next
                        break

                # Handle Previous Manual (Refactored ke Doubly Linked List)
                if self.manual_prev:
                    self.manual_prev = False
                    self.is_paused = False
                    
                    # === LOGIKA REVISI RESTART LAGU PERTAMA ===
                    if song == self.playlist.head and not self.repeat:
                        # Jangan ubah self.current.
                        # Kita biarkan tetap di lagu yang sama.
                        pass 
                    else:
                        # Jika aman, bergerak mundur menggunakan prev pointer
                        self.current = song.prev 
                        
                    # Break akan mengeluarkan eksekusi dari loop durasi detik.
                    # Program akan kembali ke 'self.current_time = 0' di atas.
                    break 

                # Handle Pause
                if self.is_paused:
                    self.update_status_display(song, "PAUSED")
                    time.sleep(0.2)
                    continue

                # Normal Playing
                self.update_status_display(song, "PLAYING")
                time.sleep(1)
                
                if self.is_playing and not self.is_paused and not self.manual_skip and not self.manual_prev:
                    self.current_time += 1
            else:
                # Transisi lagu otomatis (waktu habis)
                if not self.manual_skip and not self.manual_prev:
                    if song == self.playlist.tail:
                        if self.repeat:
                            self.current = self.playlist.head
                        else:
                            self.clear_status_line("Selesai")
                            self.is_playing = False
                            self.current = None
                            print(f"\n\nLagu '{song.title}' selesai. Playlist telah berakhir.")
                            return
                    else:
                        self.current = song.next

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

    def pause_song(self):
        if self.is_playing: self.is_paused = True

    def resume_song(self):
        if self.is_playing and self.is_paused: self.is_paused = False

    def next_song(self):
        if self.is_playing and self.current: self.manual_skip = True

    def previous_song(self):
        if self.is_playing and self.current:
            self.manual_prev = True

    def toggle_repeat(self):
        self.repeat = not self.repeat

    def stop_player(self):
        self.is_playing = False
        self.is_paused = False
        self.current = None