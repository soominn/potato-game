# 🥔 감자 게임 (Potato Game)

## 🎮 게임 소개

**감자 피하기**
- 떨어지는 감자를 피해서 최대한 오래 살아남는 게임
- 생존 시간과 피한 감자 개수 표시
- 감자에 닿으면 게임 오버
- 10초마다 레벨이 오르며 점점 더 어려워짐

**감자 받기**
- 떨어지는 감자를 받아 점수를 얻는 게임
- 3개의 목숨이 있으며, 놓친 감자가 3개가 되면 게임 오버
- 받은 개수, 놓친 개수, 플레이 시간 표시
- 10초마다 레벨이 오르며 점점 더 어려워짐

---

## 🕹 조작 방법

| 키 | 기능 |
|----|------|
| ← / → | 이동 |
| ESC | 메뉴로 돌아가기 |
| R | 게임 오버 시 재시작 |

---

## ⚙️ 실행 방법

### 💻 필수 조건
- **Python 3.10 이상**이 설치되어 있어야 합니다.
- 터미널(또는 명령 프롬프트)에서 아래 명령어를 순서대로 입력하세요.

### 📦 1) 의존성 설치
```bash
pip install -r requirements.txt
```

### ▶️ 2) 실행
```bash
python main.py
```

---

## 📁 폴더 구조
```
PotatoGame/
├── main.py
├── scenes/
│   ├── menu.py
│   ├── dodge.py
│   └── catch.py
├── images/
│   ├── background.png
│   ├── bucket.png
│   ├── player.png
│   ├── potato.png
│   └── poisonous_potato.png
├── fonts/
│   └── PretendardVariable.ttf
├── requirements.txt
└── README.md
```

---

## 🧱 기술 스택
- Python 3.10+
- Pygame 2.6.1
- 객체지향(OOP) 구조 설계
- 이미지 및 폰트 자산 활용

---

## 🧑‍💻 제작자
- 이름: 조수민
- GitHub: [github.com/soominn](https://github.com/soominn)
- 제출일: 2025년 11월
