from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from datetime import datetime
import time
import os

# === CONFIGURATION ===
excel_path = "contacts.xlsx"
image_path = "C:\\pic.jpeg"
profile_path = os.path.join(os.getcwd(), "whatsapp_profile")  # לשמירת סשן
green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

# === VALIDATE FILES EXIST ===
if not os.path.exists(excel_path):
    print(f"❌ הקובץ '{excel_path}' לא נמצא.")
    exit()

if not os.path.exists(image_path):
    print(f"❌ קובץ התמונה '{image_path}' לא קיים.")
    exit()

# === LOAD WORKBOOK ===
wb = load_workbook(excel_path)
ws = wb.active

# === PROMPT: RESET STATUS? ===
reset_choice = input("🔄 האם לאפס סטטוסים קודמים (y/n)? ").strip().lower()
if reset_choice == "y":
    for i, row in enumerate(ws.iter_rows(min_row=2), start=2):
        ws.cell(row=i, column=2).value = ""
        ws.cell(row=i, column=3).value = ""
    wb.save(excel_path)

# === START SELENIUM DRIVER ===
options = Options()
options.add_argument(f"--user-data-dir={profile_path}")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--remote-debugging-port=9222")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://web.whatsapp.com")
print("📱 אם זו הפעם הראשונה – סרוק את קוד ה-QR, אחרת ממשיך אוטומטית...")
WebDriverWait(driver, 90).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='3']"))
)

# ... (ייבוא ספריות והגדרות כמו בקוד שלך - אין שינוי)

start_time = time.time()  # מדידת זמן כולל

# === LOAD CONTACTS ===
df = pd.read_excel(excel_path)
names = df["Name"].dropna().tolist()

# === MAIN LOOP ===
for i, row in enumerate(ws.iter_rows(min_row=2, values_only=False), start=2):
    name = row[0].value
    status_cell = ws.cell(row=i, column=2)
    time_cell = ws.cell(row=i, column=3)

    if status_cell.value:
        print(f"⏭️ מדלג על {name} – כבר טופל.")
        continue

    print(f"\n📨 שולח אל: {name}")
    try:
        # יציאה מצ'אט קודם
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(0.5)

        # חיפוש איש קשר
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='3']"))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(Keys.CONTROL, "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(name)
        time.sleep(1)  # זמן לטעינת תוצאות
        search_box.send_keys(Keys.ENTER)  # בחירת התוצאה הראשונה
        time.sleep(1)  # זמן למעבר לצ'אט

        # שלב 2: מציאת התוצאה הנכונה ולחיצה על ההורה שלה
        try:
            # המתנה שתופיע לפחות תוצאת חיפוש אחת
            results = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="pane-side"]/div[1]/div/div/div')
                )
            )

            contact_found = False
            for result in results:
                try:
                    # חיפוש שם איש הקשר מתוך האלמנט (לפי title)
                    name_element = result.find_element(By.XPATH, ".//span[@title]")
                    found_name = name_element.get_attribute("title").strip()
                    print(f"👀 נבדק: {found_name}")

                    if found_name == name.strip():
                        ActionChains(driver).move_to_element(result).click().perform()
                        contact_found = True
                        print(f"✅ נמצא איש קשר תואם: {found_name}")
                        break

                except Exception as inner_e:
                    print(f"⚠️ בעיה פנימית בתוצאה: {inner_e}")
                    continue

            if not contact_found:
                raise Exception("לא נמצא איש קשר תואם")

        except Exception as e:
            print(f"❌ לא נמצא איש קשר בשם: {name}")
            status_cell.value = "Contact Not Found"
            status_cell.fill = red_fill
            time_cell.value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_cell.fill = red_fill
            wb.save(excel_path)
            continue


        # לחיצה על כפתור המהדק
        attach_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button'))
        )
        attach_btn.click()

        # שדה קובץ מדיה
        image_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
        )
        image_input.send_keys(image_path)

        # שליחת תמונה
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
        )
        send_button.click()

        # עדכון סטטוס
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_cell.value = "Successful"
        status_cell.fill = green_fill
        time_cell.value = timestamp
        time_cell.fill = green_fill
        print(f"✅ נשלח בהצלחה אל: {name}")

    except Exception as e:
        msg = str(e)
        print(f"⚠️ שגיאה בשליחה אל {name}: {msg}")
        status_cell.value = msg
        status_cell.fill = red_fill
        time_cell.value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_cell.fill = red_fill

    wb.save(excel_path)

# === CLEANUP ===
driver.quit()
wb.save(excel_path)

end_time = time.time()
elapsed = round(end_time - start_time, 2)
print(f"\n🎉 כל ההודעות טופלו! זמן כולל: {elapsed} שניות.")
