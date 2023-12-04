from ..robot.Follow_Bot import Follow_Bot

if __name__ == '__main__':
    bot = Follow_Bot()
    try:
        bot.set_v(255, 255)
        while 1:
            print('RUN')
    except:
        bot.stop()
        bot.close()
        
