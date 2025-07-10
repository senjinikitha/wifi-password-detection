# importing subprocess
import subprocess

# getting meta data
meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

# decoding meta data
data = meta_data.decode('utf-8', errors="backslashreplace")

# splitting data by line by line
data = data.split('\n')

# creating a list of profiles
profiles = []

# traverse the data
for i in data:

    # find "All User Profile" in each item
    if "All User Profile" in i:
        # split the item
        i = i.split(":")

        # get the WiFi name and clean it
        i = i[1].strip().strip('"')

        # append to the profiles list
        profiles.append(i)

# printing heading
print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
print("----------------------------------------------")

# traversing the profiles
for i in profiles:

    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])

        # decode and split
        results = results.decode('utf-8', errors="backslashreplace")
        results = results.split('\n')

        # get password
        results = [b.split(":")[1].strip() for b in results if "Key Content" in b]

        try:
            print("{:<30}| {:<}".format(i, results[0]))
        except IndexError:
            print("{:<30}| {:<}".format(i, ""))

    except subprocess.CalledProcessError:
        print("Encoding Error Occurred")
