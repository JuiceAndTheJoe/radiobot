import smtplib, schedule, time, pygame
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def send_mail():
        
        # Email configuration
        smtp_server = 'smtp.gmail.com'  # SMTP server address
        smtp_port = 587  # SMTP server port
        sender_email = 'example@gmail.com'  # Sender email address
        receiver_email = 'example@gmail.com'  # Recipient email address
        password = ""  # Your email account password
        
        # Email content
        subject = 'Elton John is playing!'
        body = 'Elton John is currently playing on the radio!'
        
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        # Send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)

def play_sound_cue():
    # Initialize the pygame library
    pygame.init()

    # Load the sound file
    sound_file = "crocc.wav"  # Replace with the actual path to your sound file
    pygame.mixer.music.load(sound_file)

    # Play the sound
    pygame.mixer.music.play()

    # Wait until the sound finishes playing
    while pygame.mixer.music.get_busy():
        continue

    # Quit pygame
    pygame.quit()

def check_elton():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode, no GUI needed

    # Provide the path to your Chrome driver executable
    driver_path = "C:/Users/chromedriver.exe"

    # Set the path to the Chrome driver
    webdriver.chrome.driver = driver_path

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    # URL of the radio station's website
    url = "https://www.ilikeradio.se/lugnafavoriter"

    # Navigate to the website
    driver.get(url)
    driver.refresh()

    # Find the element containing the currently playing artist
    artist_element = driver.find_element(By.CSS_SELECTOR, ".player-audio-content-desc")

    # Get the text of the currently playing artist
    artist_name = artist_element.text.strip()

    # Check if Elton John is currently playing
    if "Elton John" in artist_name:
        send_mail()
        play_sound_cue()
    else:
        print(f"\n\n{time.ctime()}: Elton John is not playing :(")

    # Quit the browser
    driver.quit()

# Schedule the task to run every 2 minutes
schedule.every(2).minutes.do(check_elton)

while True:
    schedule.run_pending()
    time.sleep(1)
