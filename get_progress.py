import json
import os
import requests as r

headers = {
    'origin': 'https://hack.lug.ustc.edu.cn',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'referer': 'https://hack.lug.ustc.edu.cn/board/',
    'cookie': 'coooooooooookie',
    'x-csrftoken': 'csrfffffffffffffff'
}

url = 'https://hack.lug.ustc.edu.cn/admin/submission/'


def get_progress(user_id):
    user_id = int(user_id)
    data = f'{{"method":"get_user_progress","args":{{"user":{user_id}}}}}'
    _ = r.post(url, data=data, headers=headers).text
    return json.loads(_)


def main():
    if os.path.exists('users+progress.json'):
        with open('users+progress.json', 'r') as f:
            progresses = json.load(f)  # 断点续传（
    else:
        with open('users.json', 'r') as f:
            progresses = json.load(f)

    try:
        for user_id in progresses.keys():
            print(user_id)
            if 'progress' in progresses[user_id]:
                continue
            else:
                progress = get_progress(user_id)
                print(progress)
                progresses[user_id]['progress'] = progress

    except Exception as e:
        print(e)

    finally:
        with open('users+progress.json', 'w') as f:
            json.dump(progresses, f, indent=4)


if __name__ == '__main__':
    main()
