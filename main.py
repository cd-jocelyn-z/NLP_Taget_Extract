from PyPDF2 import PdfReader
import pandas as pd
import os
from colorama import Fore, Back, Style


def all_pdfs():
    existing_pdfs = []

    for file in os.listdir():
        if file.endswith(".pdf"):
            existing_pdfs.append(file)
    return existing_pdfs


def user_views_pdfs():
    print(Fore.GREEN, "--------------------------- Welcome ------------------------------")
    print(Style.RESET_ALL, end="")
    
    current_directory = os.getcwd()
    print("You are running a Python script called NLP Targeted Extract!")
    print("Current directory:", current_directory,)
    print("Here is a list of the PDF files available for processing: ")

    for index, pdf in enumerate(all_pdfs(), start=1):
        print('   ',index, pdf)
    print()


def user_pdf_demand():
    print(Fore.GREEN, "--------------------- Initiating Process --------------------------")
    print(Style.RESET_ALL, end="")

    print("To get started, simply type in the number of the PDF you want to process and press Enter.")
    pdf_demand = int(
        input("    PDF: "))

    if pdf_demand > len(all_pdfs()):
        print("Typo? Which PDF would you like to process? ")
        pdf_demand = int(input("Please type in the number corresponding to the PDF: "))

    user_choice = (all_pdfs()[pdf_demand - 1])
    print("You are processing", "[", user_choice, "].")

    return user_choice


def user_page_demand(pdf_file):

    document_reader = PdfReader(pdf_file)
    document_size = document_reader.pages
    print("This PDF has", len(document_size), "pages. Only one page at a time is possible.")

    print("Enter the page number you want to process and hit Enter. ")
    page_demand = int(input("    Page: "))
    print()
    print(Fore.GREEN, "---------------------- Process complete ----------------------------")
    print(Style.RESET_ALL, end="")
    print("You will find two freshly generated files in the directory:")
    print("     1 .txt file containing the extracted text from page", page_demand)
    print("     1 .csv file with the frequency data of each word on page", page_demand)
    print()
    print("If you would like to process another page, please run the script again.")
    print()
    print("(Please note that if you run the script again, any files generated during this session "
          "will be deleted from your directory)")

    return page_demand


def page_text_extraction(pdf_path, page_number):
    document_reader = PdfReader(pdf_path)
    page = document_reader.pages[page_number]
    text = page.extract_text()

    return text


def write_text_to_file(page_extracted, page_number):
    existing_txt_files = []

    for file in os.listdir():
        if file.endswith(".txt"):
            existing_txt_files.append(file)

    # Store extracted txt file to a new txt file.
    if "page_{}.txt" not in existing_txt_files:
        txt_file_name = "page_{}.txt".format(page_number)
        file = open(txt_file_name, "w")
        file.write(page_extracted)
        file.close()

        return txt_file_name


def tokenize_txt_file(txt_file_path):
    path_to_txt_file = os.path.join(os.curdir, txt_file_path)
    with open(path_to_txt_file, "r") as file:
        lines = file.readlines()

        tokens_list = []

        for line in lines:
            line_content = line.split()
            for element in line_content:
                tokens_list.append(element)

        return tokens_list


def create_token_frequency_dict(token_list):
    token_frequency_dict = dict()

    for token in token_list:
        if token not in token_frequency_dict:
            token_frequency_dict[token] = 1
        else:
            token_frequency_dict[token] += 1

    return token_frequency_dict


def write_frequency_dict_to_csv(page_selected, token_frequency_dict):
    existing_csv_files = []

    for file in os.listdir():
        if file.endswith(".csv"):
            existing_csv_files.append(file)

    if "page_{}.csv".format(page_selected) not in existing_csv_files:
        csv_file_name = "page_{}.csv".format(page_selected)
        file = open(csv_file_name, "w")

        data = token_frequency_dict
        df = pd.DataFrame(data, index=[0])
        df = df.T
        df.to_csv(file, mode='w', header=True, index=True)
        file.close()

        return csv_file_name

def clear_session():

    extensions = ('.txt', '.csv')

    for file in os.listdir():
        for ext in extensions:
            if file.endswith(ext):
                os.remove(file)


clear_session()

user_views_pdfs()  
pdf_selected = user_pdf_demand()  
page_selected = user_page_demand(pdf_selected) 
page_text = page_text_extraction(pdf_selected, page_selected)  
text_path = write_text_to_file(page_text, page_selected)  
token_list = tokenize_txt_file(text_path)  
token_frequency_dict = create_token_frequency_dict(token_list) 
csv_file_name = write_frequency_dict_to_csv(page_selected, token_frequency_dict)
