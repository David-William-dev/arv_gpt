import os
import tempfile
import requests
import flet as ft
from flet_audio import Audio
from config import API_BASE_URL
from gtts import gTTS
import re

def chat_screen(page: ft.Page):
    """Creates a chat interface using the Flet framework with enhanced audio features."""
    temp_dir = os.environ.get("FLET_APP_STORAGE_TEMP", "storage/temp")
    page.bgcolor = ft.Colors.BLACK
    
    # Set global Colors based on theme
    text_color = ft.Colors.WHITE
    input_color = text_color
    icon_color = text_color

    user_token = page.session.get("user_token")
    language = page.session.get("language") or "en"

    chat_messages = ft.Column(scroll=True, expand=True, spacing=10)
    active_audio_buttons = {}
    temp_audio_files = []

    def calculate_width(text, max_width=0.75):
        length_factor = min(max(0.3, len(text) * 0.02), max_width)
        return page.width * length_factor

    def send_message(e):
        """Handles sending user messages and receiving AI responses."""
        user_input_text = user_input.value.strip()
        if not user_input_text:
            return
        user_input.value = ""
        page.update()

        chat_messages.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(
                            user_input_text, color=text_color, selectable=True
                        ),
                        padding=ft.padding.all(12),
                        bgcolor="#075e54",
                        border_radius=ft.border_radius.all(15),
                        alignment=ft.alignment.center_right,
                        width=calculate_width(user_input_text),
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=4,
                            color=ft.Colors.BLACK12,
                            offset=ft.Offset(0, 2),
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        )
        page.update()
        chat_messages.scroll_to(offset=chat_messages.height, duration=300)

        typing_indicator = ft.Row(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.ProgressRing(width=16, height=16, stroke_width=2),
                            ft.Text(
                                "AI is thinking...",
                                italic=True,
                                color=text_color,
                                size=14,
                                weight=ft.FontWeight.W_400,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.all(12),
                    bgcolor= "#203936",
                    border_radius=ft.border_radius.all(15),
                    alignment=ft.alignment.center_left,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        chat_messages.controls.append(typing_indicator)
        page.update()
        chat_messages.scroll_to(offset=chat_messages.height, duration=300)

        fetch_response(user_input_text, typing_indicator)

    def fetch_response(user_input_text, typing_indicator):
        """Fetch response from API synchronously"""
        try:
            response = requests.post(
                f"{API_BASE_URL}/chat_ai/",
                json={"message": user_input_text, "language": language},
                headers={"Authorization": f"Token {user_token}"},
                timeout=30,
            )
            ai_response = (
                response.json().get("response", "Error: No response")
                if response.status_code == 200
                else f"Error: Server returned {response.status_code}"
            )
        except Exception as e:
            ai_response = f"Error: Could not connect to server. {str(e)}"
        handle_ai_response(typing_indicator, ai_response)
        page.update()

    def handle_ai_response(typing_indicator, ai_response):
        """Handle the AI response after it's received"""
        if typing_indicator in chat_messages.controls:
            chat_messages.controls.remove(typing_indicator)

        message_id = f"msg_{len(chat_messages.controls)}"
        audio_button = ft.IconButton(
            icon=ft.Icons.VOLUME_UP,
            icon_color=icon_color,
            tooltip="Generate and play audio",
            data=message_id,
        )

        active_audio_buttons[message_id] = {"button": audio_button, "text": ai_response}
        audio_button.on_click = lambda e: toggle_audio_playback(e.control.data)

        ai_text_container = ft.Row(
            [
                ft.Container(
                    content=ft.Markdown(
                        ai_response,
                        selectable=True,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_FLAVORED,
                        code_theme="atom-one-dark",
                    ),
                    padding=ft.padding.all(16),
                    bgcolor="#203936",
                    border_radius=ft.border_radius.all(15),
                    alignment=ft.alignment.center_left,
                    width=calculate_width(ai_response, 0.85),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.BLACK12,
                        offset=ft.Offset(0, 2),
                    ),
                ),
                audio_button,
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        chat_messages.controls.append(ai_text_container)
        chat_messages.scroll_to(offset=chat_messages.height, duration=300)
        page.update()

    def clean_text(text):
        """
        Cleans AI-generated text by removing markdown, special characters, and extra spaces.
        Parameters:
        - text (str): The input text to clean.
        Returns:
        - str: The cleaned text.
        """
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)  # Remove bold (**text**)
        text = re.sub(r"\*(.*?)\*", r"\1", text)  # Remove italic (*text*)
        text = re.sub(
            r"^\s*[-•]\s*", "", text, flags=re.MULTILINE
        )  # Remove bullet points
        text = re.sub(r"\*", "", text)  # Remove stars
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
        return text

    def toggle_audio_playback(message_id):
        """Toggle audio playback between play, pause, and loading states."""
        if message_id not in active_audio_buttons:
            return
        button = active_audio_buttons[message_id]["button"]
        text = active_audio_buttons[message_id]["text"]

        if button.icon == ft.Icons.VOLUME_UP:
            button.icon = None
            button.content = ft.ProgressRing(width=16, height=16, stroke_width=2)
            page.update()
            play_audio_sync(message_id)
        elif button.icon == ft.Icons.PLAY_ARROW:
            button.icon = ft.Icons.PAUSE
            for overlay in page.overlay:
                if isinstance(overlay, Audio) and overlay.src == temp_audio_files[-1]:
                    overlay.play()
            page.update()
        elif button.icon == ft.Icons.PAUSE:
            button.icon = ft.Icons.PLAY_ARROW
            for overlay in page.overlay:
                if isinstance(overlay, Audio) and overlay.src == temp_audio_files[-1]:
                    overlay.pause()
            page.update()

    def play_audio_sync(message_id):
        """Convert text to speech and play it synchronously."""
        if message_id not in active_audio_buttons:
            return
        button = active_audio_buttons[message_id]["button"]
        text = active_audio_buttons[message_id]["text"]

        def update_icon():
            button.icon = ft.Icons.VOLUME_UP
            button.content = None
            page.update()

        if temp_dir:
            try:
                fd, temp_path = tempfile.mkstemp(suffix=".mp3", dir=temp_dir)
                os.close(fd)
                temp_audio_files.append(temp_path)
                tts = gTTS(text=clean_text(text), lang=language)
                tts.save(temp_path)
                audio_player = Audio(
                    src=temp_path,
                    autoplay=False,
                    volume=1,
                    balance=0,
                    on_loaded=lambda _: print("Loaded"),
                    on_duration_changed=lambda e: print("Duration changed:", e.data),
                    on_position_changed=lambda e: print("Position changed:", e.data),
                    on_state_changed=lambda e: print("State changed:", e.data),
                    on_seek_complete=lambda _: print("Seek complete"),
                )
                audio_player.on_end = update_icon
                page.overlay.append(audio_player)
                page.update()
                button.icon = ft.Icons.PLAY_ARROW
                button.content = None
                page.update()
            except Exception as e:
                button.icon = ft.Icons.ERROR
                button.content = None
                page.update()
                print(f"Error generating audio: {str(e)}")

    def toggle_language(e):
        """Toggle between English and Tamil."""
        nonlocal language
        language = "ta" if language == "en" else "en"
        page.session.set("language", language)
        language_toggle.label = "English" if language == "ta" else "தமிழ்"
        page.update()

    language_toggle = ft.Switch(
        label="தமிழ்" if language == "en" else "English",
        value=language == "ta",
        on_change=toggle_language,
        label_style= ft.TextStyle(color=ft.Colors.WHITE)
    )

    send_button = ft.IconButton(
        icon=ft.Icons.SEND_ROUNDED,
        on_click=send_message,
        icon_color=icon_color,
    )

    user_input = ft.TextField(
        hint_text="Type a message...",
        expand=True,
        on_submit=send_message,
        text_style=ft.TextStyle(color=input_color),
    )

    chat_ui = ft.Column(
        [
            ft.Container(
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CHAT_ROUNDED, color="#075e54", size=28),
                        ft.Text(
                            "ARV-GPT", size=24, weight=ft.FontWeight.BOLD, color=text_color
                        ),
                        language_toggle,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=ft.padding.all(50),
            ),
            chat_messages,  # This is the scrollable column
            ft.Container(ft.Row([user_input, send_button])),
        ],
        expand=True,
    )

    return chat_ui

if __name__ == "__main__":
    ft.app(target=chat_screen, assets_dir="assets")