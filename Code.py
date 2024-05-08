import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox


def install_requests():
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "requests"])
    except subprocess.CalledProcessError:
        print("Failed to install requests. Please install it manually.")
        sys.exit(1)


def send_message(webhook_url, message, times):
    import requests

    for i in range(times):
        payload = {'content': message}
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(f"Message {i+1} sent successfully.")
        else:
            print(
                f"Failed to send message {i+1}. Status code:", response.status_code)


def delete_webhook(webhook_url):
    import requests

    response = requests.delete(webhook_url)

    if response.status_code == 204:
        print("Webhook deletion requested. Waiting for 5 seconds before deletion...")
        time.sleep(5)  # 5 seconds delay
        response = requests.delete(webhook_url)  # Actually delete the webhook

        if response.status_code == 204:
            print("Webhook deleted successfully!")
        else:
            print(
                "Failed to delete the webhook after delay. Check the URL and try again.")
            retry = input("Do you want to try again? (yes/no): ")
            if retry.lower() == 'yes':
                delete_webhook(webhook_url)
            else:
                print("Webhook deletion canceled.")
    else:
        print("Failed to delete the webhook. Check the URL and try again.")
        retry = input("Do you want to try again? (yes/no): ")
        if retry.lower() == 'yes':
            delete_webhook(webhook_url)
        else:
            print("Webhook deletion canceled.")


def execute_script(script_number, webhook_url=None, message=None, times=None):
    if script_number == 1:
        if not webhook_url:
            webhook_url = input("Enter the webhook URL: ")
        if not message:
            message = input("Enter the message you want to send: ")
        if not times:
            times = int(
                input("Enter the number of times you want to send the message: "))

        send_message(webhook_url, message, times)
    elif script_number == 2:
        if not webhook_url:
            webhook_url = input("Enter the webhook URL to delete: ")
        delete_webhook(webhook_url)
    else:
        print("Invalid option.")


def main():
    def send_to_webhook():
        webhook_url = webhook_url_entry.get()
        message = message_entry.get()
        times = int(times_entry.get())
        execute_script(1, webhook_url, message, times)
        messagebox.showinfo("Message Sent", "Message sent successfully.")

    def delete_webhook():
        webhook_url = webhook_url_entry.get()
        execute_script(2, webhook_url)
        messagebox.showinfo("Webhook Deleted", "Webhook deleted successfully.")

    root = tk.Tk()
    root.title("SNAKES WEBHOOK DISTROYER")

    webhook_url_label = tk.Label(root, text="Webhook URL:")
    webhook_url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    webhook_url_entry = tk.Entry(root)
    webhook_url_entry.grid(row=0, column=1, padx=5, pady=5)

    message_label = tk.Label(root, text="Message:")
    message_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    message_entry = tk.Entry(root)
    message_entry.grid(row=1, column=1, padx=5, pady=5)

    times_label = tk.Label(root, text="Times:")
    times_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    times_entry = tk.Entry(root)
    times_entry.grid(row=2, column=1, padx=5, pady=5)

    send_button = tk.Button(
        root, text="Send Message to Webhook", command=send_to_webhook)
    send_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    delete_button = tk.Button(
        root, text="Delete Webhook", command=delete_webhook)
    delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
