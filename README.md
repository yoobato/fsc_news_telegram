# FSC News Telegram
금융위원회 보도자료에 특정 단어가 포함된 새 글이 게시된 경우 텔레그램으로 알림 전송

## 실행환경
- Python 3.10.x >=

## 실행방법

### 1. `.env` 파일 작성
```sh
$ cp .env.example .env

# 아래 필드 값 입력
# TELEGRAM_TOKEN : 텔레그램 봇 토큰 (맨 앞의 bot 은 빼고 입력)
# TELETRAM_CHAT_ID : 텔레그램 봇 채팅 ID
# FSC_SEARCH_TEXT : 모니터링할 단어
```
> `TELETRAM_CHAT_ID` 값은 `https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates` 을 통해서 가지고 올 수 있음. (https://core.telegram.org/bots/tutorial 참고)

### 2. 라이브러리 설치
```sh
$ pip install -r requirements.txt
```

### 3. 스크립트 실행
```sh
$ python alarm.py
