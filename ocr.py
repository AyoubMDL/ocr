"""# Import packages"""

from PIL import Image
import pytesseract
import pandas as pd
from utils import get_role_names, get_company_names, get_first_last_names

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


def img_to_txt(image_path):
    img = Image.open(image_path)
    img = img.crop((280, 350, 1223, img.size[1]))
    text = pytesseract.image_to_string(img)
    return text


def extract_names(text):
    # Split the text into a list based on line breaks
    text_list = text.split('\n')

    # Remove empty strings from the new list
    new_list = [item.strip() for item in text_list if item.strip()]

    names_list = [new_list[i] for i in range(0, len(new_list) - 1, 2)]
    first_names, last_names = get_first_last_names(names_list)

    description_list = [new_list[i] for i in range(1, len(new_list), 2)]
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
    text = img_to_txt("ocr_img/IMG_2828.png")
