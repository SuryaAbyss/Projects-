import tkinter as tk
from tkinter import messagebox
from instabot import Bot
import time

# Initialize the bot
bot = Bot()

# Function to login
def login():
    username = entry_username.get()
    password = entry_password.get()
    try:
        bot.login(username=username, password=password)
        messagebox.showinfo("Login", "Login successful!")
    except Exception as e:
        messagebox.showerror("Login Failed", f"Error: {e}")

# Function to follow users
def follow_users():
    usernames = entry_usernames.get().split(",")
    for username in usernames:
        try:
            bot.follow(username.strip())
            messagebox.showinfo("Follow", f"Followed {username.strip()}")
        except Exception as e:
            messagebox.showerror("Follow Failed", f"Failed to follow {username.strip()}: {e}")

# Function to send messages
def send_messages():
    usernames = entry_message_usernames.get().split(",")
    message = entry_message.get()
    for username in usernames:
        try:
            bot.send_message(message, [username.strip()])
            messagebox.showinfo("Send Message", f"Message sent to {username.strip()}")
        except Exception as e:
            messagebox.showerror("Send Message Failed", f"Failed to send message to {username.strip()}: {e}")

# Function to schedule posts
def schedule_post():
    image_path = entry_image.get()
    caption = entry_caption.get()
    try:
        delay = int(entry_delay.get())
        time.sleep(delay)
        bot.upload_photo(image_path, caption=caption)
        messagebox.showinfo("Scheduled Post", "Post uploaded successfully!")
    except Exception as e:
        messagebox.showerror("Scheduled Post Failed", f"Failed to upload post: {e}")

# Function to unfollow users
def unfollow_users():
    usernames = entry_usernames.get().split(",")
    for username in usernames:
        try:
            bot.unfollow(username.strip())
            messagebox.showinfo("Unfollow", f"Unfollowed {username.strip()}")
        except Exception as e:
            messagebox.showerror("Unfollow Failed", f"Failed to unfollow {username.strip()}: {e}")

# Creating the main window
window = tk.Tk()
window.title("Instagram Bot")
window.geometry("500x600")
window.config(bg="#f3f3f3")

# Create a colorful header
header_label = tk.Label(window, text="Instagram Bot", font=("Arial", 24, "bold"), fg="#ffffff", bg="#ff6f61", pady=10)
header_label.pack(fill="both")

# Function to create a frame with a color
def create_colored_frame(parent, bg_color, padx=10, pady=10):
    frame = tk.Frame(parent, bg=bg_color, padx=padx, pady=pady)
    frame.pack(fill="both", pady=5)
    return frame

# Create Login Section
login_frame = create_colored_frame(window, "#ffb6c1")
label_username = tk.Label(login_frame, text="Username", font=("Arial", 12), bg="#ffb6c1")
label_username.grid(row=0, column=0, sticky="w", padx=10)
entry_username = tk.Entry(login_frame, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10)

label_password = tk.Label(login_frame, text="Password", font=("Arial", 12), bg="#ffb6c1")
label_password.grid(row=1, column=0, sticky="w", padx=10)
entry_password = tk.Entry(login_frame, show="*", font=("Arial", 12))
entry_password.grid(row=1, column=1, padx=10)

button_login = tk.Button(login_frame, text="Login", command=login, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15)
button_login.grid(row=2, columnspan=2, pady=10)

# Create Follow Section
follow_frame = create_colored_frame(window, "#f0e68c")
label_usernames = tk.Label(follow_frame, text="Usernames to follow (comma-separated)", font=("Arial", 12), bg="#f0e68c")
label_usernames.grid(row=0, column=0, sticky="w", padx=10)
entry_usernames = tk.Entry(follow_frame, font=("Arial", 12))
entry_usernames.grid(row=0, column=1, padx=10)

button_follow = tk.Button(follow_frame, text="Follow Users", command=follow_users, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15)
button_follow.grid(row=1, columnspan=2, pady=10)

# Create Send Message Section
message_frame = create_colored_frame(window, "#add8e6")
label_message_usernames = tk.Label(message_frame, text="Usernames to send message to", font=("Arial", 12), bg="#add8e6")
label_message_usernames.grid(row=0, column=0, sticky="w", padx=10)
entry_message_usernames = tk.Entry(message_frame, font=("Arial", 12))
entry_message_usernames.grid(row=0, column=1, padx=10)

label_message = tk.Label(message_frame, text="Message", font=("Arial", 12), bg="#add8e6")
label_message.grid(row=1, column=0, sticky="w", padx=10)
entry_message = tk.Entry(message_frame, font=("Arial", 12))
entry_message.grid(row=1, column=1, padx=10)

button_send_message = tk.Button(message_frame, text="Send Message", command=send_messages, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15)
button_send_message.grid(row=2, columnspan=2, pady=10)

# Create Schedule Post Section
schedule_frame = create_colored_frame(window, "#90ee90")
label_image = tk.Label(schedule_frame, text="Image path", font=("Arial", 12), bg="#90ee90")
label_image.grid(row=0, column=0, sticky="w", padx=10)
entry_image = tk.Entry(schedule_frame, font=("Arial", 12))
entry_image.grid(row=0, column=1, padx=10)

label_caption = tk.Label(schedule_frame, text="Caption", font=("Arial", 12), bg="#90ee90")
label_caption.grid(row=1, column=0, sticky="w", padx=10)
entry_caption = tk.Entry(schedule_frame, font=("Arial", 12))
entry_caption.grid(row=1, column=1, padx=10)

label_delay = tk.Label(schedule_frame, text="Delay (seconds)", font=("Arial", 12), bg="#90ee90")
label_delay.grid(row=2, column=0, sticky="w", padx=10)
entry_delay = tk.Entry(schedule_frame, font=("Arial", 12))
entry_delay.grid(row=2, column=1, padx=10)

button_schedule = tk.Button(schedule_frame, text="Schedule Post", command=schedule_post, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15)
button_schedule.grid(row=3, columnspan=2, pady=10)

# Create Unfollow Section
unfollow_frame = create_colored_frame(window, "#f08080")
label_unfollow_usernames = tk.Label(unfollow_frame, text="Usernames to unfollow (comma-separated)", font=("Arial", 12), bg="#f08080")
label_unfollow_usernames.grid(row=0, column=0, sticky="w", padx=10)
entry_unfollow_usernames = tk.Entry(unfollow_frame, font=("Arial", 12))
entry_unfollow_usernames.grid(row=0, column=1, padx=10)

button_unfollow = tk.Button(unfollow_frame, text="Unfollow Users", command=unfollow_users, font=("Arial", 12, "bold"), bg="#4caf50", fg="white", width=15)
button_unfollow.grid(row=1, columnspan=2, pady=10)

# Run the application
window.mainloop()
