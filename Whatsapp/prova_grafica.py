
import flet as ft

# funzione pagina grafica
def main(page: ft.Page):
    # per decorare
    chat = ft.Column()
    # per inserire testo
    new_message = ft.TextField()
    # funzione per inviare mess
    def send_click(e):
        chat.controls.append(ft.Text(new_message.value))
        new_message.value = ""
        page.update()
    
    page.add(
        chat, ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=send_click)])
    )

ft.app(main, view=ft.AppView.WEB_BROWSER)

"""
elif choose == "6":
        campi_valori = r.hgetall("Manugianni")
        chiavi = campi_valori.keys()
        print(chiavi)
"""