import requests as r
import re


def main():
    url = 'http://202.38.93.111:10001/'
    payload = {'q1': 0, 'q2': 256, 'q3': 9, 'q4': 9, 'q5': 17098}
    headers = {'Cookie': 'cooooooookie'}

    for i in range(1, 24):
        payload['q1'] = i
        _ = r.post(url=url, data=payload, headers=headers).text

        try:
            rst = re.findall(
                r'<div class="alert alert-secondary" role="alert">((?:.|\n)*?)</div>', _)[0]
        except IndexError:
            print(re.findall(r'(flag{.*?})', _)[0])


if __name__ == '__main__':
    main()
