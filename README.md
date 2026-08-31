# anisub

CLI untuk streaming anime subtitle Indonesia di terminal.

```
   _   _  _  ___ _   _ ___ 
  /_\ | \| ||_ _/ __| | | || _ )
 / _ \| .` | | |\__ \ |_| || _ \
/_/ \_\_|\_||___|___/\___/ |___/
```

---

## Requirement

- Python 3.8+
- MPV Player

| OS | Install MPV |
|----|------------|
| Windows | `winget install mpv.mpv` |
| Linux (Arch) | `sudo pacman -S mpv` |
| Linux (Ubuntu) | `sudo apt install mpv` |
| Mac | `brew install mpv` |

---

## Instalasi

### Windows

```bash
pip install git+https://github.com/FAmanca/anisub.git
```

Jalankan:
```bash
anisub
```

### Linux / Mac

```bash
pipx install git+https://github.com/FAmanca/anisub.git
```

Install pipx jika belum ada:

| OS | Command |
|----|---------|
| Arch | `sudo pacman -S python-pipx` |
| Ubuntu/Debian | `sudo apt install pipx` |
| Mac | `brew install pipx` |

Jalankan:
```bash
anisub
```

### Tanpa install (jalankan dari source)

```bash
git clone https://github.com/FAmanca/anisub.git
cd anisub
pip install -r requirements.txt
python main.py
```

---

## Fitur

- Cari dan tonton anime Sub Indo langsung dari terminal
- Riwayat tontonan — lanjut dari episode terakhir
- Auto lanjut ke episode berikutnya setelah selesai menonton
- Navigasi kembali di setiap tahap
- Cache hasil pencarian per sesi
- Rate limit otomatis (20 req/menit)
- Cross-platform: Windows, Linux, Mac

---

## Data

Semua data disimpan di `~/.anisub/`:

| File | Isi |
|------|-----|
| `history.json` | Riwayat tontonan (maks 30 entri) |
