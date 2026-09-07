import sys
from mini_django import httpServer, send_mail
import urls


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        return

    command = sys.argv[1]

    if command == "runserver":
        port = 9000

        if len(sys.argv) > 2:
            port = int(sys.argv[2])

        httpServer(urls.router, port)

    elif command == "routes":
        print("Registered routes:")
        for route in urls.routes:
            print(" -", route)

    elif command == "shell":
        import code
        code.interact(local=globals())

    elif command == "sendmail":
        email = input('email address:')
        password = input('password:')
        subject = input('subject:')
        from_address = input('from_address:')
        to_address = input('to_address:')
        send_mail(email=email, password=password, subject=subject, from_address=from_address, to_address=to_address)            

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()