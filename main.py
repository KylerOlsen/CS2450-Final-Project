import argparse

def server(host: str='', port: int=7788):
    from library import Library
    lib = Library(host, port)
    lib.serve_forever()

def client(playername: str, host: str='localhost', port: int=7788):
    pass

def main():
    pass

if __name__ == "__main__":
    main()
