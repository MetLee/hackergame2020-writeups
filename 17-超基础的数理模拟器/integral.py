import os
import re
from selenium import webdriver

token = 'toooooooooooooooken'


def format_num(s):
    return re.sub(r'\\frac\{([\d|x]*)\}\{([\d|x]*)\}', r'\1/\2', s)


def format_func(s):
    rst = s
    rst = re.sub(r'\\,', r' ', rst)  # 分隔
    rst = re.sub(r'\^\{([\d|x]*)\}', r'^(\1)', rst)  # 幂
    rst = re.sub(r'\\sqrt\{([\d|x]*)\}', r'Sqrt[\1]', rst)  # 开方
    rst = re.sub(r'\\ln\\left\((.*?)\\right\)', r'Log[\1]', rst)  # 对数
    rst = re.sub(r'\\s(inh?)\\left\((.*?)\\right\)',
                 r'S\1(\2)', rst)  # sin sinh
    rst = re.sub(r'\\c(osh?)\\left\((.*?)\\right\)',
                 r'C\1(\2)', rst)  # cos cosh
    rst = re.sub(r'\\tan\\left\((.*?)\\right\)', r'Tan(\1)', rst)  # tan
    rst = re.sub(r'\\arctan\\left\((.*?)\\right\)',
                 r'Arctan(\1)', rst)  # arctan
    rst = re.sub(r'\\frac\{(.*?)\}\{(.*?)\}', r'((\1)/(\2))', rst)  # 分数
    rst = re.sub(r'\\(?:(?:left)|(?:right))', r'', rst)
    rst = re.sub(r'e', r'E', rst)
    return rst


def main():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'javascript': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(f'http://202.38.93.111:10190/login?token={token}')
    countdown = driver.find_element_by_xpath(
        '//h1[@class="cover-heading"]').text
    countdown = re.findall('(\d*)题', countdown)

    while countdown:
        try:
            integral_exp = driver.find_element_by_xpath(
                '//center/p').text
        except:
            break

        try:
            print(integral_exp)
            units = re.findall(
                r'\\int_\{(.*?)\}\^\{(.*?)\}\s(.*?)\\,\{d x\}', integral_exp)[0]  # 注意转义

            interval_l = units[0]
            formatted_interval_l = format_num(interval_l)
            interval_r = units[1]
            formatted_interval_r = format_num(interval_r)

            func = units[2]
            formatted_function = format_func(func)

            formatted_integral_exp = f'NIntegrate[{formatted_function}, {{x, {formatted_interval_l}, {formatted_interval_r}}}]'
            print(formatted_integral_exp)

            output = os.popen(
                f'wolframscript -code "{formatted_integral_exp}"').read()
            # print(output)

            rst = re.findall(r'([\d\-]*\.\d{6})\d*', output)
            if rst:
                rst = rst[0]
                print(rst)
                textbox = driver.find_element_by_xpath('//input[@type="text"]')
                textbox.send_keys(rst)
                button = driver.find_element_by_xpath(
                    '//button[@type="submit"]')
                button.click()
                countdown = driver.find_element_by_xpath(
                    '//h1[@class="cover-heading"]').text
                countdown = re.findall('(\d*)题', countdown)
                continue
            else:
                driver.refresh()
                continue
        except:
            driver.refresh()
            continue

    input()
    driver.quit()


if __name__ == '__main__':
    main()
