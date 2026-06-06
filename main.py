import os
from playlist import Playlist
from player import Player

os.system('')  # Aktifkan ANSI colors di Windows

def build_playlist():
    pl = Playlist()
    pl.add_song("A Little Piece Of Heaven", "Avenged Sevenfold", 480)
    pl.add_song("Hail To The King", "Avenged Sevenfold", 420)
    pl.add_song("Nightmare", "Avenged Sevenfold", 330)
    pl.add_song("So Far Away", "Avenged Sevenfold", 300)
    pl.add_song("Buried Alive", "Avenged Sevenfold", 360)
    return pl

def menu(is_playing):
    if not is_playing:
        print("\n╔══════════════════════════════════╗")
        print("║       MUSIC PLAYER PLAYLIST      ║")
        print("╠══════════════════════════════════╣")
        print("║  1. Tampilkan Playlist           ║")
        print("║  2. Play                         ║")
        print("║  3. Pause                        ║")
        print("║  4. Resume                       ║")
        print("║  5. Previous                     ║")
        print("║  6. Next                         ║")
        print("║  7. Repeat ON/OFF                ║")
        print("║  8. Delete Lagu                  ║")
        print("║  0. Keluar                       ║")
        print("╚══════════════════════════════════╝")
        return input("Pilih: ").strip()
    else:
        print("\n─────────────────────────────────────────────")
        print("  [Status Pemutar Real-Time]")
        return input("3 Pause  4 Resume  5 Prev  6 Next  7 Repeat  8 Delete  0 Stop: ").strip()

def main():
    playlist = build_playlist()
    player   = Player(playlist)

    while True:
        choice = menu(player.is_playing)

        # ── 1. Tampilkan Playlist ──────────────────
        if choice == "1":
            playlist.display(player.current, player.is_playing, player.is_paused)

        # ── 2. Play dari Head ─────────────────────
        elif choice == "2":
            if playlist.head is None:
                print("\n[!] Playlist kosong.")
            else:
                player.play()  # langsung dari head

        # ── 3. Pause ──────────────────────────────
        elif choice == "3":
            if not player.is_playing:
                print("\n[!] Tidak ada lagu yang sedang diputar.")
            else:
                player.pause()

        # ── 4. Resume ─────────────────────────────
        elif choice == "4":
            if not player.is_playing:
                print("\n[!] Tidak ada lagu yang sedang diputar.")
            else:
                player.resume()

        # ── 5. Previous ───────────────────────────
        elif choice == "5":
            if not player.is_playing:
                print("\n[!] Tidak ada lagu yang sedang diputar.")
            else:
                player.prev_song()

        # ── 6. Next ───────────────────────────────
        elif choice == "6":
            if not player.is_playing:
                print("\n[!] Tidak ada lagu yang sedang diputar.")
            else:
                player.next_song()

        # ── 7. Repeat ON/OFF ──────────────────────
        elif choice == "7":
            player.toggle_repeat()
            state = "ON" if player.repeat else "OFF"
            print(f"\nRepeat: {state}")

        # ── 8. Delete Lagu ────────────────────────
        elif choice == "8":
            if playlist.head is None:
                print("\n[!] Playlist kosong.")
                continue

            playlist.display(player.current, player.is_playing, player.is_paused)
            title = input("Judul lagu yang ingin dihapus: ").strip()

            target = playlist.find_node(title)
            if target is None:
                print(f"\n[!] '{title}' tidak ditemukan di playlist.")
                continue

            # Catat info SEBELUM penghapusan
            is_current = (player.current == target)
            next_node  = target.next
            is_tail    = (target == playlist.tail)

            # Jika lagu yang sedang diputar → hentikan player dulu
            if is_current:
                player.stop()

            playlist.delete_song(target)
            print(f"\n[-] '{target.title}' berhasil dihapus!")

            # Auto-play ke lagu berikutnya jika yang dihapus sedang diputar
            if is_current and playlist.head is not None:
                if not (is_tail and not player.repeat):
                    player.play(next_node)

        # ── 0. Keluar / Stop ──────────────────────
        elif choice == "0":
            if player.is_playing:
                player.stop()
                print("\n[+] Musik dihentikan.")
            else:
                print("\nKeluar program...")
                break

        else:
            print("\n[!] Menu tidak valid.")

if __name__ == "__main__":
    main()
