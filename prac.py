import random

# groups = ["에스파", "하트2하트", "리센느", "태연", "엔믹스"]

# my_group = random.choice(groups)
# print(my_group)

# def get_random_group():
#     groups = [
#         {
#             "이름" : "에스파",
#             "리더" : "카리나"
#         },
#         {
#             "이름" : "엔믹스",
#             "리더" : "해원"
#         },
#         {
#             "이름" : "리센느",
#             "리더" : "원이"
#         }
#     ]
#     my_group = random.choice(groups)

#     return my_group.get("이름"), my_group.get("리더")

# group_name, group_leader = get_random_group()
# print(f"그룹 이름: {group_name}, 리더: {group_leader}")


def get_random_destination():
    destinations = [
        {"나라": "프랑스", "수도": "파리"},
        {"나라": "잉글랜드", "수도": "런던"},
        {"나라": "이탈리아", "수도": "로마"},
        {"나라": "스페인", "수도": "마드리드"},
        {"나라": "호주", "수도": "캔버라"},
        {"나라": "독일", "수도": "베를린"},
    ]
    destination = random.choice(destinations)

    return destination.get("나라"), destination.get("수도")


country, capital = get_random_destination()
print(f"환영합니다! {country} 나라의 수도 {capital} 입니다!")
