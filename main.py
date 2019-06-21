# -*- code = utf-8 -*-

import os
import re
import json
import MySQLdb


# -----------------------------------------------------------------------

DBList = dict()
Language = dict()
SelectLanguage = "English"
NewSQL = None
OldSQL = None

# ==================================================[Drive SQL]


def LinkSQL(name, host, user, passwd, db):
    try:
        db = MySQLdb.connect(host=host, user=user,
                             passwd=passwd, db=db, charset="utf8",
                             read_timeout=10, write_timeout=10,
                             connect_timeout=5)
    except MySQLdb._exceptions.OperationalError as e:
        print(
            f"{Colors(255,0,0)}{Language[SelectLanguage]['ErrorFrom']}{e}{ColorsEnd()}")
        return "ERROR"
    DBList[name] = {
        "DB": db,
        "Cursor": db.cursor()
    }
    return None


def Close():
    for db in DBList.values():
        db["DB"].close()

# ---------------------------------------------------------------------[SQL]


def LoadDBDate(name=""):
    SQLDataList = list()
    count = 0
    for i in os.listdir("./sql"):
        if name == "":
            count += 1
            SQLDataList.append(os.path.join(".", "sql", i))
            print(f"\t{count} : {i}")
        elif name == i:
            return os.path.join(".", "sql", i)
    return SQLDataList


def LoadSQL(path):
    with open(path, "r", encoding="utf-8") as sqlData:
        return sqlData.read()


# ==================================================[Select]

def Display(select):
    if select == 0:
        print(f"""
        {Language[SelectLanguage]["Hello"]}
        """)
    elif select == 1:
        print(f"""
\t{Colors(0,255,0)}{"="*150}{ColorsEnd()}
{" "*72}{Colors(255,0,0)} -1：{Language[SelectLanguage]["Exit"]} {ColorsEnd()}
        
{" "*72}{Colors(0,255,255)}-2：{Language[SelectLanguage]["ReLoad"]}{ColorsEnd()}
        """)
    elif select == 2:
        print(f"""
\t{Colors(0,255,0)}{"="*150}{ColorsEnd()}
{" "*72}{Colors(255,0,0)} -1：{Language[SelectLanguage]["Exit"]} {ColorsEnd()}
        
{" "*72}{Colors(0,255,255)}-2：{Language[SelectLanguage]["Clear"]}{ColorsEnd()}
{" "*72}{Colors(0,255,255)}-3：{Language[SelectLanguage]["ReSDB"]}{ColorsEnd()}

{" "*70}{Colors(255,255,255)}0：{Language[SelectLanguage]["Select0"]}{ColorsEnd()}
{" "*70}{Colors(255,255,255)}1：{Language[SelectLanguage]["Select1"]}{ColorsEnd()}
{" "*70}{Colors(255,255,255)}2：{Language[SelectLanguage]["Select2"]}{ColorsEnd()}
{" "*70}{Colors(255,255,255)}3：{Language[SelectLanguage]["Select3"]}{ColorsEnd()}
{" "*70}{Colors(255,255,255)}4：{Language[SelectLanguage]["Select4"]}{ColorsEnd()}
\t{Colors(0,255,0)}{"="*150}{ColorsEnd()}
""")


def SelectFunc():
    Display(2)
    select = input(
        f"\t{Colors(255,255,255)}{Language[SelectLanguage]['SelectFunc']}{ColorsEnd()}")
    if select == "0":
        Function_0()
    elif select == "1":
        Function_1()
    elif select == "2":
        Function_2()
    elif select == "3":
        Function_3()
    elif select == "4":
        Function_4()
    elif select == "-2":
        if os.name == 'nt':
            os.system("cls")
        elif os.name == 'posix':
            os.system("clear")
    elif select == "-3":
        Init()
    elif select == "-1":
        return "exit"

    return None

# ==================================================[Select Function]


def Function_0():
    PathA = LoadDBDate("DataA.sql")
    if len(PathA) == 0:
        print(f"\t{Language[SelectLanguage]['NotSQLData']}")
        return "Not SQL Data"
    PathB = LoadDBDate("DataB.sql")
    if len(PathB) == 0:
        print(f"\t{Language[SelectLanguage]['NotSQLData']}")
        return "Not SQL Data"
    Look(PathA, PathB, True)


def Function_1():
    try:
        DataList = LoadDBDate()
        select = int(input(f"\t{Language[SelectLanguage]['SelectFile']}"))-1
        Path = DataList[select]
        Look(Path, Path, True)
    except KeyboardInterrupt:
        return None
    except IndexError:
        print(
            f"\n{Colors(255,0,0)}======{Language[SelectLanguage]['InputError']}======{ColorsEnd()}\n")
        Function_1()


def Function_2():
    try:
        DataList = LoadDBDate()
        PathA = DataList[int(
            input(f"\t{Colors(255,255,255)}{Language[SelectLanguage]['SelectPA']}{ColorsEnd()}"))-1]
        PathB = DataList[int(
            input(f"\t{Colors(255,255,255)}{Language[SelectLanguage]['SelectPB']}{ColorsEnd()}"))-1]
        Look(PathA, PathB, True)
    except KeyboardInterrupt:
        return None
    except IndexError:
        print(
            f"\n{Colors(255,0,0)}======{Language[SelectLanguage]['InputError']}======{ColorsEnd()}\n")
        Function_1()


def Function_3():
    SQLData = ""
    while True:
        Data = input("\tSQL>") + "\n"
        if Data == "^end\n":
            break
        SQLData += Data
    Look(SQLData, SQLData)


def Function_4():
    SQLDataA = ""
    SQLDataB = ""
    print(
        f"\t=================={Language[SelectLanguage]['PartA']}==================")
    while True:
        Data = input(f"\t{Language[SelectLanguage]['PartA']} SQL>") + "\n"
        if Data == "^end\n":
            break
        SQLDataA += Data
    print(
        f"\t=================={Language[SelectLanguage]['PartB']}==================")
    while True:
        Data = input(f"\t{Language[SelectLanguage]['PartB']} SQL>") + "\n"
        if Data == "^end\n":
            break
        SQLDataB += Data
    Look(SQLDataA, SQLDataB)

# ==================================================[Middleware]


def Look(DataA, DataB, Path=False):
    ALLSP = [0, 0, ""]
    inputA = ""
    inputB = ""
    if Path:
        inputA = LoadSQL(DataA)
        inputB = LoadSQL(DataB)
    else:
        inputA = DataA
        inputB = DataB
    try:
        DBList["ADB"]["Cursor"].execute(inputA)
        DBList["BDB"]["Cursor"].execute(inputB)
        title = [[i[0] for i in DBList["ADB"]["Cursor"].description],
                 [i[0] for i in DBList["BDB"]["Cursor"].description]]
        ALLSP = diff(title, DBList["ADB"]["Cursor"].fetchall(),
                     DBList["BDB"]["Cursor"].fetchall(),
                     ALLSP)
    except MySQLdb._exceptions.ProgrammingError as e:
        print(f"\033[91m{Language[SelectLanguage]['ErrorFrom']}{e}\033[0m")
    except MySQLdb._exceptions.OperationalError as e:
        print(
            f"\t{Colors(255,0,0)}{Language[SelectLanguage]['ErrorFrom']}{e}{ColorsEnd()}")
        if int(str(e).split(",")[0][1:]) == 2013:
            print(
                f"\t{Colors(255,0,0)}{Language[SelectLanguage]['ReLinkDB']}{ColorsEnd()}")
            Init()
            print(
                f"\t{Colors(0,255,0)}{Language[SelectLanguage]['LinkOK']}{ColorsEnd()}")
        return
    except KeyError as e:
        print(
            f"\t{Colors(255,0,0)}{Language[SelectLanguage]['NotHasError']}{ColorsEnd()}")
        Init()
        return
    start = " " * ALLSP[0] + f"{Colors(255,255,255)}" + "=" * int((ALLSP[1] - len(Language[SelectLanguage]['Result'])-3) / 2) + \
        f"{ColorsEnd()} {Colors(255,255,0)}{Language[SelectLanguage]['Result']}{ColorsEnd()} {Colors(255,255,255)}" + \
            "=" * int((ALLSP[1] - len(Language[SelectLanguage]
                                      ['Result'])-3) / 2) + f"{ColorsEnd()}\n\n"
    end = "\n" + " " * \
        ALLSP[0] + f"{Colors(255,255,255)}" + "=" * int((ALLSP[1] - len(Language[SelectLanguage]
                                                                        ['Finish'])-3) / 2) + \
        f"{ColorsEnd()} {Colors(255,255,0)}{Language[SelectLanguage]['Finish']}{ColorsEnd()} {Colors(255,255,255)}" + \
        "=" * int((ALLSP[1] - len(Language[SelectLanguage]
                                  ['Finish'])-3) / 2) + f"{ColorsEnd()}"
    print(start+ALLSP[2]+end)


def TextLen(text="", diff=False):
    temp = str(text)
    if len(temp) > 15:
        temp = temp[:15]
    if diff:
        return f"[{temp}]"
    return temp


def DataLen(dataA, dataB, ALLSP, title=0):
    textA, textB = "", ""
    subMaxCount = max(len(dataA), len(dataB))
    for i in range(subMaxCount):
        if len(dataA) <= i:
            textA += f"|{Colors(170,0,0,2,0,200,0)}{TextLen(diff=True):^15}{ColorsEnd()}"
            textB += f"|{Colors(0,220,0,2,200,0,0)}{TextLen(dataB[i],True):^15}{ColorsEnd()}"
        elif len(dataB) <= i:
            textA += f"|{Colors(170,0,0,2,0,200,0)}{TextLen(dataA[i],True):^15}{ColorsEnd()}"
            textB += f"|{Colors(0,220,0,2,200,0,0)}{TextLen(diff=True):^15}{ColorsEnd()}"
        elif str(dataA[i]) != str(dataB[i]):
            textA += f"|{Colors(170,0,0,2,0,200,0)}{TextLen(dataA[i],True):^15}{ColorsEnd()}"
            textB += f"|{Colors(0,220,0,2,200,0,0)}{TextLen(dataB[i],True):^15}{ColorsEnd()}"
        else:
            textA += f"|{Colors(170-title*170,170-title*170,170-title*170,2,85+title*170,45+title*210,130-title*130)}{TextLen(dataA[i]):^15}{ColorsEnd()}"
            textB += f"|{Colors(170-title*170,170-title*170,170-title*170,2,85+title*170,45+title*210,130-title*130)}{TextLen(dataB[i]):^15}{ColorsEnd()}"
    textA += "|"
    textB += "|"
    ASp = "".join([" " for i in range(int((100 - GetStrLen(textA)) / 2))])
    BSp = "".join([" " for i in range(int((100 - GetStrLen(textB)) / 2))])
    alls = ASp + f"{textA}" + ASp + \
        f"{Colors(255,255,0)}|:|{ColorsEnd()}" + BSp + f"{textB}\n"
    ALLSP[0] = max(ALLSP[0], len(ASp))
    ALLSP[1] = max(ALLSP[1], GetStrLen(alls)-len(ASp))
    ALLSP[2] = ALLSP[2] + alls
    if title != 0:
        ALLSP[2] += "\n"
    return ALLSP


def GetStrLen(text):
    return len(re.sub(r"\x1b[^m]*m", "", text))


def Colors(r, g, b, bf=0, br=0, bg=0, bb=0):
    if bf == 0:
        return f"\u001b[38;2;{r};{g};{b}m"
    elif bf == 2:
        return f"\u001b[48;2;{br};{bg};{bb}m\u001b[38;2;{r};{g};{b}m"
    else:
        return f"\u001b[48;2;{r};{g};{b}m"


def ColorsEnd():
    return f"\u001b[0m"


def diff(title, dataA, dataB, ALLSP):
    DataLen(title[0], title[1], ALLSP, 1)
    # ----------------------------------------------------
    maxSPCount = 0
    maxCount = max(len(dataA), len(dataB))
    # ----------------------------------------------------
    for i in range(maxCount):
        textA, textB = "", ""
        if len(dataA) <= i:
            ALLSP = DataLen(list(), dataB[i], ALLSP)
        elif len(dataB) <= i:
            ALLSP = DataLen(dataA[i], list(), ALLSP)
        else:
            ALLSP = DataLen(dataA[i], dataB[i], ALLSP)
    # -------------------------------------------------
    return ALLSP


# ==================================================[System]


def Init():
    global DBList
    temp = DBList
    DataBaseList = None
    if os.path.isfile("./DatabaseServer.json") == False:
        print(
            f"{Colors(255,0,0)}{Language[SelectLanguage]['NoConfig']}{ColorsEnd()}")
        os._exit(0)
    Names = LoadJson()
    DBList = dict()
    count = 0
    while True:
        try:
            select = int(input(
                f"\t{Language[SelectLanguage]['SelectDB']}{[Language[SelectLanguage]['PartA'],Language[SelectLanguage]['PartB']][count%2]}："))
            # --------------------------
            if select == -1:
                DBList = temp
                return "Exit"
            elif select == -2:
                Names = LoadJson()
                continue
            else:
                select -= 1
            # --------------------------
            err = LinkSQL(f"{['A','B'][count%2]}DB",  Names[select]["host"], Names[select]
                          ["user"], Names[select]["paaswd"], Names[select]["db"])
            # --------------------------
            if len(DBList) >= 2:
                return None
            elif err != None:
                continue
            # --------------------------
            count += 1
        except KeyboardInterrupt:
            Names = LoadJson()
            return "Exit"
        except:
            print(f"{Language[SelectLanguage]['SelectError']}")


def LoadJson():
    Names = list()
    DataBaseList = None
    count = 0
    Display(1)
    with open("./DatabaseServer.json", "r", encoding="utf-8") as data:
        try:
            DataBaseList = json.loads(data.read())
        except:
            print(
                f"{Colors(255,0,0)}{Language[SelectLanguage]['ConfigError']}{ColorsEnd()}")
            os._exit(0)
    print(f"\t{Colors(0,255,0)}{'='*150}{ColorsEnd()}")
    for Name, DBData in DataBaseList.items():
        count += 1
        print(
            f"{' '*67}{Colors(255,255,255)}{count} : {Language[SelectLanguage]['DBName']} : {Name}{ColorsEnd()}")
        Names.append(DBData)
    print(f"\t{Colors(0,255,0)}{'='*150}{ColorsEnd()}")
    return Names


def main():
    Display(0)
    if Init() != None:
        return None
    # --------------------------
    while True:
        err = SelectFunc()
        if err == "exit":
            break
        elif err != None:
            print(err)
        Display(0)
    # --------------------------
    Close()


# ==================================================[Language]

def LoadLanguage():
    global Language
    if os.path.isfile("./language.json") == False:
        print(f"{Colors(255,0,0)}The Language Error.{ColorsEnd()}")
        os._exit(0)
    with open("./language.json", "r", encoding="utf-8") as data:
        try:
            Language = json.loads(data.read())
        except:
            print(
                f"{Colors(255,0,0)}The Language Error.{ColorsEnd()}")
            os._exit(0)
    SelectLanguageFunc()


def SelectLanguageFunc():
    global SelectLanguage
    print(f"\t{Colors(255,255,255)}Please Select Language.{ColorsEnd()}\n\t(input '-1' than exit.)")
    while True:
        try:
            count = 0
            SelectName = list()
            for key in Language:
                count += 1
                SelectName.append(key)
                print(f"\t{Colors(255,255,255)}{count} : {key}{ColorsEnd()}")
            temp = int(
                input(f"\t{Colors(255,255,255)}Please Select：{ColorsEnd()}"))
            if temp == -1:
                os._exit(0)
            elif len(Language) < temp:
                print(f"\t{Colors(255,0,0)}Input Error.{ColorsEnd()}")
            else:
                SelectLanguage = SelectName[temp - 1]
                break
        except KeyboardInterrupt:
            os._exit(0)
        except:
            print(f"\t{Colors(255,0,0)}Input Error.{ColorsEnd()}")


def CheckOS():
    if os.name == 'nt':
        os.system("mode con cols=200 lines=1000")
        if os.path.isfile(os.path.join(".", "ansi", "x64", "ansicon.exe")):
            os.system(os.path.join(".","ansi","x64","ansicon.exe -e"))

# ==================================================[Main]


if __name__ == "__main__":
    CheckOS()
    LoadLanguage()
    main()
