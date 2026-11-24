
from JARVIS import listen, say
from browser import browseropen
from google import search_google

import datetime
import os
import time
import serial
import wikipedia

# ======================================
# ARDUINO SERIAL COMMUNICATION
# ======================================

ARDUINO_PORT = "COM5"
BAUD_RATE = 9600

arduino = None


def connect_arduino():
    global arduino

    try:
        arduino = serial.Serial(
            ARDUINO_PORT,
            BAUD_RATE,
            timeout=1,
            write_timeout=1
        )

        # Allow Arduino to reset
        time.sleep(2)

        print("Arduino connected successfully")

    except serial.SerialException as error:
        arduino = None
        print("Arduino connection failed:", error)


# ======================================
# SEND COMMANDS TO ARDUINO
# ======================================

def send_command(command):

    if arduino is None or not arduino.is_open:
        print("Arduino is not connected")
        say("Arduino is not connected")
        return False

    try:
        arduino.write(
            (command + "\n").encode("utf-8")
        )

        arduino.flush()

        print("Command sent:", command)
        return True

    except serial.SerialException as error:
        print("Serial communication error:", error)
        say("Unable to communicate with Arduino")
        return False


# ======================================
# SERVO MOTOR CONTROL
# ======================================

def start_servos():

    if send_command("START"):
        print("Starting all six servo motors")
        say("All six servo motors are moving")


def stop_servos():

    if send_command("STOP"):
        print("Stopping all six servo motors")
        say("All six servo motors have stopped")


# ======================================
# JARVIS MAIN FUNCTION
# ======================================

def main():

    say("Jarvis is now active, at your service sir")

    connect_arduino()

    print("================================")
    print("JARVIS AI VOICE ASSISTANT")
    print("================================")
    print("Available commands:")
    print("Start moving")
    print("Turn off")
    print("Browser")
    print("Time")
    print("Code")
    print("VLC")
    print("Power BI")
    print("Microsoft Word")
    print("Wikipedia")
    print("Search")
    print("Exit")
    print("================================")

    while True:

        try:
            print("\nListening for command...")

            task = listen()

            if not task:
                continue

            task = task.lower().strip()

            print("Recognized:", task)

            # ===========================
            # SERVO MOTOR COMMANDS
            # ===========================

            if "start moving" in task:
                start_servos()

            elif (
                "turn off" in task
                or "stop moving" in task
                or "stop servo motors" in task
            ):
                stop_servos()

            # ===========================
            # EXISTING JARVIS COMMANDS
            # ===========================

            elif "browser" in task:
                result = browseropen(task)
                say(result)

            elif "time" in task:
                dt = datetime.datetime.now().strftime(
                    "%H Hours and %M Minutes"
                )
                print(dt)
                say(f"Time is {dt}")

            elif "code" in task:
                os.startfile(
                    "C:/Users/DELL/Downloads/"
                    "VSCodeUserSetup-x64-1.91.1 (1).exe"
                )

            elif "vlc" in task:
                os.startfile(
                    "C:/Program Files/VideoLAN/VLC"
                )

            elif "power bi" in task:
                os.startfile(
                    "C:/Users/Public/Desktop/"
                    "Power BI Desktop.lnk"
                )

            elif "microsoft word" in task:
                os.startfile(
                    "C:/ProgramData/Microsoft/Windows/"
                    "Start Menu/Programs/Word.lnk"
                )

            elif "music" in task:
                os.startfile(
                    "C:/Users/Admin/Downloads/"
                    "(24 Bit)ACDC-Back In Black-06-"
                    "Back In Black.mp3"
                )

            elif "wikipedia" in task:
                query = task.replace("wikipedia", "").strip()

                if query:
                    result = wikipedia.summary(
                        query, sentences=3
                    )
                    print(result)
                    say(result)

            elif "search" in task:
                query = task.replace("search", "").strip()

                if query:
                    result = search_google(query)
                    print(result)
                    say(result)

            # ===========================
            # EXIT JARVIS
            # ===========================

            elif "exit" in task or "goodbye" in task:
                send_command("STOP")
                say("Shutting down Jarvis. Goodbye sir")
                break

            else:
                print("Command not recognized")

        except Exception as error:
            print("Error:", error)

    if arduino is not None and arduino.is_open:
        arduino.close()


# ======================================
# PROGRAM ENTRY POINT
# ======================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nKeyboard interruption detected")
        send_command("STOP")

        if arduino is not None and arduino.is_open:
            arduino.close()
