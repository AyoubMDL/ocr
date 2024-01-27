"""# Import packages"""

from PIL import Image
import pytesseract
import pandas as pd
from utils import get_role_names, get_company_names, get_first_last_names

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def img_to_txt(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def remove_digits(name):
    # Check if the name contains digits
    if any(char.isdigit() for char in name):
        # Remove leading numeric prefix (enclosed in parentheses) and leading/trailing spaces
        cleaned_name = ' '.join(part.strip() for part in name.split(' ')[1:])
        return cleaned_name.strip()
    else:
        return name


def remove_prefix(name):
    # Check if the name starts with two lowercase letters
    if name[:2].islower():
        # Remove the first two letters and leading/trailing spaces
        cleaned_name = name[2:].strip()
        return cleaned_name
    else:
        return name


def clean_name(name):
    name = remove_digits(name)
    name = remove_prefix(name)
    return name


def extract_names(text):
    # Split the text into a list based on line breaks
    text_list = text.split('\n')

    # Find the index of the item containing "Attendee Networking"
    start_index = next(i for i, item in enumerate(text_list) if 'Attendee Networking' in item)

    # Create a new list starting from that index
    new_list = text_list[start_index+1:]

    # Remove empty strings from the new list
    new_list = [item.strip() for item in new_list if item.strip()]

    names_list = [new_list[i] for i in range(0, len(new_list) - 1, 2)]
    names_list = [clean_name(name) for name in names_list]
    first_names, last_names = get_first_last_names(names_list)

    description_list = [new_list[i] for i in range(1, len(new_list) - 1, 2)]
    company_names = get_company_names(description_list)
    role_names = get_role_names(description_list)

    return first_names, last_names, role_names, company_names


def ocr(image_path):
    text = img_to_txt(image_path)
    names_list = extract_names(text)

    return names_list


def create_dataframe(first_names, last_names, role_names, company_names, filename):
    df = pd.DataFrame({'First Name': first_names,
                       'Last Name': last_names,
                       'Role': role_names,
                       'Company': company_names})
    # # Save the DataFrame to an Excel file
    # df.to_excel(f'{filename}.xlsx', index=False)
    # print("Excel file 'cleaned_names.xlsx' created successfully.")
    return df


def ocr_to_df(image_path):
    first_names, last_names, role_names, company_names = ocr(image_path)
    excel_filename = "extracted_names.xlsx"
    df = create_dataframe(first_names, last_names, role_names, company_names, excel_filename)
    return df


if __name__ == "__main__":
    df = ocr_to_df("ocr_img/IMG_2465.PNG")
    # df.to_excel(f'test.xlsx', index=False)
