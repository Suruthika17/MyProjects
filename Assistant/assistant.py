import pyttsx3
import pyautogui
import webbrowser
import os
import time
import tkinter as tk
import speech_recognition as sr  # voice input

# ------------ SETUP ------------
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# ------------ VOICE LISTENING ------------
def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)
    try:
        command = r.recognize_google(audio, language="en-IN")
        command = command.lower()
        speak(f"You said: {command}")
        return command
    except Exception:
        speak("Sorry, I didn't understand.")
        return ""

# ------------ COMMAND HANDLER ------------
def handle_command(command: str) -> bool:
    command = command.lower().strip()

    if command == "":
        speak("Please type a command.")
        return True

    # -------- SYSTEM APPS --------
    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open paint" in command or "open mspaint" in command:
        speak("Opening Paint")
        os.system("mspaint.exe")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    elif "open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "open powershell" in command:
        speak("Opening PowerShell")
        os.system("start powershell")

    elif "open settings" in command:
        speak("Opening Settings")
        os.system("start ms-settings:")

    # -------- BROWSERS & EDITORS --------
    elif "open chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open edge" in command or "open microsoft edge" in command:
        speak("Opening Microsoft Edge")
        os.system("start msedge")

    elif "open vscode" in command or "open vs code" in command:
        speak("Opening VS Code")
        os.system("code")

    # -------- OFFICE (IF INSTALLED) --------
    elif "open word" in command:
        speak("Opening Word")
        os.system("start winword")

    elif "open excel" in command:
        speak("Opening Excel")
        os.system("start excel")

    elif "open powerpoint" in command:
        speak("Opening PowerPoint")
        os.system("start powerpnt")

    # -------- BASIC FOLDERS --------
    elif "open downloads" in command:
        speak("Opening Downloads folder")
        os.startfile(r"C:\Users\SURUTHIKA\Downloads")

    elif "open documents" in command or "open my documents" in command:
        speak("Opening Documents folder")
        os.startfile(r"C:\Users\SURUTHIKA\Documents")

    elif "open desktop" in command:
        speak("Opening Desktop")
        os.startfile(r"C:\Users\SURUTHIKA\Desktop")

    elif "open pictures" in command or "open photos" in command:
        speak("Opening Pictures folder")
        os.startfile(r"C:\Users\SURUTHIKA\Pictures")

    elif "open projects" in command:
        speak("Opening Projects folder")
        os.startfile(r"D:\Projects")

    # -------- BROWSER SHORTCUTS --------
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open github" in command:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    # -------- TYPING DEMO --------
    elif "type hello" in command:
        speak("Typing hello")
        pyautogui.write("Hello!", interval=0.05)

    # -------- EXIT --------
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye")
        return False

    else:
        speak("Command not recognized.")
    return True

# ------------ TKINTER SUPER STYLE WINDOW ------------
def run_gui():
    root = tk.Tk()
    root.title("Automation Assistant")

    # window size and center it
    width, height = 560, 260
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = int((screen_w - width) / 2)
    y = int((screen_h - height) / 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)

    # background color (VS Code-like theme)
    root.configure(bg="#0f172a")  # dark navy

    # outer frame (card)
    card = tk.Frame(root, bg="#111827", bd=0, highlightthickness=1, highlightbackground="#1f2937")
    card.pack(expand=True, fill="both", padx=20, pady=20)

    # title label
    title_label = tk.Label(
        card,
        text="Automation Assistant",
        font=("Segoe UI", 18, "bold"),
        bg="#111827",
        fg="#e5e7eb"
    )
    title_label.pack(pady=(15, 5))

    # hint label
    hint_label = tk.Label(
        card,
        text="Type or speak your command (e.g. 'open notepad', 'open chrome', 'open downloads', 'exit')",
        font=("Segoe UI", 10),
        bg="#111827",
        fg="#9ca3af",
        wraplength=520,
        justify="center"
    )
    hint_label.pack(pady=(0, 12))

    # entry container (for border effect)
    entry_frame = tk.Frame(card, bg="#111827")
    entry_frame.pack(pady=5, padx=30, fill="x")

    entry_border = tk.Frame(entry_frame, bg="#374151")
    entry_border.pack(fill="x")

    entry = tk.Entry(
        entry_border,
        font=("Consolas", 12),
        bg="#111827",
        fg="#f9fafb",
        insertbackground="#f9fafb",
        relief="flat"
    )
    entry.pack(ipadx=8, ipady=6, fill="x", padx=1, pady=1)

    # button bar frame
    btn_frame = tk.Frame(card, bg="#111827")
    btn_frame.pack(pady=15)

    def on_run():
        cmd = entry.get()
        if cmd.strip() == "":
            return
        if not handle_command(cmd):
            root.destroy()
            return
        entry.delete(0, tk.END)

    def on_voice():
        cmd = listen_voice()
        if cmd.strip() == "":
            return
        if not handle_command(cmd):
            root.destroy()

    def on_exit():
        speak("Goodbye")
        root.destroy()

    run_btn = tk.Button(
        btn_frame,
        text="Run Command",
        font=("Segoe UI", 11, "bold"),
        bg="#22c55e",
        fg="#0b1120",
        activebackground="#16a34a",
        activeforeground="#0b1120",
        relief="flat",
        padx=16,
        pady=6,
        cursor="hand2",
        command=on_run
    )
    run_btn.grid(row=0, column=0, padx=8)

    voice_btn = tk.Button(
        btn_frame,
        text="🎤 Voice",
        font=("Segoe UI", 11, "bold"),
        bg="#3b82f6",
        fg="#f9fafb",
        activebackground="#2563eb",
        activeforeground="#f9fafb",
        relief="flat",
        padx=16,
        pady=6,
        cursor="hand2",
        command=on_voice
    )
    voice_btn.grid(row=0, column=1, padx=8)

    exit_btn = tk.Button(
        btn_frame,
        text="Exit",
        font=("Segoe UI", 11, "bold"),
        bg="#ef4444",
        fg="#0b1120",
        activebackground="#b91c1c",
        activeforeground="#0b1120",
        relief="flat",
        padx=16,
        pady=6,
        cursor="hand2",
        command=on_exit
    )
    exit_btn.grid(row=0, column=2, padx=8)

    # Enter key runs command
    root.bind("<Return>", lambda event: on_run())

    # focus in entry
    entry.focus_set()

    speak("Assistant ready. Type or speak your command.")
    root.mainloop()

# ------------ MAIN ------------
if __name__ == "__main__":
    run_gui()
