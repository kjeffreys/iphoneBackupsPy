import datetime
import os
import shutil
import zipfile


def extract_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def is_file_type(file_path, extensions):
    return file_path.lower().endswith(extensions)


def get_creation_date(file_path):
    t = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(t)


def organize_files(source_dir, dest_dir):
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

            target_dir = os.path.join(
                dest_dir, "family", year, month, category
            )  # noqa: E501
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            target_file_path = os.path.join(target_dir, file)
            shutil.copy2(file_path, target_file_path)
            copied_files.append(target_file_path)

    return copied_files, remaining_files


def clean_up(directory):
    if os.path.exists(directory):
        shutil.rmtree


def main():
    # download_dir = 'path/to/downloaded/zips'
    download_dir = "path/to/downloaded/zips"

    # extract_to = 'path/to/extracted/files'
    extract_to = "path/to/downloaded/zips"

    # download_dir = 'path/to/destination/directory'
    dest_dir = "path/to/downloaded/zips"

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


if __name__ == "__main__":
    main()
