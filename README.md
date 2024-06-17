# Hanspell (v. 2024)

## 개요

네이버 맞춤법 검사기를 이용한 한글 맞춤법 검사 라이브러리입니다.

[Py-hanspell](https://github.com/ssut/py-hanspell) 소스코드를 바탕으로 만든

[alfhanspell](https://github.com/kw-lee/alfhanspell/blob/main/workflow/hanspell_break.py)의 코드를 발췌하여 수정한 것입니다.

네이버 맞춤법 검사기를 사용하기 위해 필요한 토큰을 매일 갱신해야 되는데, 그 부분을 자동화하였습니다.

코드를 사용하면 자동으로 `token.txt` 파일이 생성되며, 여기에 토큰값과 마지막으로 저장한 날짜가 저장됩니다.

사용 시 날짜가 저장된 날짜와 다르면 토큰값을 자동으로 갱신합니다.


## 사용 방법

```python
from hanspell import get_correction

text = "안녕하십니까? 저는한국사람이에요. 만나서 반갑습 니다!"
print(get_correction(text))
# Output: 안녕하십니까? 저는 한국 사람이에요. 만나서 반갑습니다!
```