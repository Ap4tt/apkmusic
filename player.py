import time
import threading
from utils import format_duration

class Player:
    def __init__(self):
        self.playlist     = None     # playlist AKTIF (yang baru/sedang diputar)
        self.current      = None     # node yang sedang diputar
        self.is_playing   = False    # status player
        self.is_paused    = False    # status pause
        self.repeat       = False    # repeat on/off
        self.manual_skip  = False    # sinyal next dari user
        self.manual_prev  = False    # sinyal prev dari user

    def _join_thread(self):
        thread = getattr(self, '_thread', None)
        if thread and thread.is_alive():
            thread.join()

    def play_playlist(self, playlist, song=None):
        """Jadikan `playlist` sebagai playlist aktif, lalu mulai memutar."""
        self.playlist = playlist
        self.play(song)

    def play(self, song=None):
        if self.playlist is None:
            return
        if song is None:
            song = self.playlist.head
        if song is None:
            return

        if self.is_playing:
            self.is_playing = False
            self._join_thread()

        self.current      = song
        self.is_playing   = True
        self.is_paused    = False
        self.manual_skip  = False
        self.manual_prev  = False

        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def pause(self):
        if self.is_playing:
            self.is_paused = True

    def resume(self):
        if self.is_playing and self.is_paused:
            self.is_paused = False

    def next_song(self):
        if self.is_playing and self.current:
            self.manual_skip = True

    def prev_song(self):
        if self.is_playing and self.current:
            self.manual_prev = True

    def toggle_repeat(self):
        self.repeat = not self.repeat

    def stop(self):
        self.is_playing = False
        self.is_paused  = False
        self.current    = None
        self._join_thread()

    def run(self):
        while self.is_playing and self.current is not None:
            song = self.current
            self.current_time = 0

            while self.current_time < song.duration:
                if not self.is_playing or self.current != song:
                    return

                # Handle skip manual (Next)
                if self.manual_skip:
                    self.manual_skip = False
                    self.is_paused   = False
                    if song == self.playlist.tail and not self.repeat:
                        self._clear("Playlist Selesai")
                        self.is_playing = False
                        self.current    = None
                        return
                    self.current = song.next
                    break

                # Handle prev manual (Previous)
                if self.manual_prev:
                    self.manual_prev = False
                    self.is_paused   = False
                    if song != self.playlist.head or self.repeat:
                        self.current = song.prev
                    break

                # Pause — tunggu resume
                if self.is_paused:
                    self.current_display(song, "PAUSED")
                    time.sleep(0.2)
                    continue

                # Playing normal
                self.current_display(song, "PLAYING")
                time.sleep(1)
                if self.is_playing and not self.is_paused and \
                   not self.manual_skip and not self.manual_prev:
                    self.current_time += 1

            else:
                # Lagu habis secara alami
                if self.manual_skip or self.manual_prev:
                    continue
                if song == self.playlist.tail:
                    if self.repeat:
                        self.current = self.playlist.head
                    else:
                        self._clear("Selesai")
                        self.is_playing = False
                        self.current    = None
                        print(f"\n\nLagu '{song.title}' Selesai. Playlist Berakhir.")
                        return
                else:
                    self.current = song.next

    def current_display(self, song, status):
        line = (
            f" [{status}] {self.playlist.name} » {song.title} - {song.artist} "
            f"[{format_duration(self.current_time)}/{format_duration(song.duration)}] "
            f"| Repeat: {'ON' if self.repeat else 'OFF'}"
        )
        print(f"\033[s\033[A\r\033[K{line}\033[u", end="", flush=True)

    def _clear(self, message):
        print(f"\033[s\033[A\r\033[K [{message}]\033[u", end="", flush=True)
