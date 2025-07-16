import os
import requests
import random
import time

# ==== PROXY FUNCTION ====
def get_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=3000&country=all"
    try:
        r = requests.get(url)
        proxies = [p.strip() for p in r.text.splitlines() if p.strip()]
        with open("proxies.txt", "w") as f:
            for p in proxies:
                f.write(p + "\n")
        print(f"\n✓ Lấy {len(proxies)} proxy thành công!")
    except Exception as e:
        print(f"✗ Không lấy được proxy: {e}")

def load_tokens():
    try:
        with open("tokens.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_tokens(tokens):
    with open("tokens.txt", "w") as f:
        for token in tokens:
            f.write(token + "\n")

import random
import time

def fake_sms_spam():
    phone = input("📱 số điện thoại muốn spam : ").strip()
    if not phone.isdigit() or len(phone) < 9:
        print("❌ Số điện thoại không hợp lệ!")
        return

    print(f"\n🚀 Bắt đầu spam ảo SMS tới số {phone}...\n")
    
    messages = [
        "Mã OTP của bạn là: " + str(random.randint(100000, 999999)),
        "Xác nhận đăng nhập thành công.",
        "Cảnh báo: Có người đăng nhập từ thiết bị lạ.",
        "Bạn vừa yêu cầu đổi mật khẩu, nếu không phải bạn, hãy báo ngay.",
        "Mã xác thực là: " + str(random.randint(100000, 999999)),
        "Đăng nhập thành công lúc " + time.strftime("%H:%M:%S"),
        "Phát hiện truy cập lạ vào tài khoản bạn."
    ]

    for i in range(1, 100):  # 30 tin nhắn ảo
        msg = random.choice(messages)
        fake_ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        print(f"[{i:02}] 📩 {msg} (IP: {fake_ip})")
        time.sleep(0.15)

    print("\n✅ Hoàn tất spam thằng kia đã cay =))\n")

# Gọi hàm

def spam_message():
    tokens = load_tokens()
    message = input("✉️ Nội dung tin nhắn muốn spam: ").strip()
    if not message:
        print("❌ Tin nhắn không được để trống!")
        return
    
    delay = 0.5  # Giãn cách mỗi request để tránh rate limit
    count = 0

    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        # Lấy danh sách bạn bè
        try:
            res = requests.get("https://discord.com/api/v10/users/@me/relationships", headers=headers)
            if res.status_code != 200:
                print(f"✗ Không lấy được danh sách bạn bè ({token[:25]})")
                continue
            friends = res.json()
        except Exception as e:
            print(f"✗ Lỗi khi lấy bạn bè ({token[:25]}): {e}")
            continue

        # Gửi tin nhắn đến từng người
        for friend in friends:
            if friend.get("type") == 1:  # type=1 là bạn bè
                user_id = friend["id"]

                # Tạo DM channel
                dm = requests.post("https://discord.com/api/v10/users/@me/channels",
                                   headers=headers,
                                   json={"recipient_id": user_id})
                if dm.status_code == 200:
                    channel_id = dm.json()["id"]

                    # Gửi tin nhắn
                    send = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages",
                                         headers=headers,
                                         json={"content": message})
                    if send.status_code == 200:
                        count += 1
                        print(f"✓ Đã gửi tin nhắn đến {user_id} ({count})")
                    else:
                        print(f"✗ Lỗi gửi đến {user_id}: {send.status_code}")
                else:
                    print(f"✗ Lỗi tạo DM với {user_id}: {dm.status_code}")

                time.sleep(delay)  # tránh bị block

def spam_call():
    tokens = load_tokens()
    delay = 1.5  # Thời gian nghỉ giữa mỗi cuộc gọi

    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        # Lấy danh sách bạn bè
        try:
            res = requests.get("https://discord.com/api/v10/users/@me/relationships", headers=headers)
            if res.status_code != 200:
                print(f"✗ Không lấy được bạn bè ({token[:25]}...)")
                continue
            friends = res.json()
        except Exception as e:
            print(f"✗ Lỗi khi lấy danh sách bạn bè: {e}")
            continue

        for friend in friends:
            if friend.get("type") == 1:  # type=1 là bạn bè
                user_id = friend["id"]

                # Tạo DM channel
                dm = requests.post("https://discord.com/api/v10/users/@me/channels",
                                   headers=headers,
                                   json={"recipient_id": user_id})
                if dm.status_code != 200:
                    print(f"✗ Không tạo được DM với {user_id}")
                    continue

                channel_id = dm.json()["id"]

                # Gửi call
                call = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/call/ring",
                                     headers=headers,
                                     json={"recipients": [user_id]})
                if call.status_code == 204:
                    print(f"📞 Đã spam call đến {user_id}")
                else:
                    print(f"✗ Lỗi call {user_id}: {call.status_code}")

                time.sleep(delay)



def input_tokens():
    tokens = load_tokens()
    print("\nNhập token mới (gõ 'done' để kết thúc):")
    i = len(tokens) + 1
    while True:
        new_token = input(f"[{i}] Token: ").strip().strip('"')
        if new_token.lower() == 'done':
            break
        if new_token:
            tokens.append(new_token)
            i += 1
    save_tokens(tokens)
    print(f"\n✓ Đã lưu {len(tokens)} token!")

def check_tokens():
    tokens = load_tokens()
    if not tokens:
        print("Không có token nào để kiểm tra.")
        return
    print("\nBắt đầu kiểm tra token...")
    for token in tokens:
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        try:
            response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)
            if response.status_code == 200:
                user = response.json()
                print(f"✓ LIVE: {user.get('username')}#{user.get('discriminator')} ({token[:25]}...)")
            else:
                print(f"✗ DEAD: {token[:25]}...")
        except Exception as e:
            print(f"✗ ERROR: {token[:25]}... {e}")

def join_server():
    tokens = load_tokens()
    invite = input("Nhập invite code (không https://discord.gg/): ").strip()
    if not invite:
        print("Invite không hợp lệ!")
        return
    for token in tokens:
        headers = {"Authorization": token}
        url = f"https://discord.com/api/v10/invites/{invite}"
        res = requests.post(url, headers=headers)
        if res.status_code == 200:
            print(f"✓ JOINED: {token[:25]}...")
        else:
            print(f"✗ FAIL: {token[:25]} ({res.status_code})")

def leave_server():
    tokens = load_tokens()
    guild_id = input("Nhập guild ID để out: ").strip()
    for token in tokens:
        headers = {"Authorization": token}
        url = f"https://discord.com/api/v10/users/@me/guilds/{guild_id}"
        res = requests.delete(url, headers=headers)
        if res.status_code == 204:
            print(f"✓ OUT: {token[:25]}...")
        else:
            print(f"✗ FAIL: {token[:25]} ({res.status_code})")

def spam_all_channels():
    tokens = load_tokens()
    guild_id = input("Nhập guild ID: ").strip()
    message = input("Nội dung spam: ").strip()
    for token in tokens:
        headers = {"Authorization": token}
        r = requests.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers)
        if r.status_code == 200:
            channels = r.json()
            for ch in channels:
                if ch.get("type") == 0:
                    res = requests.post(f"https://discord.com/api/v10/channels/{ch['id']}/messages",
                                        headers=headers,
                                        json={"content": message})
                    if res.status_code == 200:
                        print(f"✓ SPAM: {ch['name']} ({token[:25]})")
                    else:
                        print(f"✗ FAIL SPAM: {ch['name']} ({res.status_code})")
        else:
            print(f"Không thể lấy kênh từ {token[:25]} ({r.status_code})")

def spam_link():
    print("🚧 Tính năng đang phát triển...")

def spam_invite():
    print("🚧 Tính năng đang phát triển...")

from time import sleep

def print_banner():
    gradient = [
        '\033[38;2;180;0;255m',  # tím
        '\033[38;2;210;0;230m',
        '\033[38;2;240;0;200m',
        '\033[38;2;255;0;170m',
        '\033[38;2;255;0;130m',  # hồng đậm
        '\033[38;2;255;50;180m',
        '\033[38;2;255;100;220m',
        ]
    banner_lines = [
        """ _     _           _             ____             
| |   (_)_ __ ___ | |__   ___   |  _ \  _____   __
| |   | | '_ ` _ \| '_ \ / _ \  | | | |/ _ \ \ / /
| |___| | | | | | | |_) | (_) | | |_| |  __/\ V / 
|_____|_|_| |_| |_|_.__/ \___/  |____/ \___| \_/  """,
        "         LIMBO X - nguyen tuan phi"
    ]

    for i, line in enumerate(banner_lines):
        color = gradient[i % len(gradient)]
        print(color + line + '\033[0m')
        sleep(0.02)  # Cho mượt mượt thêm tí cảm giác khởi động ngầu

def print_menu():
    options = [
         "01» Checker",
        "02» Join Server",
        "03» Leave Server",
        "04» Spam Channels",
        "05» Spam Message",
        "06» Spam Call",
        "07» Spam Link",
        "08» Spam Invite Sever",
        "09» Nhập Token",
        "10» Get Proxy",
        "11» Buff Follow TikTok",
        "12» Buff Like TikTok",
        "13» Buff View TikTok",
        "14» Spam SMS",
        "15» Exit Menu"
    ]
    print(f"\nLoaded <{len(load_tokens())}> tokens")
    print("┌──────────────────────────────┐")
    for opt in options:
        print(f"│ {opt.ljust(28)}│")
    print("└──────────────────────────────┘")

def fake_loading(task_name="Đang xử lý", count=50, delay=0.2):
    print(f"\n[•] {task_name}...\n")
    for i in range(1, count + 1):
        fake_ip = f"{random.randint(10,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        print(f"   [{i:02}/50] → Sent from IP: {fake_ip}")
        time.sleep(delay)
    print("\n[✓] Hoàn tất!\n")

def fake_buff_view():
    url = input("\n🔗 Nhập link video TikTok cần buff view: ").strip()
    if not url:
        print("❌ URL không hợp lệ!\n")
        return
    fake_loading(f"Buff view cho {url}")
    print(f"🔥 Đã buff {random.randint(1000, 5000)} view cho video thành công!\n")
    input("⏎ Nhấn Enter để quay lại menu...")

def fake_buff_like():
    url = input("\n🔗 Nhập link video TikTok cần buff tym: ").strip()
    if not url:
        print("❌ URL không hợp lệ!\n")
        return
    fake_loading(f"Buff tym cho {url}")
    print(f"💖 Đã buff {random.randint(500, 1500)} tym cho video thành công!\n")
    input("⏎ Nhấn Enter để quay lại menu...")

def fake_buff_follow():
    user = input("\n👤 Nhập @username TikTok cần buff follow: ").strip().lstrip("@")
    if not user:
        print("❌ Username không hợp lệ!\n")
        return
    fake_loading(f"Buff follow cho @{user}")
    print(f"📈 Đã buff {random.randint(300, 1000)} follow cho @{user} thành công!\n")
    input("⏎ Nhấn Enter để quay lại menu...")
    

def main():
    os.system("clear" if os.name == "posix" else "cls")
    print_banner()
    print_menu()

    while True:
        try:
            choice = input("\n-> Chọn chức năng (01-15): ").strip()
            print(f"[!] Đang chạy chức năng {choice}...\n")

            if choice == "01":
                check_tokens()             # 01» Checker
            elif choice == "02":
                join_server()             # 02» Join Server
            elif choice == "03":
                leave_server()            # 03» Leave Server
            elif choice == "04":
                spam_all_channels()       # 04» Spam Channels
            elif choice == "05":
                spam_message()            # 05» Spam Message
            elif choice == "06":
                spam_call()               # 06» Spam Call
            elif choice == "07":
                spam_link()               # 07» Spam Link
            elif choice == "08":
                spam_invite()             # 08» Spam Invite Sever
            elif choice == "09":
                input_tokens()            # 09» Nhập Token
            elif choice == "10":
                get_proxies()             # 10» Get Proxy
            elif choice == "11":
                fake_buff_follow()        # 11» Buff Follow TikTok
            elif choice == "12":
                fake_buff_like()          # 12» Buff Like TikTok
            elif choice == "13":
                fake_buff_view()          # 13» Buff View TikTok
            elif choice == "14":
                fake_sms_spam()                # 14» Spam SMS
            elif choice == "15":
                print("\n👋 Tạm biệt! Hẹn gặp lại Phi lần sau...")
                break                     # 15» Exit Menu
            else:
                print("[!] Lựa chọn không hợp lệ!")
        except KeyboardInterrupt:
            print("\n❌ Đã thoát tool")
            break

if __name__ == "__main__":
    main()
