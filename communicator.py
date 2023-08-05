# ライブラリのインポート
import re
import requests
class Communicator:        
    def get_article_text(self, token, user_name, tag=''):
        res = self.request_qiita(token, user_name, tag, page="1")
        err, res_json = self.json_decode(res)
        if err != 0:
            return err, res_json
        
        article_text = self.get_rendered_body(res_json)
        
        return err, article_text
        
    
    def request_qiita(self, token, user_name, tag, page="1"):
        url = "https://qiita.com/api/v2/items"
        
        # headerの設定
        h = {
            'content-type'  : 'application/json',
            'charset'       : 'utf-8',
            'Authorization': 'Bearer ' + token,
            }
        
        # パラメータの設定
        params = {
            'page'      : page,
            'per_page'  : "100",
            'query'     : user_name,
            'tag'       : tag,
            }
        return requests.get(url,params=params, headers=h)
    
    def json_decode(self, res):
        #JSONにデコード
        res_json = res.json()
        # headerのtotal_caountの確認
        if  "Total-Count" in res.headers:
            total_count = res.headers["Total-Count"]
            if total_count == "0":
                return 1, "error: Username may be incorrect"
            
        elif type(res_json) is dict:
            return 2, f"error: The token may be wrong.\n message : {res_json['message']}, type : {res_json['type']}"
        
        return 0, res_json
    
    def get_rendered_body(self, res_json):
        article_text = ''
        
        for article in res_json:
            article_text += re.sub(re.compile('<.*?>'), '', article["rendered_body"])
            
        return article_text