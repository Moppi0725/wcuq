# encode: utf-8
import sys
import wcuq


def main():
    # ユーザIDのユーザトークンを取得する（string型）
    user_name = input("ユーザIDを入力してください：")
    user_token = input("トークンを入力してください：")
    # 今後にタグ指定する選択できるようにしたい

    print("ユーザID：{}\nユーザトークン：{}".format(user_name))
    wcuq.Wcuq(user_name, user_token)

# main関数の呼び出し
if __name__ == "__main__":

    # このモジュールのmain()を呼び出して結果を得て、Pythonシステムを修了する
    sys.exit(main())