# -*- coding: utf-8 -*-
import re
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree


# 定义类
class LagouSpider(object):
    driver_path = r"D:\ProgramData\chromedriver\chromedriver.exe"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        # 绑定url： 'python实习' （上海站）所有招聘信息
        self.url = "https://www.lagou.com/jobs/list_Python%E5%AE%9E%E4%B9%A0?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput="
        self.positions = []  # 存放职位信息

    def run(self):
        # 使用driver请求页面
        self.driver.get(self.url)
        count = 1
        while True:
            print("正在获取第{}的页数据".format(count))
            count += 1
            # 拿列表页数据
            source = self.driver.page_source
            WebDriverWait(driver=self.driver, timeout=10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="pager_container"]/span[last()]'))
                # 元素呈现以后才点击
            )
            # 调用解析页面方法
            self.parse_list_page(source)
            # 点击下一页
            # 找到下一页 使用xpath，div标签下class属性位page_container下的span标签的最后一个 使用last()
            next_btn = self.driver.find_element_by_xpath(
                r'//div[@class="pager_container"]/span[last()]')
            if "pager_next_disabled" in next_btn.get_attribute('class'):
                break
                # 最后一页不点击
            else:
                next_btn.click()  # 点击到下一页
            time.sleep(3)
        self.driver.quit()  # 将浏览器退出
        self.write_to_csv()  # 将获取的数据写入csv文件

    # 定义函数，解析列表页页面
    def parse_list_page(self, source):
        html = etree.HTML(source)
        # 详情页获取 链接在class标签下
        links = html.xpath(r"//a[@class='position_link']/@href")
        # # 找到每一页里面的职位详情页链接
        for link in links:
            self.request_detail_page(link)  # 获取详情页链接成功
            time.sleep(1)  # 沉睡一秒 不要太快

    # 详情页
    def request_detail_page(self, url):
        # self.driver.get(url)
        # 开启新的标签页
        self.driver.execute_script("window.open('%s')" % url)
        # 保留俩个窗口 列表页+详情页
        # 切换到新的标签页
        self.driver.switch_to.window(self.driver.window_handles[1])
        # 添加等待
        WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='name']"))
        )
        source = self.driver.page_source
        self.parse_detail_page(source)
        # 关闭当前详情页 继续切换回列表页
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    # 解析详情页数据
    def parse_detail_page(self, source):
        html = etree.HTML(source)
        position_name = html.xpath("//span[@class='name']/text()")[0]
        # print(position_name)
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath('.//text()')[0].strip()
        # salary = salary_span.xpath('.//text()')[0]
        city = job_request_spans[1].xpath('.//text()')[0].strip()
        city = re.sub(r'[\s/]', '', city)
        work_years = job_request_spans[2].xpath('.//text()')[0].strip()
        work_years = re.sub(r'[\s/]', '', work_years)
        education = job_request_spans[3].xpath('.//text()')[0].strip()
        education = re.sub(r'[\s/]', '', education)

        # 工作地址 待解决
        # work_addr = "".join(html.xpath("//div[@class='address']//a[@rel='nofollow']//text()")).strip()
        address = re.findall(
            r'<input type="hidden" name="positionAddress" value="([^"]*)',
            self.driver.page_source)[0]  # 获取工作地点

        desc = html.xpath("//dd[@class='job_bt']//text()")
        # 打印出来是一个列表 转换成字符串 "".join()
        desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        desc = re.sub(r'[\s\\n]', '', desc)
        # job_desc = html.xpath(
        #     '//div[@class="job-detail"]//p/text()')  # 获取职位描述
        # job_desc = ' '.join(job_desc)  # 另一种职位描述方法
        company_name = html.xpath('//em[@class="fl-cn"]/text()')[0].strip()

        position = {
            '公司名称': company_name,
            '职位': position_name,
            '薪资': salary,
            '城市': city,
            '工作地址': address,
            '经验要求': work_years,
            '学历要求': education,
            '职位描述': desc
        }
        time.sleep(2)  # 沉睡2秒，防止开启太快临时封IP
        self.positions.append(position)
        print(position)
        # print("___" * 20)

    def write_to_csv(self):  # 写入文件
        header = [
            '公司名称',
            '职位',
            '薪资',
            '城市',
            '工作地址',
            '经验要求',
            '学历要求',
            '职位描述'
        ]
        with open('positons1.csv', 'w', newline='', encoding='utf-8') as fp:
            write = csv.DictWriter(fp, header)
            write.writeheader()
            write.writerows(self.positions)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
