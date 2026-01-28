import flet as ft
from auth import login, signup
from chat_screen import chat_screen

def main(page: ft.Page):
    page.title = "ARV-GPT"
    page.theme_mode = ft.ThemeMode.SYSTEM  # Auto-detect system theme
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.BLUE)

    def show_login_ui(event=None):  # Add optional argument for event handling
        page.clean()  # Clear the current page content

        username_field = ft.TextField(label="Username", width=300, border_radius=10)
        password_field = ft.TextField(
            label="Password", password=True, width=300, border_radius=10
        )
        message_text = ft.Text(color="red")
        login_img = ft.Image(
            src="/images/welcome.png",
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )

        def handle_login(e):
            """Handles the login button click."""
            username = username_field.value.strip()
            password = password_field.value.strip()
            if username and password:
                res = login(username, password)
                if "token" in res:
                    page.session.set("user_token", res["token"])
                    page.session.set("language", "en")
                    page.go("/chat")  # Navigate to the chat screen
                else:
                    message_text.value = "Login failed"
                    page.update()
            else:
                message_text.value = "Please enter both username and password."
                page.update()

        def switch_to_signup(e):
            """Switches to the signup screen."""
            page.go("/signup")

        login_button = ft.ElevatedButton("Login", on_click=handle_login)
        signup_button = ft.TextButton("Create an account", on_click=switch_to_signup)

        login_container = ft.Container(
            content=ft.Column(
                [
                    login_img,
                    ft.Text("Login", size=24, weight="bold"),
                    username_field,
                    password_field,
                    login_button,
                    signup_button,
                    message_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )

        page.add(login_container)

    def show_signup_ui(event=None):  # Add optional argument for event handling
        page.clean()  # Clear the current page content

        signup_img = ft.Image(
            src="/images/auth.png",
            width=200,
            height=200,
            fit=ft.ImageFit.CONTAIN,
        )
        new_username = ft.TextField(label="Username", width=300, border_radius=10)
        new_email = ft.TextField(label="Email", width=300, border_radius=10)
        new_password = ft.TextField(
            label="Password", password=True, width=300, border_radius=10
        )
        signup_message = ft.Text(color="red")

        def handle_signup(e):
            """Handles the signup button click."""
            username = new_username.value.strip()
            email = new_email.value.strip()
            password = new_password.value.strip()
            if username and email and password:
                res = signup(username, email, password)
                if "message" in res:
                    signup_message.value = "Signup successful! Please log in."
                    page.update()
                    page.go("/")  # Navigate back to the login screen
                else:
                    signup_message.value = "Signup failed"
                    page.update()
            else:
                signup_message.value = "Please fill in all fields."
                page.update()

        back_to_login = ft.TextButton("Back to Login", on_click=lambda _: page.go("/"))
        signup_button = ft.ElevatedButton("Sign Up", on_click=handle_signup)

        signup_container = ft.Container(
            content=ft.Column(
                [
                    signup_img,
                    ft.Text("Sign Up", size=24, weight="bold"),
                    new_username,
                    new_email,
                    new_password,
                    signup_button,
                    back_to_login,
                    signup_message,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=20,
        )

        page.add(signup_container)

    def route_change_handler(route_event):
        """Handles route changes."""
        if page.route == "/":
            show_login_ui()  # Show the login screen
        elif page.route == "/signup":
            show_signup_ui()  # Show the signup screen
        elif page.route == "/chat":
            page.clean()
            page.add(chat_screen(page))  # Load the chat screen

    page.on_route_change = route_change_handler  # Assign the route change handler
    page.go("/")  # Start on the login screen

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")