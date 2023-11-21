from bs4 import BeautifulSoup
import pandas as pd
import requests


def get_data_from_url():
    """
    Function that opens vigoshop.si URL and parses data.
    return: Product list
    """
    
    url = 'https://vigoshop.si'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        ul_element = soup.find('ul', class_='products columns-4')

        # Extract information from li elements within the ul
        if ul_element:
            product_list = ul_element.find_all('li', class_='product')
            return product_list
    else:
        print('Napaka pri pridobivanju spletne strani. Status code:', response.status_code)
    return None


def generate_response(client, messages):
    """
    Call OpenAI ChatGPT (so far we will use GPT-3.5-turbo).
    :param client: OpenAI object
    :param messages: array of message rules
    return: response
    """
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=messages,
      temperature=0,
      max_tokens=256
    )
    return response


def get_data(online=True): 
    """
    Function that reads data from URL and saves it or reads saved data. 
    :param online: bool, whether we want to use real data or data from URL. 
    return: pd.DataFrame
    """
    filename = "products.csv"
    if online: 
        df = list()
        data = get_data_from_url()

        if data:
            for product in data:
                anchor = product.find('a')
                href = anchor.get('href')
                img = product.find('img')
                img_url = img.get('src')
                text = product.text.split("\n")[:3]
                price = text[2][:-1].replace(",", ".")
                name = text[1]
                df.append([name, price, href, img_url])

        column_names = ["name", "price", "href", "img_url"]
        df = pd.DataFrame(df, columns=column_names)
        df.to_csv(filename)
    else: 
        df = pd.read_csv(filename)
    return df


def prepare_input_messages(item_name, target_group, must_use_words, language="slovenian"):
    """
    Prepares messages with commands for ChatGPT.
    :param item_name: name of the item we want to sell
    :param target_group: name of target group
    :param must_use_words: Specific words that should be used
    :param language: Language in which ad will be created.
    return: list of json objects with messages.
    """
    # Prepare prompt messages to guide your ChatBot
    rules_slovenian = ""
    rules_english = "You are a helpful assistant for creating marketing ads on Facebook platform. You will use all knowladge to set up the most clickable ad." + \
                    "You know that facebook allows ad headers of length 40 characters and contrent of length 125 characters." + \
                    "Answer should be formed as header in one line, one empty line and content in third line. So it shoul have only 2 lines! First one with mamimum 40 characters and second with maximum 125 characters. " + \
                    f"Prepare response in {language} language"

    messages = [{"role": "system", "content": rules_english}]

    target_group_message = ""
    if target_group != "": 
        target_group_message = f" Create an ad to target {target_group}"
    
    must_use_words_message = ""
    if must_use_words != "": 
        must_use_words_message = f" You must use the following words in ad text: '{must_use_words}'"


    messages.append({"role": "user", "content": f"Create facebook add for: {item_name} (the name is in slovenian). THe header should not be item name. "
                                                + target_group_message
                                                + must_use_words_message
                                                + "You know that facebook allows ad headers of length 40 characters and contrent of length 125 characters."
                     })

    return messages


def create_ad(client, name, target_group, must_use_words, language=None):
    """
    Function that creates an ad.
    :param client: OpenAI client
    :param name: name of item we want to sell
    :param target_group: specific group we are targeting
    :param must_use_words: Words that need to be included.
    :param language: its language.
    return: test of ad.
    """

    messages = prepare_input_messages(name, target_group, must_use_words, language=language)
    generated_text = generate_response(client, messages)
    text = generated_text.choices[0].message.content

    return text
