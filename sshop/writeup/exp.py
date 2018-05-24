import re
import sys

# host 被攻击机器的ip
# port 题目端口
def exp(host, port):

    attack = to_do_something() # 真实的exp攻击 To do..

    if attack:
        return True # exp攻击成功, 说明patch失败
    else:
        return False # exp攻击失败, 说明patch成功


if __name__ == '__main__':
    '''
    if len(sys.argv) != 4:
        print("Wrong Params")
        print("example: python %s %s %s" % (sys.argv[0], '127.0.0.1', '8233'))
        exit(0)
    ip = sys.argv[1]
    port = sys.argv[2]
    exp(ip, port)
    '''
    exp("localhost", 8233)
