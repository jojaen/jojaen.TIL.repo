	#참고:https://velog.io/@kxxmz312/Telegram-bot-%EB%B4%87-%EB%A7%8C%EB%93%A4%EA%B8%B0-with-%ED%8C%8C%EC%9D%B4%EC%8D%AC
    
    #텔레그램 봇 설정
    #bot_token = ""  # 본인의 봇 토큰으로 변경
    #chat_id = ""  # 본인의 채팅 ID로 변경, 1:1 채팅일 때는 해당 id를 사용하지만 단톡일 때는 id가 달라 변경해야 한다.

    #코인니스에서 요소를 찾아봐도 먹히지 않아 https://www.tokenpost.kr/search?v=gmt 사이트가 코인니스와 실시간으로 연동이 되어 해당 사이트의 요소를 사용하니 구현 성공함.
    
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

async def get_coinness_alerts():
    # 코인니스 사이트에서 알람 가져오기
    url = "https://www.tokenpost.kr/coinness"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 알람 요소, 선택 요소를 선택하는 CSS 선택자를 찾습니다. 일반적으로 오른쪽 클릭 후 "Copy" 메뉴에서 "Copy selector"를 선택하면 해당 요소의 CSS 선택자를 클립보드에 복사할 수 있습니다.
    alert1 = soup.select_one('#main_list_wrap > div > div > div.list_left_item > div:nth-child(1) > div.list_item_content > div.list_item_text > div > a')
    alert2 = soup.select_one('#main_list_wrap > div > div > div.list_left_item > div:nth-child(1) > div.list_item_content > div.list_item_text > a > p')

    # 알람 텍스트 추출
    alert1_text = alert1.text.strip() if alert1 else "No title found"
    alert2_text = alert2.text.strip() if alert2 else "No content found"

    # 하나의 문자열로 합치기
    combined_alert = f"Title: {alert1_text}\n\nContent: {alert2_text}"

    return combined_alert

async def send_telegram_alert(bot_token, chat_id, message):
    try:
        # 텔레그램 봇을 통해 메시지 보내기
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print("Telegram 메시지 전송 중 오류 발생:", e)

async def main():
    # 텔레그램 봇 설정
    bot_token = ""  # 본인의 봇 토큰으로 변경
    chat_id = ""  # 본인의 채팅 ID로 변경
    
    previous_alert = None
    
    while True:
        # 코인니스 사이트에서 새로운 알람 가져오기
        new_alert = await get_coinness_alerts()
        
        # 이전 알람과 비교하여 변경된 경우에만 메시지 전송
        if new_alert != previous_alert:
            await send_telegram_alert(bot_token, chat_id, new_alert)
            previous_alert = new_alert
        
        # 3초마다 사이트 확인
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())
