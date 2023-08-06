"""The main script."""
from pkg_resources import resource_filename

# File resource, may be used as a normal file
ZIP_F_NAME = resource_filename(__name__, f"data/example.jpg")


def main():
    """The main function."""
    print(ZIP_F_NAME)
    return 0


if __name__ == "__main__":
    main()
