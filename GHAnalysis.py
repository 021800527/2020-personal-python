import json
import os
import argparse


def initialization(path):
    json_list = []
    dict_address = path
    user_4event_num = {}
    repo_4event_num = {}
    user_repo_4event_num = {}
    for root, dic, files in os.walk(dict_address):
        for f in files:
            if f[-5:] == '.json' and f[-6] != '0' and f[-6] != '1' and f[-6] != '2':
                json_path = f
                x = open(dict_address+'\\'+json_path, 'r', encoding='utf-8').read()
                str_list = [_x for _x in x.split('\n') if len(_x) > 0]
                for i, _str in enumerate(str_list):
                    # 个人用户的四个事件
                    json_list.append(json.loads(_str))
                    str_key = json_list[i]['actor']['login']
                    # 初始化 如果非空就继续往下
                    if user_4event_num.get(str_key) is None:
                        user_4event_num[str_key] = {}
                    # 初始化 不存在就创建，存在在后面处理
                    if user_4event_num[str_key].get('IssuesEvent') is None:
                        user_4event_num[str_key].update({'IssuesEvent': 0})
                    if user_4event_num[str_key].get('PushEvent') is None:
                        user_4event_num[str_key].update({'PushEvent': 0})
                    if user_4event_num[str_key].get('IssueCommentEvent') is None:
                        user_4event_num[str_key].update({'IssueCommentEvent': 0})
                    if user_4event_num[str_key].get('PullRequestEvent') is None:
                        user_4event_num[str_key].update({'PullRequestEvent': 0})
                    if json_list[i]['type'] in user_4event_num[str_key].keys():
                        user_4event_num[str_key][json_list[i]['type']] = user_4event_num[str_key][json_list[i]['type']] + 1
                    # 项目的四种事件
                    str_key = json_list[i]['repo']['name']
                    # 初始化 如果非空就继续往下
                    if repo_4event_num.get(str_key) is None:
                        repo_4event_num[str_key] = {}
                    # 初始化 不存在就创建，存在在后面处理
                    if repo_4event_num[str_key].get('IssuesEvent') is None:
                        repo_4event_num[str_key].update({'IssuesEvent': 0})
                    if repo_4event_num[str_key].get('PushEvent') is None:
                        repo_4event_num[str_key].update({'PushEvent': 0})
                    if repo_4event_num[str_key].get('IssueCommentEvent') is None:
                        repo_4event_num[str_key].update({'IssueCommentEvent': 0})
                    if repo_4event_num[str_key].get('PullRequestEvent') is None:
                        repo_4event_num[str_key].update({'PullRequestEvent': 0})
                    if json_list[i]['type'] in repo_4event_num[str_key].keys():
                        repo_4event_num[str_key][json_list[i]['type']] = repo_4event_num[str_key][json_list[i]['type']] + 1
                    # 每一个人在每一个项目的 4 种事件的数量
                    new_str_key = json_list[i]['repo']['name']
                    str_key = json_list[i]['actor']['login']
                    # 初始化 如果非空就继续往下
                    if user_repo_4event_num.get(str_key) is None:
                        user_repo_4event_num[str_key] = {}
                        # 套娃第二步，先把项目名放进去
                    if user_repo_4event_num[str_key].get(new_str_key) is None:
                        user_repo_4event_num[str_key][new_str_key] = {}
                    if user_repo_4event_num[str_key][new_str_key].get('IssuesEvent') is None:
                        user_repo_4event_num[str_key][new_str_key].update({'IssuesEvent': 0})
                    if user_repo_4event_num[str_key][new_str_key].get('PushEvent') is None:
                        user_repo_4event_num[str_key][new_str_key].update({'PushEvent': 0})
                    if user_repo_4event_num[str_key][new_str_key].get('IssueCommentEvent') is None:
                        user_repo_4event_num[str_key][new_str_key].update({'IssueCommentEvent': 0})
                    if user_repo_4event_num[str_key][new_str_key].get('PullRequestEvent') is None:
                        user_repo_4event_num[str_key][new_str_key].update({'PullRequestEvent': 0})
                    if json_list[i]['type'] in user_repo_4event_num[str_key][new_str_key].keys():
                        user_repo_4event_num[str_key][new_str_key][json_list[i]['type']] = user_repo_4event_num[str_key][new_str_key][json_list[i]['type']] + 1
    with open('0.json', 'w', encoding='utf-8') as f:
        json.dump(user_4event_num, f)
    with open('1.json', 'w', encoding='utf-8') as f:
        json.dump(repo_4event_num, f)
    with open('2.json', 'w', encoding='utf-8') as f:
        json.dump(user_repo_4event_num, f)


def inquire_user_event(user, event):
    with open('0.json', 'r',encoding='utf-8') as f:
        dict1 = json.load(f)
        print(dict1.get(user).get(event))


def inquire_repo_event(repo, event):
    with open('1.json', 'r',encoding='utf-8') as f:
        dict1 = json.load(f)
        print(dict1.get(repo).get(event))


def inquire_user_repo_event(user, repo, event):
    with open('2.json', 'r',encoding='utf-8') as f:
        dict1 = json.load(f)
        print(dict1.get(user).get(repo).get(event))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user")
    parser.add_argument("-e", "--event")
    parser.add_argument("-i", "--address")
    parser.add_argument("-r", "--repo")
    args = parser.parse_args()
    if args.address is not None:
        initialization(args.address)
        if args.address is None and not os.path.exists('1.json') and not os.path.exists('2.json') and not os.path.exists('3.json'):
            print("初始化失败,本地文件不可写入")
        else:
            print("初始化成功")
    if args.user is not None and args.event is not None and args.repo is None:
        inquire_user_event(args.user,args.event)
    if args.repo is not None and args.event is not None and args.user is None:
        inquire_repo_event(args.repo, args.event)
    if args.user is not None and args.repo is not None and args.event is not None:
        inquire_user_repo_event(args.user, args.repo, args.event)