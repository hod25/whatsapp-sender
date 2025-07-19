import os
import shutil
from webdriver_manager.chrome import ChromeDriverManager

# הגדרת הנתיב של תיקיית הסקריפט שלך
my_script_driver_folder = "/path/to/your/whatsapp_script_folder"

# הורדת הדרייבר העדכני ביותר
driver_path = ChromeDriverManager().install()

# העתקת הדרייבר לתיקיית הסקריפט
destination_path = os.path.join(my_script_driver_folder, "chromedriver")
shutil.copy(driver_path, destination_path)

print(f"Updated chromedriver copied to: {destination_path}")
