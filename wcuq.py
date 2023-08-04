from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import communicator as co
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class wcuq:
    def __init__(self, name, token):
        self.name = name
        self.token = token

# Function to read stopwords from a file
def read_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        stopwords = [line.strip() for line in file]
    return stopwords

# Function to tokenize text using Janome and extract only nouns and adjectives
def tokenize_and_extract_nouns_adjectives(text):
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize(text)
    words = []
    for token in tokens:
        # 名詞と形容詞の場合のみ単語を抽出
        if '名詞' in token.part_of_speech or '形容詞' in token.part_of_speech:
            words.append(token.base_form)
    return words

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) //2 ))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)

    return img

def createwordclowd(extracted_words):
    # Read stopwords from the file
    stopwords_file = '/stop_words.txt'
    stopwords = read_stopwords(stopwords_file)
    wordcloud = WordCloud(font_path='/ipam00303/ipam.ttf', max_words=100, stopwords=stopwords, background_color='white', max_font_size=50).generate(' '.join(extracted_words))
    # # Word Cloudを描画
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')  # 軸を表示しないように設定
    # Word Cloudの画像をファイルに保存
    output_file_path = '/wordcloud_output.png'
    wordcloud.to_file(output_file_path)
    im = Image.open(output_file_path)
    return im

# テキストデータ（サンプルとして文章を使用）
def get_wcuq(self):
    com = co.Communicator()
    errorcord, text_data = co.get_article_text(user_name=self.name, token=self.token)
    if errorcord == 0:
        # 名詞と形容詞のみを抽出する
        extracted_words = tokenize_and_extract_nouns_adjectives(text_data)
        im = createwordclowd(extracted_words)
        im_new = expand2square(im, (0, 0, 0))
        im_new.save('/wordcloud_output_padding.png', quality=95)
        #plt.show()
        text_to_draw = self.name
        font_path = "/ipam00303/ipam.ttf"
        font_size = 20
        font_color = (255, 255, 255)
        height = 0
        width = 0
        img = add_text_to_image(im_new, text_to_draw, font_path, font_size, font_color, height, width)
        final_output_path = '/user_wordclowd.png'
        img.save()
        user_wordclowd = Image.open(final_output_path)
        return user_wordclowd
    else:
        print(f"errorcord : {errorcord}, text : {text_data}")
        return None