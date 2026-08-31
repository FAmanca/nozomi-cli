# ANISUB CLI

CLI untuk streaming anime subtitle Indonesia di terminal, terinspirasi dari `ani-cli`.

```
   _   _  ___ _   _ ___ 
  /_\ | \| ||_ _/ __| | | || _ )
 / _ \| .` | | |\__ \ |_| || _ \
/_/ \_\_|\_||___|___/\___/ |___/
```

---

## Requirement

Sebelum install, pastikan sudah punya:

- **Python 3.8+**
- **MPV Player**
  - Windows: `winget install mpv.mpv`
  - Linux: `sudo apt install mpv`
  - Mac: `brew install mpv`
- **yt-dlp** (opsional, membantu MPV di beberapa format)
  - `winget install yt-dlp` / `pip install yt-dlp`

---

## Instalasi

### Via pip (direkomendasikan)

**Dari GitHub langsung:**
```bash
pip install git+https://github.com/USERNAME/anisub.git
```

**Dari folder lokal:**
```bash
pip install .
```

Setelah install, langsung jalankan dari terminal mana saja:
```bash
anisub
```

### Tanpa install (jalankan langsung)

```bash
git clone https://github.com/USERNAME/anisub.git
cd anisub
pip install -r requirements.txt
python main.py
```

---

## Fitur

- Cari dan tonton anime Sub Indo langsung dari terminal
- Riwayat tontonan — lanjut dari episode terakhir dengan mudah
- Auto lanjut ke episode berikutnya setelah selesai menonton
- Simpan preferensi kualitas video (360p / 480p / 720p) sebagai default
- Cache hasil pencarian per sesi (hemat request)
- Rate limit otomatis 20 request/menit agar tidak diblokir server
- Navigasi kembali di setiap tahap
- Cross-platform: Windows, Linux, Mac

---

## Data User

Semua data disimpan di folder `~/.anisub/`:

| File | Isi |
|------|-----|
| `~/.anisub/history.json` | Riwayat tontonan (maks 30 entri) |
| `~/.anisub/user_config.json` | Preferensi kualitas video |

---

## Struktur Project

| File | Fungsi |
|------|--------|
| `main.py` | Entry point & logika alur utama |
| `api.py` | Request ke API anime (+ rate limiter & cache) |
| `config.py` | Konfigurasi URL base API |
| `history.py` | Manajemen riwayat tontonan |
| `user_config.py` | Manajemen preferensi user |
