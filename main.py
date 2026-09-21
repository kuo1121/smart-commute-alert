import os
import requests


TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def get_weather_and_aqi():
  try:
   
    data = {"max_temp": 34.0, "rain_prob": 70, "aqi": 105}
    return data
  except Exception as e:
    print(f"API 取得失敗: {e}")
    return None


def generate_alerts(data):
  if not data:
    return "無法取得今日的氣象與空氣品質資料，請檢查 API 狀態。"

  max_temp = data.get("max_temp", 0)
  rain_prob = data.get("rain_prob", 0)
  aqi = data.get("aqi", 0)

  alerts = []

 
  if rain_prob >= 60:
    alerts.append("☔ 降雨機率達 60% 以上，出門請記得攜帶雨傘！")

  if max_temp >= 33:
    alerts.append(f"☀️ 今日最高溫達 {max_temp}°C，請注意防曬並隨時補充水分！")

  if aqi >= 100:
    alerts.append(f"😷 空氣品質 AQI 達 {aqi}，建議外出配戴口罩！")

  if not alerts:
    alerts.append("✨ 今日天氣與空氣品質皆良好，非常適合外出通勤！")

  message = "📊 【智慧通勤風險通知】\n" + "\n".join(alerts)
  return message


def send_telegram_message(message):
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("錯誤：未設定 Telegram Bot Token 或 Chat ID")
    return

  url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
  payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

  try:
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code == 200:
      print("Telegram 訊息發送成功！")
    else:
      print(f"Telegram 發送失敗，HTTP 狀態碼: {response.status_code}")
  except Exception as e:
    print(f"發送請求時發生錯誤: {e}")


if __name__ == "__main__":
  data = get_weather_and_aqi()
  message = generate_alerts(data)
  print(message)
  send_telegram_message(message)
