import inquirer
from loaders import PDFLoader, WebLoader

questions = [
    inquirer.List(
        "download_type",
        message="Where do you want to download resources from?",
        choices=["Web", "PDF"],
    ),
]

answers = inquirer.prompt(questions)
if answers["download_type"] == "Web":
    url = input("Web URL: ")
    destination_folder = input("Destination Folder: ")
    WebLoader(url, destination_folder)
if answers["download_type"] == "PDF":
    pdf_path = input("PDF path: ")
    destination_folder = input("Destination Folder: ")
    PDFLoader(pdf_path, destination_folder)
