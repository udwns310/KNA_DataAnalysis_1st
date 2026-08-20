import os
import pandas as pd

inj = pd.read_csv('data/15_01_사출성형_공정.csv', encoding='utf-8')

# 실습 7. 결측 확인 요약표

counts = inj.isna().sum()
ratio = (counts / len(inj) * 100).round(1)
table = pd.DataFrame({'결측수': counts, '비율(%)': ratio})
table = table[table['결측수'] > 0].sort_values('결측수', ascending=False)


def decide_direction(pct):
    if pct < 5:
        return '대체로 살리기'
    if pct < 40:
        return '중요도 보고 결정'
    return '제거 고민'


table['처리방향'] = table['비율(%)'].apply(decide_direction)
print(table)

report_path = 'data/15_missing_summary_temp.csv'
table.to_csv(report_path, encoding='utf-8-sig')
print(os.path.exists(report_path))
os.remove(report_path)
