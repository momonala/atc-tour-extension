from google.oauth2 import service_account

# Set up credentials
SERVICE_ACCOUNT_FILE = "google_application_credentials.json"
SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]

CALENDAR_ID = "mnalavadi@gmail.com"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

TELEGRAM_TOKEN = "7762551087:AAEhp0_GzEoY90seVxMW2s86FPFw4e2-q1c"
TELEGRAM_CHAT_ID = "5601207384"
