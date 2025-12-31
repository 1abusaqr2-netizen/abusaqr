import flet as ft
import random
import os

def main(page: ft.Page):
    page.title = "Chat App - By Aseel"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.LIGHT
    
    generated_otp = None
    txt_name = ft.TextField(label="الاسم المستعار")
    txt_phone = ft.TextField(label="رقم الهاتف")
    txt_otp = ft.TextField(label="أدخل كود التحقق", visible=False)
    chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    msg_input = ft.TextField(hint_text="اكتب رسالة...", expand=True)

    def on_broadcast(data):
        is_me = data["phone"] == page.session.get("phone")
        chat_list.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Text(data["user"], size=10, color="blue", weight="bold"),
                        ft.Text(data["text"], size=16),
                    ], spacing=2),
                    bgcolor="#E1FFC7" if is_me else "#F0F0F0",
                    padding=10, border_radius=10,
                )
            ], alignment=ft.MainAxisAlignment.END if is_me else ft.MainAxisAlignment.START)
        )
        page.update()

    page.pubsub.subscribe(on_broadcast)

    def send_message(e):
        if msg_input.value:
            data = {"phone": page.session.get("phone"), "user": page.session.get("username"), "text": msg_input.value}
            page.pubsub.send_all(data)
            msg_input.value = ""
            page.update()

    def verify_logic(e):
        nonlocal generated_otp
        if not txt_otp.visible:
            generated_otp = str(random.randint(1000, 9999))
            page.snack_bar = ft.SnackBar(ft.Text(f"كود التحقق: {generated_otp}"), open=True)
            txt_phone.disabled = txt_name.disabled = txt_otp.visible = True
            btn_login.text = "تأكيد الكود"
            page.update()
        else:
            if txt_otp.value == generated_otp:
                page.session.set("phone", txt_phone.value)
                page.session.set("username", txt_name.value or "مستخدم")
                page.clean()
                page.add(ft.Column([ft.Container(content=chat_list, expand=True), ft.Row([msg_input, ft.IconButton(ft.icons.SEND, on_click=send_message)])], expand=True))
            else:
                txt_otp.error_text = "خطأ!"
                page.update()

    btn_login = ft.ElevatedButton("دخول", on_click=verify_logic, width=200, bgcolor="gold")
    page.add(ft.Column([ft.Icon(ft.icons.CHAT, size=50), txt_name, txt_phone, txt_otp, btn_login], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8502))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")
