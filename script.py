import pyautogui
import pandas as pd
import pyperclip
import time
import webbrowser

# === CONFIGURATION ===
image_path = "C:\\pic.jpeg"
csv_path = "contacts.csv"

# === OPEN WHATSAPP WEB ===
webbrowser.open("https://web.whatsapp.com")
print("🌐 Opening WhatsApp Web...")
time.sleep(10)  # זמן לסריקת קוד QR

# === LOAD CONTACT NAMES ===
df = pd.read_csv(csv_path)
names = df["Name"].dropna().tolist()

# === HELPER FUNCTIONS ===
def wait_and_click(image, timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            pos = pyautogui.locateCenterOnScreen(image, confidence=0.8)
        except Exception as e:
            print(f"❌ Error locating {image}: {e}")
            return False
        if pos:
            pyautogui.moveTo(pos)
            pyautogui.click()
            return True
        time.sleep(1)
    print(f"❌ Could not find '{image}'")
    return False

def contact_not_found():
    try:
        return pyautogui.locateOnScreen("nofound.png", confidence=0.8) is not None
    except:
        return False

def clear_search():
    if wait_and_click("searchbar.png"):
        time.sleep(1)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("delete")
    time.sleep(1)

# === MAIN LOOP ===
for name in names:
    print(f"\n🔍 Processing: {name}")

    # Step 1: Clear search bar
    clear_search()

    # Step 2: Search for contact
    pyperclip.copy(name)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1.5)
    pyautogui.press("enter")
    time.sleep(0.5)

    # Step 3: Check if not found
    if contact_not_found():
        print(f"⚠️ Contact '{name}' not found. Skipping.")
        clear_search()  # נקה שוב את השם הלא נכון
        continue

    # Step 4: Click clip icon
    if not wait_and_click("clip.png"):
        continue
    time.sleep(2.5)

    # Step 5: Click photo icon
    if not wait_and_click("photo.png"):
        continue
    time.sleep(2.5)

    # Step 6: Paste image path and press Enter
    # pyperclip.copy(image_path)
    # pyautogui.hotkey("ctrl", "v")
    # pyautogui.press("enter")
    # time.sleep(2)
    
    # Step 6: Paste image path and press Enter
    pyautogui.write(image_path, interval=0.1)
    pyautogui.press("enter")
    time.sleep(2)

    # Step 7: Click send
    if not wait_and_click("send.png"):
        continue
    time.sleep(2)

    print(f"✅ Message sent to: {name}")
    time.sleep(2)

print("\n🎉 All messages sent successfully!")
