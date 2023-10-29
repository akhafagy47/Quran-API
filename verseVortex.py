import requests, pprint, arabic_reshaper

BASE_URL = 'https://api.quran.com/api/v4/'

def get_chapter(chapter_id):
    extension = f'chapters/{chapter_id}'
    full_url = BASE_URL+extension
    get_info = requests.get(full_url)
    final_data = get_info.json()
    return final_data

def format_chapter(info:dict):
    surah_name = info['name_simple']
    return surah_name
    
def pick_chapter():
    chapter_id = input('Insert the number of the chapter that you would like to see.\n')
    data = get_chapter(chapter_id)
    print(data)
    return data, chapter_id
def making_sure(answer):
    wrong = True
    while wrong:
        if answer.lower() == 'yes':
            return False
        elif answer.lower() == 'no':
            return True
        else:
            answer = input('Please enter Yes or No: ')
def get_arabic_verses():
    ext = 'quran/verses/uthmani_simple'
    full_url = BASE_URL+ext
    get_info = requests.get(full_url)
    data = get_info.json()
    return data
    
def format_arabic_verses(data, verse_count, surah_num):
    verses = data['verses']
    for i in range(1,(verse_count+1)):
        for verse in verses:
            if verse['verse_key'] == f'{surah_num}:{i}':
                a_verse = arabic_reshaper.reshape(verse['text_uthmani_simple'])
                print(a_verse[::-1])


def get_english_translation(chapter_id):
    ext = f'verses/by_chapter/{chapter_id}'
    full_url = BASE_URL+ext
    get_info = requests.get(f'http://api.alquran.cloud/v1/surah/{chapter_id}/en.asad')
    data = get_info.json()
    block = data['data']
    line = block["ayahs"]
    for text in line:
        text = text['text']
        print(text)

def get_audio(chapter_id):
    
    url = f'http://api.alquran.cloud/v1/surah/{chapter_id}/ar.alafasy'
    raw_data = requests.get(url)
    data = raw_data.json()
    set = data['data']
    row = set['ayahs']  
    num = 1
    for line in row:
        audio = line['audio']
        print(f'{num:>2}.', audio)
        num += 1
        
   

def get_command(answer, info, chapter_id):
    valid = False
    while not valid:
        if answer == 1:
            data = get_arabic_verses()
            format_arabic_verses(data, info['verses_count'], chapter_id)
            valid = True
        elif answer == 2:
            get_english_translation(chapter_id)
            valid = True
        elif answer == 3:
            get_audio(chapter_id)
            valid = True
        else:
            print('Not a valid response. Please try again:')
            answer = int(input('> '))
        


def main():
    data, chapter_id = pick_chapter()
    info = data['chapter']
    surah_name = format_chapter(info)
    print(f"You have chosen Surah {surah_name}, chapter {chapter_id} from the Qur'an")
    certainty = making_sure(input('Is this the Chapter you are looking for?\n'))
    while certainty:
        data, chapter_id = pick_chapter()
        info = data['chapter']
        surah_name = format_chapter(info)
        print(f"You have chosen Surah {surah_name}, chapter {chapter_id} from the Qur'an.")
        certainty = making_sure(input('Is this the Chapter you are looking for?\n'))
    #print('You made it!')
    dict_of_options = {1: "Read the Qur'an in the Arabic text", 2: "Read the English Translation of the Qur'an", 3: "Listen to Mishary's Recitation"}
    back = True
    while  back:
        for key,value in dict_of_options.items():
            print(f"{key}. {value}")
        get_command(int(input('> ')), info, chapter_id)
        if input('Go Back? (y/n) \n') == 'n':
            back = False
    

if __name__ == '__main__':
    main()
