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

if __name__=="__main__":
    c = APIcovidTH()
    c.callAPI()
    print(c)