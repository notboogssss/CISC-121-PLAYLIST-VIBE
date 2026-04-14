import copy
from typing import Any, Dict, List, Tuple

import gradio as gr

Song = Dict[str, Any]

DEFAULT_SONGS: List[Song] = [
    {"title": "Midnight Drive", "artist": "Nova Lane", "energy": 82, "duration": 214},
    {"title": "Cloud Sneakers", "artist": "The Skylines", "energy": 61, "duration": 189},
    {"title": "Static Hearts", "artist": "Echo Bloom", "energy": 94, "duration": 242},
    {"title": "Slow Orbit", "artist": "Velvet North", "energy": 37, "duration": 276},
    {"title": "Neon Letters", "artist": "Juniper Hall", "energy": 73, "duration": 201},
    {"title": "Golden Signals", "artist": "Atlas Run", "energy": 55, "duration": 233},
]


def safe_text(value: Any) -> str:
    """Escape text for safe HTML display."""
    text = str(value)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def parse_playlist_data(text: str) -> List[Song]:
    """Parse the textarea into a list of song dictionaries.

    Expected format:
    title | artist | energy | duration
    """
    songs: List[Song] = []
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]

    if not lines:
        raise ValueError("Please enter at least one song.")

    for line_number, line in enumerate(lines, start=1):
        parts = [part.strip() for part in line.split("|")]
        if len(parts) != 4:
            raise ValueError(
                f"Line {line_number} must have exactly 4 parts: title | artist | energy | duration"
            )

        title, artist, energy_text, duration_text = parts

        if not title or not artist:
            raise ValueError(f"Line {line_number} is missing a title or artist.")

        try:
            energy = int(energy_text)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: energy must be an integer.") from exc

        try:
            duration = int(duration_text)
        except ValueError as exc:
            raise ValueError(f"Line {line_number}: duration must be an integer number of seconds.") from exc

        if not 0 <= energy <= 100:
            raise ValueError(f"Line {line_number}: energy must be between 0 and 100.")

        if duration <= 0:
            raise ValueError(f"Line {line_number}: duration must be greater than 0.")

        songs.append(
            {
                "title": title,
                "artist": artist,
                "energy": energy,
                "duration": duration,
            }
        )

    return songs


def format_duration(seconds: int) -> str:
    minutes = seconds // 60
    remaining = seconds % 60
    return f"{minutes}:{remaining:02d}"


def song_label(song: Song) -> str:
    return (
        f"{song['title']} — {song['artist']} | "
        f"Energy: {song['energy']} | Duration: {format_duration(song['duration'])}"
    )


def merge_sort_with_steps(songs: List[Song], key: str) -> Tuple[List[Song], List[Dict[str, Any]]]:
    """Sort songs using merge sort while recording visualization steps."""
    working = [dict(song) for song in songs]
    steps: List[Dict[str, Any]] = []

    def merge_sort(items: List[Song], left_index: int) -> List[Song]:
        if len(items) <= 1:
            return items

        midpoint = len(items) // 2
        left_half = merge_sort(items[:midpoint], left_index)
        right_half = merge_sort(items[midpoint:], left_index + midpoint)
        return merge(left_half, right_half, left_index)

    def merge(left_half: List[Song], right_half: List[Song], start_index: int) -> List[Song]:
        merged: List[Song] = []
        left_pointer = 0
        right_pointer = 0

        while left_pointer < len(left_half) and right_pointer < len(right_half):
            left_song = left_half[left_pointer]
            right_song = right_half[right_pointer]

            steps.append(
                {
                    "type": "compare",
                    "left_index": start_index + left_pointer,
                    "right_index": start_index + len(left_half) + right_pointer,
                    "message": (
                        f"Compare {left_song['title']} ({key}={left_song[key]}) with "
                        f"{right_song['title']} ({key}={right_song[key]})."
                    ),
                    "snapshot": copy.deepcopy(working),
                }
            )

            if left_song[key] <= right_song[key]:
                chosen = left_song
                left_pointer += 1
            else:
                chosen = right_song
                right_pointer += 1

            merged.append(chosen)

        while left_pointer < len(left_half):
            merged.append(left_half[left_pointer])
            left_pointer += 1

        while right_pointer < len(right_half):
            merged.append(right_half[right_pointer])
            right_pointer += 1

        for offset, song in enumerate(merged):
            working[start_index + offset] = song
            steps.append(
                {
                    "type": "write",
                    "index": start_index + offset,
                    "message": (
                        f"Place {song['title']} into position {start_index + offset + 1} "
                        f"for this merged section."
                    ),
                    "snapshot": copy.deepcopy(working),
                }
            )

        return merged

    sorted_songs = merge_sort(working, 0)
    steps.append(
        {
            "type": "done",
            "message": f"Sorting complete. Playlist is now ordered by {key}.",
            "snapshot": copy.deepcopy(sorted_songs),
        }
    )
    return sorted_songs, steps


def build_visual_html(songs: List[Song], key: str, step: Dict[str, Any] | None = None) -> str:
    boxes: List[str] = []
    highlighted_positions = set()
    compare_positions = set()

    if step:
        if step.get("type") == "compare":
            compare_positions.update({step.get("left_index"), step.get("right_index")})
        elif step.get("type") == "write":
            highlighted_positions.add(step.get("index"))

    for index, song in enumerate(songs):
        value = song[key]
        if key == "duration":
            value_display = format_duration(value)
            bar_width = min(100, max(15, int((value / 300) * 100)))
        else:
            value_display = str(value)
            bar_width = min(100, max(15, value))

        border = "#cbd5e1"
        background = "#ffffff"
        if index in compare_positions:
            border = "#f59e0b"
            background = "#fffbeb"
        elif index in highlighted_positions:
            border = "#10b981"
            background = "#ecfdf5"

        boxes.append(
            f"""
            <div style="border:2px solid {border}; background:{background}; border-radius:12px; padding:12px; margin-bottom:10px;">
                <div style="font-weight:700;">{index + 1}. {safe_text(song['title'])}</div>
                <div>{safe_text(song['artist'])}</div>
                <div style="margin-top:6px;">Energy: {song['energy']} | Duration: {format_duration(song['duration'])}</div>
                <div style="margin-top:8px; font-size:14px;">{safe_text(key.title())}: <strong>{safe_text(value_display)}</strong></div>
                <div style="margin-top:6px; width:100%; background:#e5e7eb; border-radius:999px; height:12px; overflow:hidden;">
                    <div style="height:12px; width:{bar_width}%; background:#6366f1;"></div>
                </div>
            </div>
            """
        )

    return "<div>" + "".join(boxes) + "</div>"


def build_step_table(steps: List[Dict[str, Any]]) -> List[List[str]]:
    rows: List[List[str]] = []
    for index, step in enumerate(steps, start=1):
        rows.append([str(index), step["type"].title(), step["message"]])
    return rows


def run_sort(playlist_text: str, sort_key: str):
    try:
        songs = parse_playlist_data(playlist_text)
    except ValueError as error:
        return (
            f"❌ {error}",
            "<p>Please fix the input and try again.</p>",
            [],
            "",
        )

    sorted_songs, steps = merge_sort_with_steps(songs, sort_key)
    preview_step = steps[0] if steps else None

    summary_lines = [
        f"✅ Sorted {len(sorted_songs)} songs by {sort_key} using merge sort.",
        f"Total visualization steps recorded: {len(steps)}",
        "Top 3 after sorting:",
    ]

    for song in sorted_songs[:3]:
        summary_lines.append(f"• {song_label(song)}")

    return (
        "\n".join(summary_lines),
        build_visual_html(preview_step["snapshot"] if preview_step else sorted_songs, sort_key, preview_step),
        build_step_table(steps),
        "\n".join(song_label(song) for song in sorted_songs),
    )


def load_example_playlist() -> str:
    return "\n".join(
        f"{song['title']} | {song['artist']} | {song['energy']} | {song['duration']}"
        for song in DEFAULT_SONGS
    )


def add_song(
    playlist_text: str,
    title: str,
    artist: str,
    energy: int,
    duration: int,
):
    title = title.strip()
    artist = artist.strip()

    if not title or not artist:
        return playlist_text, "Please enter both a title and an artist before adding a song."

    if not 0 <= int(energy) <= 100:
        return playlist_text, "Energy must be between 0 and 100."

    if int(duration) <= 0:
        return playlist_text, "Duration must be greater than 0 seconds."

    new_line = f"{title} | {artist} | {int(energy)} | {int(duration)}"
    if playlist_text.strip():
        updated = playlist_text.strip() + "\n" + new_line
    else:
        updated = new_line

    return updated, f"Added: {title} by {artist}."


with gr.Blocks(title="Playlist Vibe Builder - Merge Sort Visualizer") as demo:
    gr.Markdown(
        """
        # Playlist Vibe Builder
        Sort a playlist by **energy** or **duration** using **merge sort**.

        **Input format:** one song per line using:
        `title | artist | energy | duration_in_seconds`

        Example: `Midnight Drive | Nova Lane | 82 | 214`
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            playlist_box = gr.Textbox(
                label="Playlist Data",
                lines=12,
                value=load_example_playlist(),
            )
            sort_key = gr.Radio(
                choices=["energy", "duration"],
                value="energy",
                label="Sort Key",
            )

            with gr.Accordion("Add a new song", open=False):
                new_title = gr.Textbox(label="Song Title")
                new_artist = gr.Textbox(label="Artist")
                new_energy = gr.Slider(0, 100, value=50, step=1, label="Energy Score")
                new_duration = gr.Number(value=200, precision=0, label="Duration (seconds)")
                add_status = gr.Textbox(label="Add Song Status", interactive=False)
                add_button = gr.Button("Add Song")

            with gr.Row():
                example_button = gr.Button("Reload Example Data")
                sort_button = gr.Button("Run Merge Sort")

        with gr.Column(scale=1):
            summary_output = gr.Textbox(label="Summary", lines=8, interactive=False)
            visualization_output = gr.HTML(label="Visualization")
            sorted_playlist_output = gr.Textbox(
                label="Sorted Playlist",
                lines=10,
                interactive=False,
            )

    step_table = gr.Dataframe(
        headers=["Step", "Action", "Explanation"],
        datatype=["str", "str", "str"],
        row_count=(0, "dynamic"),
        col_count=(3, "fixed"),
        label="Algorithm Steps",
        interactive=False,
        wrap=True,
    )

    sort_button.click(
        fn=run_sort,
        inputs=[playlist_box, sort_key],
        outputs=[summary_output, visualization_output, step_table, sorted_playlist_output],
    )

    example_button.click(fn=load_example_playlist, inputs=None, outputs=playlist_box)

    add_button.click(
        fn=add_song,
        inputs=[playlist_box, new_title, new_artist, new_energy, new_duration],
        outputs=[playlist_box, add_status],
    )


if __name__ == "__main__":
    demo.launch()
