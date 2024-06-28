import datetime
import os
import shutil
import zipfile


def extract_zip(file_path, extract_to):
    """
    Extracts the contents of a zip file to the specified directory.

    Args:
        file_path (str): The path to the zip file.
        extract_to (str): The directory to extract the contents to.
    """
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def is_file_type(file_path, extensions):
    """
    Checks if a file is of a specified type based on its extension.

    Args:
        file_path (str): The path to the file.
        extensions (tuple): A tuple of file extensions to check against.

    Returns:
        bool: True if the file matches one of the extensions, False otherwise.
    """
    return file_path.lower().endswith(extensions)


def get_creation_date(file_path):
    """
    Gets the creation date of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        datetime.datetime: The creation date of the file.
    """
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t)


def generate_unique_filename(directory, filename):
    """
    Generates a unique filename by appending a counter if a file with the
    same name exists.

    Args:
        directory (str): The directory to check for existing files.
        filename (str): The original filename.

    Returns:
        str: A unique filename.
    """
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1
    return new_filename


def organize_files(source_dir, dest_dir):
    """
    Organizes files from the source directory into the destination
    directory based on their creation date.

    Args:
        source_dir (str): The source directory containing files to organize.
        dest_dir (str): The destination directory to organize files into.

    Returns:
        tuple: A tuple containing lists of copied files and remaining files.
    """
    copied_files = []
    remaining_files = []

    picture_extensions = (".jpeg", ".jpg", ".png", ".heif")
    video_extensions = (".mp4", ".mov")
    audio_extensions = ".wav"

    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            creation_date = get_creation_date(file_path)
            year = creation_date.strftime("%Y")
            month = creation_date.strftime("%B")

            if is_file_type(file, picture_extensions):
                category = "Pictures"
            elif is_file_type(file, video_extensions):
                category = "Videos"
            elif is_file_type(file, audio_extensions):
                category = "Audio"
            else:
                remaining_files.append(file_path)
                continue

            target_dir = os.path.join(dest_dir, "kids", year, month, category)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            unique_filename = generate_unique_filename(target_dir, file)
            target_file_path = os.path.join(target_dir, unique_filename)
            shutil.copy2(file_path, target_file_path)
            copied_files.append(target_file_path)

    return copied_files, remaining_files


def clean_up(directory):
    """
    Deletes the specified directory and all its contents.

    Args:
        directory (str): The directory to delete.
    """
    if os.path.exists(directory):
        shutil.rmtree(directory)


def process_zip_and_organize_files():
    """
    Processes a zip file by extracting its contents and organizing the files.

    Extracts the zip file from a predefined download directory, organizes
    the files into a destination directory based on their creation date,
    and performs cleanup if all files are processed.
    """
    download_dir = "/path/to/downloaded/zips"
    extract_to = "/path/to/extracted/files"
    dest_dir = "/path/to/destination/directory"

    # Assume the downloaded zip file is named 'iCloud_backup.zip'
    zip_file_path = os.path.join(download_dir, "iCloud_backup.zip")

    # Extract the zip file
    extract_zip(zip_file_path, extract_to)

    # Organize the files
    copied_files, remaining_files = organize_files(extract_to, dest_dir)

    # Print copied files
    print("Copied and organized files:")
    for file in copied_files:
        print(file)

    # Print remaining files
    if remaining_files:
        print("\nFiles not processed (remaining in the extracted directory):")
        for file in remaining_files:
            print(file)

    # Clean up only if there are no remaining files
    if not remaining_files:
        clean_up(extract_to)
        os.remove(zip_file_path)
        print(
            "\nCleanup successful: All extracted files have been processed \
                and directories removed."
        )
    else:
        print(
            "\nCleanup not performed: There are unprocessed files \
                remaining in the extracted directory."
        )


def organize_existing_files():
    """
    Organizes files from an existing directory into a destination directory.

    Organizes the files from a predefined source directory into a
    destination directory based on their creation date.
    """
    source_dir = "/path/to/existing/files"
    dest_dir = "/path/to/destination/directory"

    # Organize the files
    copied_files, remaining_files = organize_files(source_dir, dest_dir)

    # Print copied files
    print("Copied and organized files:")
    for file in copied_files:
        print(file)

    # Print remaining files
    if remaining_files:
        print("\nFiles not processed (remaining in the source directory):")
        for file in remaining_files:
            print(file)


if __name__ == "__main__":
    # Uncomment the function you want to run
    # process_zip_and_organize_files()
    organize_existing_files()
