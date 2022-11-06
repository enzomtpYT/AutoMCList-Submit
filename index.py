import pymysql, json, requests, os, threading, time, locale
locale.setlocale(locale.LC_TIME,'')

# Verify, Create the logs.txt
ls = open("logs.txt", "w")
ls.write("")
ls.close()
print("created file")
logs = open('./logs.txt')

def logger(txt):
    act = time.strftime('%d/%m/%Y %H:%M:%S')
    md = "["+act+"] "+str(txt)
    print(md)
    with open("./logs.txt", "a", encoding="utf-8") as lg:
        lg.write(md+"\n")


# Verify, Create and Read the data.json
if os.path.isfile("./data.json"):
    data = json.load(open('./data.json'))
    logger(data)
else:
    f = open("data.json", "x")
    data = {
               "alreadyin":[]
            }
    with open('data.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    logger("created file")
    f.close()
    data = json.load(open('./data.json'))
    logger(data)

count = 0

def sendrq(ip):
    global count
    if ip not in data["alreadyin"]:
        res = requests.request("POST", "https://mcl.ist/api/server/submit", data="{\"server\": \""+ip+"\"}", headers={'content-type': "application/json"})
        if res.text == '':
            if res.status_code == 429:
                threading.Thread(target=sendrq(ip))
            else:
                logger("error, status code : "+res.status_code)
        else:
            data["alreadyin"].append(ip)
            logger(res.text)
            with open('data.json', 'w') as f:
                json.dump(data, f, ensure_ascii=False)
    count+=1
    logger(str(count))

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='ENTER PASSWORD', db='YOUR DB', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cr = conn.cursor()
cr.execute("SELECT IpAddress FROM servers")
for a in cr.fetchall():
    threading.Thread(target=sendrq(a["IpAddress"]))
