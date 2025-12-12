from googletrans import Translator

def dich_tieng_viet_sang_tieng_anh(text):
    translator = Translator()
    translation = translator.translate(text, src='vi', dest='en')
    return translation.text

def dich_tieng_anh_sang_tieng_viet(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='vi')
    return translation.text

if __name__ == "__main__":
    viet_text = "vãi lồn luôn nhỉ?"
    eng_text = "do you fuck me?"

    print("Dịch tiếng Việt sang tiếng Anh:")
    print(dich_tieng_viet_sang_tieng_anh(viet_text))

    print("\nDịch tiếng Anh sang tiếng Việt:")
    print(dich_tieng_anh_sang_tieng_viet(eng_text))