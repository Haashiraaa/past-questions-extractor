

# __main__.py


if __name__ == "__main__":
    try:
        from engine.main import main
        main()
    except KeyboardInterrupt:
        print()
