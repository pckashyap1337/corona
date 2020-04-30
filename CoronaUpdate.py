from tkinter import *
import json
import requests
import os
from PIL import Image

# Getting latest corona updates from internet
url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

headers = {
    'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
    'x-rapidapi-key': "77a2972042mshaced7afc764ba15p119e95jsn92bb3beb8886"
}

root = Tk()
root.geometry('700x530')
root.title('Corona Update by PCKashyap')
root.resizable(0,0)

try:
    # root.call('wm', 'iconphoto', root._w, PhotoImage(file='./corona/icon.png'))
    root.iconbitmap('./corona/icon.ico')
except:
    # creating file called corona in current location
    if not os.path.exists('./corona'):
        os.mkdir('./corona')
    # fetching image or corona icon from Internet
    coronaIcon = requests.get('https://cdn.datta.store/auxapi/files/image/virus.png').content
    with open('./corona/icon.png', 'wb') as response:
        response.write(coronaIcon)
    # resizing icon size
    imgPath = Image.open('./corona/icon.png')
    if imgPath.width > 32 or imgPath.height > 32:
        new_icon_size = (32, 32)
        imgPath.thumbnail(new_icon_size)
        imgPath.save('./corona/icon.ico')
    # setting icon
    root.iconbitmap('./corona/icon.ico')


# all variables
stateVar = StringVar()
districtVar = StringVar()
infectedDistricts = StringVar()
lastUpdatedTime = ''

status = ''
states = list()
districts = list()

try:
    data = requests.request("GET", url, headers=headers).json()
    status = 'Latest Data from Internet'
    # writing in file
    with open('./corona/corona.json', 'w') as f:
        latest_data = json.dumps(data, indent=2)
        f.write(latest_data)
except Exception:
    try:
        with open('./corona/corona.json') as f:
            data = json.load(f)
            status = 'Old Data, {Please connect to Internet to get Latest Data}'
    except Exception:
        status = 'Something went wrong! Please to Internet to fix this issue.'


try:
    # last update time
    lastUpdatedTime = data['total_values']['lastupdatedtime']
    # getting states name
    for state in data['state_wise']:
        states.append(state)
    stateVar.set(states[states.index('Chhattisgarh')])
except Exception:
    status = 'Something went wrong! Please to Internet to fix this issue.'


# All functions

def refresh():
    root.destroy()
    exec(open("./CoronaUpdate.py").read())

def allDistricts():
    all_districts = ''

    stateName = stateVar.get().strip()
    stateMsg = f'Infected Districts of {stateName} :'
    # to get all districts name
    try:
        for district in data['state_wise'][stateName]['district']:
            if district == 'Unknown' or district == 'Other States':
                continue
            all_districts += district + ", "
            districts.append(district)
        districts.reverse()
        # 
        districtVar.set(districts[0])
    except Exception:
        status = 'something went wrong. Please to Internet to fix this issue'
    # 

    districts_title = Label(root, text=stateMsg, font=('arial', 13, 'bold'), fg='red')
    districts_title.place(x=85, y=147)

    all_infected_districts = Text(root, state='disabled' , relief='solid', height=5, width=64)
    all_infected_districts.place(x=85, y=184)

    # inserting districts name
    all_infected_districts.configure(state='normal')
    all_infected_districts.insert('end', all_districts + '\n')
    all_infected_districts.configure(state='disabled')

    district_name = Label(root, text="Select District Name: ", font=('arial', 15, 'bold'))
    district_name.place(x=85, y=289)

    try:
        district_input = OptionMenu(root, districtVar, *districts)
        district_input.place(x=288, y=291)
    except Exception:
        globals()['status']  = 'Something went wrong! Please to Internet to fix this issue.'

    submit_btn2 = Button(root, text='Submit', width=10, bg='green', fg='white', command=results)
    submit_btn2.place(x=520, y=290)

def results():
    state_wise_results = ''
    district_wise_results = ''
    indiaUpdate = ''
    stateName = stateVar.get()

    
    districtName = districtVar.get()

    try:
        # to get district wise result
        for districtResult in data['state_wise'][stateName]['district'][districtName]:
            if districtResult == 'notes' or districtResult == 'delta':
                continue
            district_wise_results += districtResult + " : " + str(data['state_wise'][stateName]['district'][districtName][districtResult]) + "\n"

        # to get state wise result
        for stateResult in data['state_wise'][stateName]:
            if stateResult == 'state' or stateResult == 'statecode' or stateResult == 'statenotes' or stateResult == 'district' or stateResult == 'lastupdatedtime' or stateResult == 'deltaconfirmed' or stateResult == 'deltadeaths' or stateResult == 'deltarecovered':
                continue
            state_wise_results += stateResult + " : " + str(data['state_wise'][stateName][stateResult]) + '\n'

        # getting Corona updates of India
        for IndiaUpdates in data['total_values']:
            if IndiaUpdates == 'lastupdatedtime' or IndiaUpdates == 'state' or IndiaUpdates == 'statecode' or IndiaUpdates == 'statenotes' or IndiaUpdates == 'deltaconfirmed' or IndiaUpdates == 'deltadeaths' or IndiaUpdates == 'deltarecovered':
                continue
            indiaUpdate += IndiaUpdates + " : " + data['total_values'][IndiaUpdates] + "\n"
    except Exception:
        status = 'something went wrong. Please to Internet to fix this issue'

    
    
    # results
    result_label = Label(root, text='Results of:', font=('arial', 10, 'bold'))
    result_label.place(x=85, y=320)

    district_label = Label(root, text=f'"{districtName}"', font=('arial', 12, 'bold'))
    district_label.place(x=85, y=345)

    district_results = Text(root, state='disabled', width=20, height=6, relief='solid')
    district_results.place(x=85, y=370)

    district_results.configure(state='normal')
    district_results.insert('end', district_wise_results)
    district_results.configure(state='disabled')

    state_label = Label(root, text=f'"{stateName}"', font=('arial', 12, 'bold'))
    state_label.place(x=256, y=345)

    state_results = Text(root, state='disabled', width=20, height=6, relief='solid')
    state_results.place(x=257 ,y=370)

    state_results.configure(state='normal')
    state_results.insert('end', state_wise_results)
    state_results.configure(state='disabled')

    india_label = Label(root, text='"India"', font=('arial', 12, 'bold'))
    india_label.place(x=473, y=345)

    india_results = Text(root, state='disabled', width=21, height=6, relief='solid')
    india_results.place(x=430 ,y=370)

    india_results.configure(state='normal')
    india_results.insert('end', indiaUpdate)
    india_results.configure(state='disabled')

def exitMe():
    root.destroy()

def mainWindow():
    # main title
    Label(root, text='Get Latest Corona Updates:', font=('arial', 20, 'bold'), fg='green').pack()
    # lastUpdatedTime
    Label(root, text=f"Last Updated Time: {lastUpdatedTime}", font=('arial', 12, 'bold')).pack()
    # status
    Label(root, text=status, font=('arial', 14, 'bold'), fg='red').pack()

    state_name = Label(root, text="Select State Name: ", font=('arial', 16, 'bold'))
    state_name.place(x=85, y=106)

    try:
        state_options = OptionMenu(root, stateVar, *states)
        state_options.place(x=285, y=110)
    except Exception:
        globals()['status']  = 'Something went wrong! Please to Internet to fix this issue.'

    submit_btn1 = Button(root, text='Submit', width=10, bg='green', fg='white', command=allDistricts)
    submit_btn1.place(x=520, y=110)

    exit_btn = Button(root, text='Exit', width=10, bg='red', fg='white', command=exitMe)
    exit_btn.place(x=310, y=490)

    # refresh_btn = Button(root, text='Refresh', width=10, bg='red', fg='white', command=refresh)
    # refresh_btn.place(x=380, y=465)

# calling main window
mainWindow()
root.mainloop()
