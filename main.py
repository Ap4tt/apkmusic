import os
from playlist import Playlist
from player import Player
from utils import format_duration
from database_song import SONG_DATABASE

os.system('')

USERNAME    = "123"
PASSWORD    = "123"
MAX_ATTEMPT = 5

def login():
    chance = MAX_ATTEMPT
    while chance > 0:
        print("\n--- LOGIN ---")
        u = input("Username: ").strip()
        p = input("Password: ").strip()
        if u == USERNAME and p == PASSWORD:
            print("\n[+] Login Berhasil!\n")
            return True
        chance -= 1
        print("\n[!] Username/Password Salah.")
    print("\n[!] Gagal. Program Ditutup.")
    return False

def show_database(database):
    print("\n═══════════════ DATABASE LAGU ═══════════════")
    for song in database:
        print(f"  {song['db_id']}. {song['title']} - {song['artist']} "
              f"({format_duration(song['duration'])})")
    print("═══════════════════════════════════════════\n")


def search_in_database(database, query):
    query = query.strip()
    for song in database:
        if query.isdigit() and song["db_id"] == int(query):
            return song
        if song["title"].lower() == query.lower():
            return song
    return None

def search_playlist(playlists, query):
    query = query.strip()
    if query.isdigit():
        index = int(query)
        if 1 <= index <= len(playlists):
            return playlists[index - 1]
        return None
    for pl in playlists:
        if pl.name.lower() == query.lower():
            return pl
    return None


def choose_playlist(playlists, prompt="Pilih Playlist "):
    print("\n═════ DAFTAR PLAYLIST ═════")
    for i, pl in enumerate(playlists, start=1):
        print(f"  {i}. {pl.name} ({pl.count()} lagu)")
    print("════════════════════════════\n")
    query = input(f"{prompt}: ").strip()
    pl = search_playlist(playlists, query)
    if pl is None:
        print("\n[!] Playlist Tidak Ditemukan.")
        return None
    return pl


def add_song_to_playlist(database, playlists):
    show_database(database)

    query = input("Pilih Lagu Dari Database: ").strip()
    song = search_in_database(database, query)
    if song is None:
        print(f"\n[!] Lagu '{query}' Tidak Ditemukan di Database.")
        return

    print("\n═════ PILIH PLAYLIST TUJUAN ═════")
    for i, pl in enumerate(playlists, start=1):
        print(f"{i}. {pl.name} ({pl.count()} lagu)")
    print(f"{len(playlists) + 1}. Buat Playlist Baru")
    print("════════════════════════════════\n")
    aim = input("Pilih Playlist Tujuan: ").strip()

    is_new = (aim.isdigit() and int(aim) == len(playlists) + 1) or \
              (aim.lower() == "buat playlist baru")
    
    if is_new:
        nama = input("Nama Playlist Baru: ").strip()
        target = Playlist(nama)
        playlists.append(target)
    else:
        target = search_playlist(playlists, aim)
        if target is None:
            print("\n[!] Playlist Tidak Ditemukan.\n")
            return

    if target.find_node(song["title"]) is not None:
        print(f"\n[!] '{song['title']}' Sudah Ada di Playlist '{target.name}'.")
        return

    target.add_song(song["title"], song["artist"], song["duration"])
    print(f"\n[+] '{song['title']}' Berhasil Ditambahkan ke '{target.name}'!")


def delete_song_from_playlist(playlists, player):
    if not playlists:
        print("\n[!] Belum Ada Playlist.")
        return

    chosen = choose_playlist(playlists, "Pilih Playlist Yang Ingin Dihapus Isinya")
    if chosen is None:
        return
    if chosen.head is None:
        print(f"\n[!] Playlist '{chosen.name}' Kosong.")
        return

    is_active = (chosen == player.playlist)
    chosen.display(player.current if is_active else None,
                    player.is_playing if is_active else False,
                    player.is_paused if is_active else False)

    query  = input("Pilih Lagu Yang Ingin Dihapus: ").strip()
    target = chosen.find(query)
    if target is None:
        print(f"\n[!] Lagu '{query}' Tidak Ditemukan di '{chosen.name}'.")
        return
    
    is_current = is_active and (player.current == target)
    next_node  = target.next
    is_tail    = (target == chosen.tail)

    if is_current:
        player.stop()

    chosen.delete_song(target)
    print(f"\n[-] '{target.title}' Berhasil Dihapus dari '{chosen.name}'!")

    if is_current and chosen.head is not None:
        if not (is_tail and not player.repeat):
            player.play(next_node)


def delete_playlist(playlists, player):
    if not playlists:
        print("\n[!] Belum Ada Playlist.")
        return

    chosen = choose_playlist(playlists, "Pilih Playlist Yang Ingin Dihapus ")
    if chosen is None:
        return

    if chosen == player.playlist and player.is_playing:
        player.stop()
        print("\n[+] Musik Dihentikan Karena Playlist Aktif Dihapus.")

    playlists.remove(chosen)
    print(f"\n[-] Playlist '{chosen.name}' Berhasil Dihapus!")


def menu_utama():
    items = [
        "1. Lihat Database Lagu",
        "2. Tambah Lagu ke Playlist",
        "3. Lihat Playlist",
        "4. Putar Playlist",
        "5. Hapus Lagu dari Playlist",
        "6. Hapus Playlist",
        "7. Keluar",
    ]
    width = max(len(i) for i in items) + 4
    print("\n╔" + "═" * width + "╗")
    print("║" + "MUSIC PLAYER ".center(width) + "║")
    print("╠" + "═" * width + "╣")
    for i in items:
        print("║  " + i.ljust(width - 2) + "║")
    print("╚" + "═" * width + "╝")
    return input("Pilih: ").strip()


def menu_playing(player):
    player.playlist.display(player.current, player.is_playing, player.is_paused)
    print("─" * 56)
    return input("3.Pause  4.Resume  5.Previous  6.Next  7.Repeat  8.Lihat Playlist  9.Hapus Lagu  0.Stop: ").strip()


def main():
    if not login():
        return

    playlists = [Playlist("Favorit")]  
    player    = Player()

    while True:
        if player.is_playing:
            choice = menu_playing(player)
            if choice == "2":
                add_song_to_playlist(SONG_DATABASE, playlists)

            elif choice == "3":
                if player.is_paused:
                    print("\n[!] Lagu Sudah Dalam Kondisi Pause.")
                else:
                    player.pause()

            elif choice == "4":
                if not player.is_paused:
                    print("\n[!] Lagu Sudah Sedang Diputar.")
                else:
                    player.resume()

            elif choice == "5":
                player.prev_song()

            elif choice == "6":
                player.next_song()

            elif choice == "7":
                player.toggle_repeat()
                print(f"\n[!] Repeat: {'ON' if player.repeat else 'OFF'}")

            elif choice == "8":
                if not playlists:
                    print("\n[!] Belum Ada Playlist.")
                else:
                    pl = choose_playlist(playlists, "Pilih Playlist Yang Ingin Dilihat")
                    if pl is not None:
                        if pl == player.playlist:
                            pl.display(player.current, player.is_playing, player.is_paused)
                        else:
                            pl.display()
                input("\nTekan ENTER Untuk Kembali ke Player...")
                
            elif choice == "9":
                delete_song_from_playlist(playlists, player)

            elif choice == "0":
                player.stop()
                print("\n[+] Musik Dihentikan.")

            else:
                print("\n[!] Menu tidak valid.")
                
        else:
            choice = menu_utama()

            if choice == "1":
                show_database(SONG_DATABASE)

            elif choice == "2":
                add_song_to_playlist(SONG_DATABASE, playlists)

            elif choice == "3":
                if not playlists:
                    print("\n[!] Belum Ada Playlist.")
                else:
                    pl = choose_playlist(playlists, "Pilih Playlist Yang Ingin Dilihat ")
                    if pl is not None:
                        pl.display()

            elif choice == "4":
                if not playlists:
                    print("\n[!] Belum Ada Playlist.")
                else:
                    pl = choose_playlist(playlists, "Pilih Playlist Yang Ingin Diputar")
                    if pl is not None:
                        if pl.head is None:
                            print(f"\n[!] Playlist '{pl.name}' Kosong.")
                        else:
                            player.play_playlist(pl)

            elif choice == "5":
                delete_song_from_playlist(playlists, player)

            elif choice == "6":
                delete_playlist(playlists, player)

            elif choice == "7":
                print("\n[!] Keluar Program...")
                break

            else:
                print("\n[!] Menu Tidak Valid.")


if __name__ == "__main__":
    main()
