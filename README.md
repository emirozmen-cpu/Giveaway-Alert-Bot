# 🎁 Giveaway Alert Bot - Web Automation & Discord Integration

*[Türkçe açıklamalar aşağıdadır / Turkish documentation is below]*

A decentralized, multi-threaded desktop application built with Python that automates headless browser sessions to monitor web platforms and dispatches real-time alerts via the Discord API.

## 🚀 Core Architecture & Features
* **Client-Side Security:** Users input their own Discord bot tokens locally; no central server collects or stores sensitive user credentials.
* **Asynchronous Execution:** Implements Python `threading` to run intensive browser automation loops in the background without blocking the main GUI thread.
* **Dynamic DOM Parsing:** Utilizes Playwright to monitor real-time DOM changes and intercept specific target elements (e.g., Flash Giveaways, Rakeback Rains).
* **Automated Dependency Management:** Features a built-in routine to verify and seamlessly install required headless Chromium binaries directly on the client's machine during the initial launch.
* **Modern GUI:** Designed with CustomTkinter for a sleek, responsive, and native desktop experience.

## 🛠️ Tech Stack
* **Core:** Python 3, Threading
* **Web Automation:** Playwright (Headless Chromium)
* **GUI:** CustomTkinter
* **Network & API:** Requests (Discord v10 API)
* **Build & Packaging:** PyInstaller

## 📥 Installation & Usage
1. Download the latest `Giveaway Alert Bot.exe` from the **Releases** tab.
2. Run the application directly (no local Python environment required).
3. Enter your Discord Channel ID and Bot Token.
4. Select your target module and initialize the monitoring engine.

---

# 🎁 Bildirim Botu - Web Otomasyonu ve Discord Entegrasyonu

Python ile geliştirilmiş; web platformlarını izlemek için arka planda (headless) tarayıcı oturumlarını otomatize eden ve Discord API üzerinden gerçek zamanlı bildirimler gönderen, çok kanallı (multi-threaded) ve dağıtık bir masaüstü uygulamasıdır.

## 🚀 Temel Mimari ve Özellikler
* **İstemci Taraflı Güvenlik:** Kullanıcılar kendi Discord bot token'larını yerel olarak girerler; hiçbir merkezi sunucu hassas kullanıcı verilerini toplamaz veya saklamaz.
* **Asenkron Çalışma:** Arayüzün (GUI) donmasını engellemek için, yoğun tarayıcı otomasyon döngülerini arka planda çalıştırmak üzere Python `threading` modülü kullanılmıştır.
* **Dinamik DOM Analizi:** Gerçek zamanlı DOM değişikliklerini izlemek ve belirli hedef elementleri (örn. Flash Giveaway, Rakeback Rain) yakalamak için Playwright kullanılmıştır.
* **Otomatik Bağımlılık Yönetimi:** Uygulama ilk açıldığında, kullanıcının bilgisayarında gereken Chromium altyapısının olup olmadığını kontrol eden ve yoksa otomatik kuran yerleşik bir sisteme sahiptir.
* **Modern Arayüz (GUI):** Şık, duyarlı ve yerel masaüstü deneyimi sunmak için CustomTkinter ile tasarlanmıştır.

## 🛠️ Kullanılan Teknolojiler
* **Çekirdek:** Python 3, Threading
* **Web Otomasyonu:** Playwright (Headless Chromium)
* **Arayüz:** CustomTkinter
* **Ağ ve API:** Requests (Discord v10 API)
* **Derleme:** PyInstaller

## 📥 Kurulum ve Kullanım
1. **Releases** sekmesinden en güncel `Giveaway Alert Bot.exe` dosyasını indirin.
2. Uygulamayı doğrudan çalıştırın (Bilgisayarınızda Python kurulu olmasına gerek yoktur).
3. Discord Kanal ID'nizi ve Bot Token'ınızı girin.
4. Hedef bot modülünü seçip sistemi başlatın.
