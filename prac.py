location_dict = {
    "시": [
        {"이름": "서울특별시", "기초단체": ["중구", "종로구", "마포구"]},
        {"이름": "부산광역시", "기초단체": ["해운대구", "사상구", "남구"]},
    ],
    "도": [
        {"이름": "경기도", "기초단체": ["수원시", "성남시", "용인시"]},
        {"이름": "경상북도", "기초단체": ["포항시", "경주시", "안동시"]},
    ],
}

for basic_dict in location_dict["시"]:
    print(basic_dict.get("이름"))
    print(basic_dict.get("기초단체"))
    print("---------")

for basic_dict in location_dict.get("도"):
    print(basic_dict.get("이름"))
    print(basic_dict.get("기초단체"))
    print("---------")
