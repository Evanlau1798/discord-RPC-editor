from json import load

with open(f'./data/test.json',encoding="UTF-8",mode="r") as json_file:
    data = load(json_file)
    #detail = data["User_stored_stat"]["detail"]



    stat = data["User_stored_stat"]["stat"] 
    if "User_stored_stat" in data and "stat" in data["User_stored_stat"]:
        print(stat)