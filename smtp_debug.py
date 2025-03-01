import socket

def test_smtp_resolution():
    try:
        host = socket.gethostbyname("smtp.gmail.com")
        print(f"Resolved host: {host}")
    except socket.gaierror as e:
        print(f"Hostname resolution error: {e}")

if __name__ == "__main__":
    print("Testing SMTP hostname resolution...")
    test_smtp_resolution()
