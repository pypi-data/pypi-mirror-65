from htmldom import htmldom
import urllib
import re

def update():
    dom = htmldom.HtmlDom("https://beta.wikiversity.org/w/index.php?title=%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90&action=edit&section=56")
    dom = dom.createDom()

    ta = dom.find("textarea")
    html, s = ta.html(), ta.html()

    s = s.split('\n')[11:]
    list_of_lists = []
    new_list_of_lists = []
    l = []
    i = 0

    while i < len(s) - 5:
        l = [s[i], s[i + 1], s[i + 2], s[i + 3], s[i + 4]]
        list_of_lists.append(l)
        l = []

        i = i + 5

    i = 0

    while i < len(list_of_lists):
        new_list_of_lists.append([list_of_lists[i][0][2:], list_of_lists[i][2][2:]])
        i = i + 1


    ninjas = []

    for ninja in new_list_of_lists:
        print(ninja)

        try:
            name_and_link = ninja[0].split('[')
            ninjas_name = name_and_link[0]
            codewars_link = name_and_link[1][:-1]

        except:
            print('There is no link in the wikiversity for this user')
            continue

        try:
            dom = htmldom.HtmlDom(str(codewars_link)).createDom()
        except Exception as err:
            print('link caused error: ', err, '\n')
            continue

        stats = dict(re.findall(r'<\w+\s+class=\"stat[\w\s\-_]*\">\s*<[\w\s\-_]+>\s*([^:]+):\s*</[\w\s\-_]+>\s*([^\n]+)', dom.find('div[class~=stat-box]').html()))
        stats['Nickname'] = ninjas_name
        stats['Link'] = codewars_link
        ninjas.append(stats)
        print(stats, '\n')

    completed = sorted(ninjas, key = lambda i : float(i['Honor Percentile'][4:][:-1]))


    basic = '''
    ===משתתפים באתגר <span dir="ltr">This means war</span>===
    * סטטוס: מרץ 2020

    {| class="wikitable sortable"  style="background:black; color:red;" dir="ltr"
    |-
    ! Nickname
    ! Kyu
    ! top Precentage
    ! Leaderboard (Beta Kyu)
    '''

    for a in completed:
        leaderboard_position = int(''.join(a['Leaderboard Position'][1:].split(',')))

        leaderboard_position_color_code = 0
        if leaderboard_position <= 100: leaderboard_position_color_code = 1
        elif leaderboard_position <= 1000: leaderboard_position_color_code = 2
        elif leaderboard_position <= 5000: leaderboard_position_color_code = 3
        elif leaderboard_position <= 15000: leaderboard_position_color_code = 4
        elif leaderboard_position <= 50000: leaderboard_position_color_code = 5
        elif leaderboard_position <= 100000: leaderboard_position_color_code = 6
        elif leaderboard_position <= 150000: leaderboard_position_color_code = 7
        elif leaderboard_position <= 200000: leaderboard_position_color_code = 8
        else: leaderboard_position_color_code = 0
        leaderboard_position_background_color = ['pink', 'black', 'red', 'purple', 'blue', 'green', 'orange', 'yellow', 'white'][leaderboard_position_color_code]
        leaderboard_position_text_color = 'white' if leaderboard_position_color_code < 5 else 'black'

        kyu = int(a['Rank'][:1])
        kyu_background_color = 'black' if kyu == 1 else 'purple' if kyu == 2 else 'blue' if kyu == 3 or kyu == 4 else 'yellow' if kyu == 5 or kyu == 6 else 'white' if kyu == 7 or kyu == 8 else 'pink'
        kyu_text_color = 'red' if kyu == 1 else 'white' if kyu <= 4 else 'black'

        basic += '|-\n| ' + a['Nickname'] + '[' + codewars_link + a['Link'] + ']\n| style="background:' + kyu_background_color + '; color:' + kyu_text_color + '"| ' + a['Rank'][:1] + '\n| ' + a['Honor Percentile'][4:] + '\n| style="background:' + leaderboard_position_background_color + '; color:' + leaderboard_position_text_color + '"| ' + a['Leaderboard Position'][1:] + '\n'

    basic += '|}'

    print(completed, '\n')
    print(basic)
