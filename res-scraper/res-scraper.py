from loaders import WebLoader, PDFLoader
import inquirer

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
    PDFLoader("C:\\Users\\loren\\Dropbox\\cartella_condivisa\\enami.it\\Clienti\\Antica birreria San Filippo\\Bevande Menu A5 Vini Italiani.pdf","C:\\Users\\loren\\Desktop")