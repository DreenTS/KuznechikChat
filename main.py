from app.chat_app import KuznechikChatApp
import sys


if __name__ == '__main__':
    app = KuznechikChatApp(sys.argv)
    sys.exit(app.exec_())
