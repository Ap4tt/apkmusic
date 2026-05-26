import os
import time
from database_song import SONG_DATABASE
from playlist import Playlist
from player import Player
from utils import input_integer, input_string

os.system('') # Inisialisasi ANSI Colors untuk Windows

def display_database():
    print("\n================ DATABASE LAGU INTERNAL ================")
    for db_song in SONG_DATABASE:
        m = db_song['duration'] // 60
        s = db_song['duration'] % 60
        print(f"[DB ID:{db_song['db_id']}] {db_song['title']} - {db_song['artist']} ({m}:{s:02d})")
    print("========================================================")

def find_song_in_db(search_key):
    for song in SONG_DATABASE:
        if str(song['db_id']) == search_key or song['title'].lower() == search_key.lower():
            return song
    return None

def main():
    playlist = Playlist()
    player = Player(playlist)

    print("\n[Sistem] Menyiapkan playlist otomatis dari Database...")
    song1 = find_song_in_db("101")
    if song1: playlist.add_song(song1['db_id'], song1['title'], song1['artist'], song1['duration'])
    
    song2 = find_song_in_db("102")
    if song2: playlist.add_song(song2['db_id'], song2['title'], song2['artist'], song2['duration'])

    while True:
        if not player.is_playing:
            print("\n=============================================")
            print("            MUSIC PLAYER PLAYLIST")
            print("=============================================")
            print("1. Tambah Lagu dari Database")
            print("2. Tampilkan Playlist")
            print("3. Play")
            print("4. Pause")
            print("5. Resume")
            print("6. Previous Song")
            print("7. Next Song")
            print("8. Repeat ON/OFF")
            print("9. Delete Lagu")
            print("0. Keluar")
            choice = input("Pilih menu: ").strip()
        else:
            print("\n---------------------------------------------------------")
            print(" [Status Pemutar Real-Time]")
            choice = input(" KONTROL -> (4 Pause, 5 Resume, 6 Prev, 7 Next, 8 Repeat, 9 Delete, 0 Stop): ").strip()

        if choice == "1":
            display_database()
            search_key = input_string("Masukkan DB ID Lagu ATAU Judul Lagu (Ketik 'batal' untuk kembali): ")
            if search_key.lower() == 'batal':
                continue
                
            db_song = find_song_in_db(search_key)
            if db_song:
                if playlist.is_db_id_exist(db_song['db_id']):
                    print(f"\n[!] '{db_song['title']}' [DB ID:{db_song['db_id']}] SUDAH ADA di playlist.")
                else:
                    new_song = playlist.add_song(db_song['db_id'], db_song['title'], db_song['artist'], db_song['duration'])
                    print(f"\n[+] '{db_song['title']}' berhasil ditambahkan! [ID:{new_song.playlist_id}]")
            else:
                print(f"\n[!] Lagu dengan pencarian '{search_key}' tidak ditemukan di Database.")

        elif choice == "2":
            playlist.display_playlist(player.current, player.is_playing, player.is_paused)

        elif choice == "3":
            if playlist.head is None:
                print("\n[!] Playlist kosong.")
                continue
            length = playlist.get_length()
            nomor = input_integer(f"Mulai dari lagu keberapa (1-{length}): ", min_val=1)
            if nomor > length:
                print(f"\n[!] Playlist hanya memiliki {length} lagu.")
            else:
                song_to_play = playlist.get_song_by_position(nomor)
                player.play_from_song(song_to_play)

        elif choice == "4":
            if not player.is_playing: print("\n[!] Tidak ada lagu yang sedang diputar.")
            else: player.pause_song()
                
        elif choice == "5":
            if not player.is_playing: print("\n[!] Tidak ada lagu yang sedang diputar.")
            else: player.resume_song()
                
        elif choice == "6":
            if not player.is_playing: print("\n[!] Tidak ada lagu yang sedang diputar.")
            else: player.previous_song()
                
        elif choice == "7":
            if not player.is_playing: print("\n[!] Tidak ada lagu yang sedang diputar.")
            else: player.next_song()
                
        elif choice == "8":
            player.toggle_repeat()

        elif choice == "9":
            if playlist.head is None:
                print("\n[!] Playlist kosong.")
                continue
            
            playlist.display_playlist(player.current, player.is_playing, player.is_paused)
            target_id = input_integer("\nMasukkan Playlist ID lagu yang ingin dihapus (0 untuk batal): ", min_val=0)
            if target_id == 0: continue

            if playlist.is_song_exist(target_id):
                # Amankan pointer jika lagu yang dihapus sedang diputar
                is_current = (player.current and player.current.playlist_id == target_id)
                if is_current:
                    was_tail = (player.current == playlist.tail)
                    next_node = player.current.next

                playlist.delete_song(target_id)
                print(f"\n[-] Lagu [Playlist ID:{target_id}] berhasil dihapus!")

                # Alihkan pemutar otomatis jika lagunya terhapus
                if is_current:
                    player.is_playing = False
                    time.sleep(0.3)
                    if playlist.head is None:
                        player.stop_player()
                    elif was_tail and not player.repeat:
                        player.stop_player()
                    else:
                        player.play_from_song(next_node)
            else:
                print(f"\n[!] Playlist ID [{target_id}] tidak ditemukan di playlist saat ini.")

        elif choice == "0":
            if player.is_playing:
                player.stop_player()
                print("\n[+] Musik dihentikan.")
            else:
                print("\nKeluar program...")
                break
        else:
            print("\n[!] Menu tidak valid.")

if __name__ == "__main__":
    main()