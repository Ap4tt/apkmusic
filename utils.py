def format_duration(seconds):
    """Mengubah detik menjadi format m:ss"""
    return f"{seconds // 60}:{seconds % 60:02d}"
