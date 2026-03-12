import sys
from mini_django import httpServer
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

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()