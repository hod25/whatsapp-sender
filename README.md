# WhatsApp Bot - Automated WhatsApp Message Sender

🤖 An automated bot for sending images via WhatsApp to a contact list from an Excel file

---

## Project Description

This bot enables automatic sending of images to a contact list from an Excel file using Selenium and WhatsApp Web. It includes delivery status tracking and cell coloring based on success or failure.

---

## Features

- ✅ Automatic image sending to contact list
- 📊 Reading from Excel file with contact list
- 🎯 Precise contact identification
- 📈 Delivery status tracking (success/failure)
- 🎨 Cell coloring based on results (green/red)
- ⏰ Timestamp logging
- 🔄 Option to reset previous statuses
- 📱 Persistent profile usage to avoid repeated QR scanning

---

## System Requirements

- Python 3.7+
- Google Chrome Browser
- Excel file with contact list
- Image file for sending

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp-sender.git
cd whatsapp-sender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Prepare required files:
   - Excel file with "Name" column containing contact names
   - Image file for sending (update path in code)

---

## Usage

1. Update paths in `sle.py` file:
   ```python
   excel_path = "contacts - Copy.xlsx"  # Path to Excel file
   image_path = "C:\\pic.jpeg"          # Path to image
   ```

2. Run the bot:
   ```bash
   python sle.py
   ```

3. On first run, scan the QR code in WhatsApp

4. The bot will automatically process all contacts in the list

---

## Excel File Structure

| Name | Status | Timestamp |
|------|--------|-----------|
| John Doe | | |
| Jane Smith | | |

- **Name**: Contact name (required)
- **Status**: Delivery status (automatically updated)
- **Timestamp**: Send time (automatically updated)

---

## Project Files

- `sle.py` - Main bot file
- `requirements.txt` - Python dependencies list
- `contacts - Copy.xlsx` - Sample contacts file
- `chromedriver.exe` - Chrome driver
- `whatsapp_profile/` - Profile directory for session persistence

---

## Troubleshooting

### Common Issues:
1. **"Contact Not Found"** - Ensure the name in Excel exactly matches the name in WhatsApp
2. **ChromeDriver issues** - Ensure Chrome version matches driver version
3. **Image not sending** - Check that image path is correct and file exists

### Tips:
- Use full names as they appear in WhatsApp
- Ensure stable internet connection
- Don't close the browser window during operation

---

## Security

⚠️ **Important Security Note**: This bot uses WhatsApp Web and not the official API. Use at your own risk.

- Don't share your account details
- Use a separate profile for the bot if possible
- Be careful of temporary blocks from WhatsApp during intensive use

---

## License

MIT License - See LICENSE file for more details

---

## Contributing

1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Contact

If you have questions or suggestions for improvement, please open an issue in the project.

---

**Note**: This project was created for educational purposes. Use it at your own responsibility and in accordance with WhatsApp's terms of service.