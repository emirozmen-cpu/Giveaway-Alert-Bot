import os
import time
from datetime import datetime
import threading
import requests
import subprocess
import customtkinter as ctk
from playwright.sync_api import sync_playwright
from playwright._impl._driver import compute_driver_executable, get_driver_env

stop_event = threading.Event()


def send_discord_alert(message_text, token, channel_id, bot_name):
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }

    if "Bandit" in bot_name:
        content = f"@everyone 🌧️ **BANDITCAMP RESMİ RAİN ALERTI!** \n{message_text}"
    elif "Rusty" in bot_name:
        content = f"@everyone 🎁 **RUSTYPOT ÇEKİLİŞ ALARMI!** \n{message_text}"
    else:
        content = message_text

    payload = {"content": content}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(">>> Discord'a bildirim başarıyla iletildi!")
        else:
            print(f"❌ Discord bildirim hatası: {response.status_code}\n{response.text}")
    except Exception as e:
        print(f"❌ Discord istek hatası: {e}")


def check_and_install_browser(ui_callback=None):
    try:
        if ui_callback:
            ui_callback("⏳ Tarayıcı kontrol ediliyor... (İlk açılışta 1-2 dk sürebilir)", "orange")

        driver_executable = compute_driver_executable()
        subprocess.run([driver_executable, "install", "chromium"], env=get_driver_env(), check=False,
                       capture_output=True)

        if ui_callback:
            ui_callback("🟢 Bot aktif ve nöbette!", "green")
    except Exception:
        if ui_callback:
            ui_callback("🟢 Bot aktif ve nöbette!", "green")


def run_bandit_bot(token, channel_id, ui_callback):
    send_discord_alert("✅ Merhaba! Bot başarıyla Discord kanalınıza bağlandı ve Bandit Rain takibine başladı!", token,
                       channel_id, "Test")

    user_data_dir = os.path.join(os.getcwd(), "browser_profile")
    check_and_install_browser(ui_callback)
    print("🚀 Banditcamp tarayıcı profili başlatılıyor...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = context.pages[0] if context.pages else context.new_page()

        try:
            page.goto("https://banditcamp.com", timeout=60000)
        except Exception as e:
            print(f"⚠️ Yükleme hatası: {e}")

        print("🛡️ Bandit Bot nöbette!")
        rain_active_before = False

        while not stop_event.is_set():
            try:
                page.wait_for_timeout(3000)
                if stop_event.is_set(): break

                rain_locator = page.locator("h3:has-text('Rakeback Rain')")
                rain_detected_now = False

                if rain_locator.count() > 0:
                    for i in range(rain_locator.count()):
                        if rain_locator.nth(i).is_visible():
                            rain_detected_now = True
                            break

                if rain_detected_now and not rain_active_before:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"\n🚨 RESMİ RAİN YAKALANDI! Saat: {current_time}")
                    send_discord_alert(f"🚨 Sitede Resmi Rakeback Rain Başladı! Koşun! | Saat: {current_time}", token,
                                       channel_id, "Bandit")
                    rain_active_before = True

                elif not rain_detected_now:
                    rain_active_before = False

            except Exception as e:
                print(f"⚠️ Kontrol hatası: {e}")
                time.sleep(5)

        print("🛑 Bandit Bot durduruldu.")


def run_rustypot_bot(token, channel_id, ui_callback):
    send_discord_alert("✅ Merhaba! Bot başarıyla Discord kanalınıza bağlandı ve Rustypot takibine başladı!", token,
                       channel_id, "Test")

    user_data_dir = os.path.join(os.getcwd(), "browser_profile")
    check_and_install_browser(ui_callback)
    print("🚀 Rustypot tarayıcı profili başlatılıyor...")

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            no_viewport=True,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        page = context.new_page() if len(context.pages) == 0 else context.pages[0]

        try:
            page.goto("https://rustypot.com", timeout=60000)
        except Exception as e:
            print(f"Yükleme hatası: {e}")

        print("🛡️ Rustypot Bot nöbette!")
        giveaway_active_before = False
        last_reload_time = time.time()

        while not stop_event.is_set():
            try:
                page.wait_for_timeout(3000)
                if stop_event.is_set(): break

                if time.time() - last_reload_time > 600:
                    print("🔄 Sayfa temizliği için yenileniyor (F5)...")
                    page.reload()
                    last_reload_time = time.time()
                    page.wait_for_timeout(5000)
                    giveaway_active_before = False

                hedef_listesi = [
                    page.locator("text=/Flash Giveaway/i"),
                    page.locator("text=/Starting in/i"),
                    page.locator("button:has-text('Join')"),
                    page.locator("button:has-text('JOIN')")
                ]

                giveaway_detected_now = False
                for hedef in hedef_listesi:
                    if hedef.count() > 0:
                        for i in range(hedef.count()):
                            elem = hedef.nth(i)
                            if elem.is_visible():
                                giveaway_detected_now = True
                                break
                    if giveaway_detected_now: break

                if giveaway_detected_now and not giveaway_active_before:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(f"\n🚨 ÇEKİLİŞ YAKALANDI! Saat: {current_time}")
                    send_discord_alert(f"🚨 Çekiliş Başladı! | Saat: {current_time}", token, channel_id, "Rusty")
                    giveaway_active_before = True

                    for _ in range(30):
                        if stop_event.is_set(): break
                        time.sleep(1)

                elif not giveaway_detected_now:
                    giveaway_active_before = False

            except Exception as e:
                print(f"⚠️ Kontrol hatası: {e}")
                time.sleep(5)

        print("🛑 Rustypot Bot durduruldu.")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bildirim Botu v2.3")
        self.geometry("550x560")
        self.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.frame_main = ctk.CTkFrame(self)
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        self.label_welcome = ctk.CTkLabel(self.frame_main, text="Hoşgeldiniz!", font=("Arial", 22, "bold"))
        self.label_welcome.pack(pady=(15, 5))

        self.label_desc = ctk.CTkLabel(self.frame_main, text="Lütfen kullanmak istediğiniz botu seçin:")
        self.label_desc.pack(pady=(0, 15))

        self.btn_bandit = ctk.CTkButton(self.frame_main, text="🌧️ Bandit Rain Bot", height=45,
                                        command=lambda: self.show_config("Bandit Rain"))
        self.btn_bandit.pack(fill="x", padx=40, pady=8)

        self.btn_rusty = ctk.CTkButton(self.frame_main, text="🎁 Rustypot Free GW Bot", height=45,
                                       command=lambda: self.show_config("Rustypot"))
        self.btn_rusty.pack(fill="x", padx=40, pady=8)

        self.guide_frame = ctk.CTkFrame(self.frame_main, fg_color="#2b2b2b")
        self.guide_frame.pack(fill="x", padx=20, pady=15)

        guide_text = (
            "📌 BİLGİLENDİRME & NASIL KULLANILIR?\n"
            "1. Discord Developer Portal'dan bot oluşturup 'Token'ı kopyalayın.\n"
            "    (Token başına 'Bot ' yazmanıza GEREK YOKTUR, direkt yapıştırın)\n"
            "2. Botu sunucunuza ekleyin ve mesaj gönderme izni verin.\n"
            "3. Geliştirici Modu'nu açıp bildirim gidecek kanala sağ tıklayıp\n"
            "    'Kanal ID'sini Kopyala' deyin."
        )
        self.label_guide = ctk.CTkLabel(self.guide_frame, text=guide_text, justify="left", font=("Arial", 11),
                                        text_color="#d1d1d1")
        self.label_guide.pack(padx=10, pady=10)

        self.frame_config = ctk.CTkFrame(self)
        self.bot_title = ctk.CTkLabel(self.frame_config, text="", font=("Arial", 18, "bold"))
        self.bot_title.pack(pady=(15, 10))

        self.entry_token = ctk.CTkEntry(self.frame_config, placeholder_text="Discord Bot Token (Başında Bot yazmayın)",
                                        show="*", width=340, height=35)
        self.entry_token.pack(pady=8)

        self.entry_channel = ctk.CTkEntry(self.frame_config, placeholder_text="Discord Kanal ID", width=340, height=35)
        self.entry_channel.pack(pady=8)

        self.btn_start = ctk.CTkButton(self.frame_config, text="🚀 Botu Başlat", height=40, fg_color="#2fa572",
                                       hover_color="#248259", command=self.start_bot)
        self.btn_start.pack(pady=10)

        self.btn_stop = ctk.CTkButton(self.frame_config, text="🛑 Botu Durdur", height=40, fg_color="#d9534f",
                                      hover_color="#c9302c", command=self.stop_bot)

        self.status_label = ctk.CTkLabel(self.frame_config, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.btn_back = ctk.CTkButton(self.frame_config, text="Geri Dön", fg_color="gray", hover_color="#555555",
                                      command=self.show_main)
        self.btn_back.pack(pady=10)

        self.selected_bot = ""
        self.bot_thread = None

    def update_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def show_config(self, bot_name):
        self.selected_bot = bot_name
        self.frame_main.pack_forget()
        self.frame_config.pack(fill="both", expand=True, padx=20, pady=20)
        self.bot_title.configure(text=f"{bot_name} Yapılandırması")
        self.status_label.configure(text="")

    def show_main(self):
        if self.bot_thread and self.bot_thread.is_alive():
            stop_event.set()
        self.frame_config.pack_forget()
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

    def start_bot(self):
        token = self.entry_token.get().strip()
        channel_id = self.entry_channel.get().strip()

        if not token or not channel_id:
            self.update_status("❌ HATA: Lütfen tüm alanları doldurun!", "red")
            return

        stop_event.clear()
        self.btn_start.pack_forget()
        self.btn_stop.pack(pady=10)
        self.entry_token.configure(state="disabled")
        self.entry_channel.configure(state="disabled")

        if self.selected_bot == "Bandit Rain":
            self.bot_thread = threading.Thread(target=run_bandit_bot, args=(token, channel_id, self.update_status),
                                               daemon=True)
        elif self.selected_bot == "Rustypot":
            self.bot_thread = threading.Thread(target=run_rustypot_bot, args=(token, channel_id, self.update_status),
                                               daemon=True)

        self.bot_thread.start()

    def stop_bot(self):
        stop_event.set()
        self.update_status("🛑 Bot durduruldu.", "orange")
        self.btn_stop.pack_forget()
        self.btn_start.pack(pady=10)
        self.entry_token.configure(state="normal")
        self.entry_channel.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()