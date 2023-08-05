import requests

class APIcovidTH:

    def __init__(self):
        self.UpdateDate = ""
        self.confirmed = ""
        self.NewConfirmed = ""
        self.Recovered = ""
        self.Hospitalized = ""
        self.Deaths = ""

    def __str__(self):
        txtLine = "อัพเดทข้อมูลล่าสุด: {}\nติดเชื้อสะสม: {}\nติดเชื้อรายใหม่: {}\nหายแล้ว: {}\nรักษาอยู่ใน รพ: {}\nเสียชีวิต: {}"\
                    .format(self.UpdateDate, self.confirmed, self.NewConfirmed, self.Recovered, self.Hospitalized, self.Deaths)
        return txtLine
    
    def callAPI(self):
        url = 'https://covid19.th-stat.com/api/open/today' 
        r = requests.get(url)
        result = r.json()
        self.UpdateDate = result['UpdateDate']
        self.confirmed = result['Confirmed']
        self.NewConfirmed = result['NewConfirmed']
        self.Hospitalized = result['Hospitalized']
        self.Recovered = result['Recovered']
        self.Deaths = result['Deaths']

    @staticmethod
    def LineNoti(tex, token):
        url = 'https://notify-api.line.me/api/notify'
        token = token
        headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
        msg = tex
        r = requests.post(url, headers=headers , data = {'message':msg})        
        print(r.text)


if __name__=="__main__":
    texdata = APIcovidTH()
    texdata.callAPI()
    APIcovidTH.LineNoti(texdata, token)