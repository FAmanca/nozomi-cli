# nozomi-cli

CLI untuk streaming anime subtitle Indonesia di terminal.

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

Menggunakan `uv` (Direkomendasikan):
```bash
uv tool install git+https://github.com/FAmanca/nozomi-cli.git
```

Atau menggunakan `pip`:
```bash
pip install git+https://github.com/FAmanca/nozomi-cli.git
```

Jalankan:
```bash
nozomi-cli
```

### Linux / Mac

```bash
pipx install git+https://github.com/FAmanca/nozomi-cli.git
```

Install pipx jika belum ada:

| OS | Command |
|----|---------|
| Arch | `sudo pacman -S python-pipx` |
| Ubuntu/Debian | `sudo apt install pipx` |
| Mac | `brew install pipx` |

Jalankan:
```bash
nozomi-cli
```

### Tanpa install (jalankan dari source)

```bash
git clone https://github.com/FAmanca/nozomi-cli.git
cd nozomi-cli
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

Semua data disimpan di `~/.nozomi/`:

| File | Isi |
|------|-----|
| `history.json` | Riwayat tontonan (maks 30 entri) |
