from . import *


def main() -> None:
    import sys
    if len(sys.argv[1:]) != 1:
        exit(1)
    command = sys.argv[1]
    if command == "server":
        def test(data: Any) -> str:
            return f"Data:\t{data}"
        functions = dict(test=test)
        SS(functions=functions).start()
        print("test socket server started.", flush=True)
    elif command == "client":
        for i in range(5):
            print(SC().request(command="test", data=f"Hello, {i}!"))
        print("test socket client started.", flush=True)
    else:
        exit(1)
    exit(0)


if __name__ == "__main__":
    main()
