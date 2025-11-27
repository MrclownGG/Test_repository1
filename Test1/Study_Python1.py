"""
示例说明：使用 Scrapy 抓取百度首页导航栏并打印到控制台。

运行方式：
    python Study_Python1.py
"""

from scrapy import Spider  # 导入 Scrapy 的 Spider 基类
from scrapy.crawler import CrawlerProcess  # 导入便于在脚本中运行爬虫的工具


class BaiduNavSpider(Spider):
    """定义一个爬虫类，专门抓取 https://www.baidu.com/ 的导航链接。"""

    name = "baidu_nav"  # 爬虫名称，Scrapy 识别用
    start_urls = ["https://www.baidu.com/"]  # 起始请求列表，只包含百度首页

    def parse(self, response):
        """解析响应内容，把导航栏的文本与链接提取出来。"""
        nav_items = response.css("#s-top-left a, #s-top-right a")  # 选中顶部左右导航栏所有链接
        if not nav_items:
            self.logger.warning("页面上没有匹配到导航链接，可能结构变了。")  # 如果没抓到就给出警告
        for link in nav_items:  # 遍历每一个 <a> 标签
            text = link.css("::text").get(default="").strip()  # 把链接文字取出来并去除两端空白
            href = response.urljoin(link.attrib.get("href", ""))  # 将相对地址拼成完整 URL
            if text:  # 只打印有文字的导航项
                print(f"{text}: {href}")  # 输出到控制台


if __name__ == "__main__":
    process = CrawlerProcess(  # 创建 Scrapy 运行器
        {
            "LOG_LEVEL": "INFO",  # 设置日志级别，避免过多调试信息
        }
    )
    process.crawl(BaiduNavSpider)  # 把上面定义的爬虫加入调度
    process.start()  # 启动爬虫并阻塞直到完成

