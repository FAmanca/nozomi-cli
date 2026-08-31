from InquirerPy import prompt
from api import search, get_episode, get_qualities, resolve_stream
from history import load_history, save_history, clear_history
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import subprocess
import sys

console = Console()

BANNER = r"""
   _   _  _  ___ _   _ ___ 
  /_\ | \| ||_ _/ __| | | || _ )
 / _ \| .` | | |\__ \ |_| || _ \
/_/ \_\_|\_||___|___/\___/ |___/
"""

def show_banner():
    console.print(Panel(
        Text(BANNER.strip(), style="bold cyan", justify="center"),
        subtitle="[dim]streaming anime sub indo[/dim]",
        border_style="cyan",
        padding=(0, 2),
    ))
    console.print()

def get_player_path() -> str:
    return "mpv"

def play(episode_href: str, episode_name: str, anime_name: str, anime_href: str) -> str:
    with console.status("[cyan]Mengambil kualitas video...[/cyan]"):
        quality_choices = get_qualities(episode_href)

    if not quality_choices:
        console.print("[red]Video tidak tersedia untuk episode ini.[/red]")
        return "back"

    res_q = prompt([{
        "type": "list",
        "message": "Pilih Kualitas:",
        "name": "quality",
        "choices": [{"name": "[ Kembali ke Pilih Episode ]", "value": "BACK"}] + quality_choices,
    }])
    if res_q["quality"] == "BACK":
        return "back"

    urls = res_q["quality"]
    chosen_quality_name = next((q["name"] for q in quality_choices if q["value"] == urls), "")

    selected_url = next(
        (u["url"] for u in urls if "pdrain" in u["title"].lower() or "pixeldrain" in u["title"].lower()),
        None
    )
    if not selected_url:
        selected_url = urls[0]["url"]
        console.print(f"[yellow]PDrain tidak tersedia, mencoba {urls[0]['title']}...[/yellow]")

    with console.status("[cyan]Menyiapkan stream...[/cyan]"):
        stream_url = resolve_stream(selected_url)

    save_history({
        "anime_name": anime_name,
        "anime_href": anime_href,
        "episode_name": episode_name,
        "episode_href": episode_href,
        "quality": chosen_quality_name,
    })

    console.print(f"\n[bold green]Memutar:[/bold green] [cyan]{episode_name}[/cyan] [dim]({chosen_quality_name})[/dim]\n")

    try:
        subprocess.run([get_player_path(), stream_url])
        console.print("[green]Selesai menonton.[/green]\n")
    except FileNotFoundError:
        console.print("[red]Error: MPV tidak ditemukan![/red]")
        console.print("[dim]Install MPV: winget install mpv.mpv  /  sudo apt install mpv  /  brew install mpv[/dim]\n")
        return "done"

    return "ask_next"


def watch_session(anime_name: str, anime_href: str, eps_list: list):
    eps_choices = [{"name": "[ Kembali ke Pilih Anime ]", "value": "BACK"}] + eps_list

    while True:
        res_eps = prompt([{"type": "list", "message": "Pilih Episode:", "name": "episode", "choices": eps_choices}])
        if res_eps["episode"] == "BACK":
            return

        current_idx = next((i for i, e in enumerate(eps_list) if e["value"] == res_eps["episode"]), None)

        while current_idx is not None:
            ep = eps_list[current_idx]
            result = play(ep["value"], ep["name"], anime_name, anime_href)

            if result == "back":
                break

            if result == "ask_next":
                has_next = current_idx + 1 < len(eps_list)
                if has_next:
                    next_ep = eps_list[current_idx + 1]
                    res_next = prompt([{
                        "type": "confirm",
                        "message": f"Lanjut ke '{next_ep['name']}'?",
                        "name": "next",
                        "default": True,
                    }])
                    if res_next["next"]:
                        current_idx += 1
                        continue
                break

            break


def flow_search():
    while True:
        res_name = prompt([{"type": "input", "message": "Cari Judul Anime (kosongkan untuk kembali):", "name": "name"}])
        name = res_name.get("name", "").strip()
        if not name:
            return

        with console.status(f"[cyan]Mencari '{name}'...[/cyan]"):
            anime_choices = search(name)

        if not anime_choices:
            console.print("[red]Anime tidak ditemukan atau terjadi kesalahan jaringan.[/red]\n")
            continue

        console.print(f"[dim]Ditemukan {len(anime_choices)} hasil.[/dim]")
        anime_choices_prompt = [{"name": "[ Kembali ke Pencarian ]", "value": "BACK"}] + anime_choices

        while True:
            res_anime = prompt([{"type": "list", "message": "Pilih Anime:", "name": "anime", "choices": anime_choices_prompt}])
            if res_anime["anime"] == "BACK":
                break

            with console.status("[cyan]Mengambil daftar episode...[/cyan]"):
                eps_list = get_episode(res_anime["anime"])

            if not eps_list:
                console.print("[red]Daftar episode gagal dimuat.[/red]\n")
                continue

            anime_name = next((a["name"] for a in anime_choices if a["value"] == res_anime["anime"]), "")
            console.print(f"[dim]{len(eps_list)} episode tersedia.[/dim]")
            watch_session(anime_name, res_anime["anime"], eps_list)


def flow_history():
    history = load_history()
    if not history:
        console.print("[yellow]Riwayat tontonan kosong.[/yellow]\n")
        return

    history_choices = [{"name": "[ Kembali ]", "value": "BACK"}] + [
        {"name": f"{h['anime_name']}  |  {h['episode_name']}", "value": h}
        for h in history
    ]
    history_choices.append({"name": "[ Hapus Semua Riwayat ]", "value": "CLEAR"})

    res = prompt([{"type": "list", "message": "Riwayat Tontonan:", "name": "entry", "choices": history_choices}])
    entry = res["entry"]

    if entry == "BACK":
        return
    if entry == "CLEAR":
        res_confirm = prompt([{"type": "confirm", "message": "Yakin ingin menghapus semua riwayat?", "name": "ok", "default": False}])
        if res_confirm["ok"]:
            clear_history()
            console.print("[green]Riwayat dihapus.[/green]\n")
        return

    with console.status("[cyan]Mengambil daftar episode...[/cyan]"):
        eps_list = get_episode(entry["anime_href"])

    if not eps_list:
        console.print("[red]Gagal memuat episode.[/red]\n")
        return

    last_idx = next((i for i, e in enumerate(eps_list) if e["value"] == entry["episode_href"]), None)

    options = [{"name": "[ Kembali ]", "value": "BACK"}]
    if last_idx is not None and last_idx + 1 < len(eps_list):
        next_ep = eps_list[last_idx + 1]
        options.append({"name": f"Lanjutkan -> {next_ep['name']}", "value": "NEXT"})
    options.append({"name": "Ulangi episode ini", "value": "REPLAY"})
    options.append({"name": "Pilih episode lain", "value": "BROWSE"})

    res_action = prompt([{"type": "list", "message": f"Terakhir ditonton: {entry['episode_name']}", "name": "action", "choices": options}])
    action = res_action["action"]

    if action == "BACK":
        return
    elif action == "NEXT":
        current_idx = last_idx + 1
        while current_idx is not None and current_idx < len(eps_list):
            ep = eps_list[current_idx]
            result = play(ep["value"], ep["name"], entry["anime_name"], entry["anime_href"])
            if result == "ask_next" and current_idx + 1 < len(eps_list):
                next_ep = eps_list[current_idx + 1]
                res_next = prompt([{"type": "confirm", "message": f"Lanjut ke '{next_ep['name']}'?", "name": "next", "default": True}])
                if res_next["next"]:
                    current_idx += 1
                    continue
            break
    elif action == "REPLAY":
        play(entry["episode_href"], entry["episode_name"], entry["anime_name"], entry["anime_href"])
    elif action == "BROWSE":
        watch_session(entry["anime_name"], entry["anime_href"], eps_list)


def start():
    show_banner()

    while True:
        history = load_history()

        main_menu = [{"name": "Cari Anime", "value": "search"}]
        if history:
            main_menu.append({"name": f"Riwayat Tontonan  ({len(history)} entri)", "value": "history"})
        main_menu.append({"name": "Keluar", "value": "exit"})

        res = prompt([{"type": "list", "message": "Menu Utama:", "name": "menu", "choices": main_menu}])

        if res["menu"] == "search":
            flow_search()
        elif res["menu"] == "history":
            flow_history()
        elif res["menu"] == "exit":
            console.print("\n[cyan]Sampai jumpa![/cyan]\n")
            break

if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        console.print("\n[dim]Keluar dari program...[/dim]")
        sys.exit(0)