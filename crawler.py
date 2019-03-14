import re
import requests
from lxml import html

from request import Request


class _ProxyBase(object):
    def __init__(self):
        self.request = Request()

    def crawl(self):
        pass


class ProxyWuYou(_ProxyBase):
    """
    无忧代理 http://www.data5u.com/
    :return:
    """

    def crawl(self):
        urls = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
        ]
        ip_ports = []
        for url in urls:
            page = self.request.get(url).content
            root = html.fromstring(page)
            uls = root.xpath('//ul[@class="l2"]')
            for ul in uls:
                ip_port = ':'.join(ul.xpath('.//li/text()')[0:2])
                ip_ports.append(ip_port)
        return ip_ports


class ProxyDaiLi66(_ProxyBase):
    """
    代理66 http://www.66ip.cn/
    :return:
    """

    def crawl(self):
        urls = [
            "http://www.66ip.cn/mo.php?sxb=&tqsl={count}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=",
            "http://www.66ip.cn/nmtq.php?getnum={count}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip",
        ]
        ip_ports = []
        count = 20
        for _ in urls:
            url = _.format(count=count)
            page = self.request.get(url).content
            ips = re.findall(br"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", page)
            for ip in ips:
                ip_ports.append(ip.decode().strip())
        return ip_ports


class ProxyXiCi(_ProxyBase):
    """
    西刺代理 http://www.xicidaili.com
    :return:
    """

    def crawl(self):
        urls = [
            'http://www.xicidaili.com/nn/',  # 高匿
            'http://www.xicidaili.com/nt/',  # 透明
        ]
        ip_ports = []
        page = 1
        for url in urls:
            for i in range(1, page + 1):
                url = url + str(i)
                content = self.request.get(url).content
                root = html.fromstring(content)
                proxy_list = root.xpath('.//table[@id="ip_list"]//tr[position()>1]')
                for proxy in proxy_list:
                    try:
                        ip_port = ':'.join(proxy.xpath('./td/text()')[0:2])
                        ip_ports.append(ip_port)
                    except Exception as e:
                        pass
        return ip_ports


class ProxyGuoBanJia(_ProxyBase):
    """
    guobanjia http://www.goubanjia.com/
    :return:
    """

    def crawl(self):
        url = "http://www.goubanjia.com/"
        page = self.request.get(url).content
        root = html.fromstring(page)
        proxy_list = root.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        ip_ports = []
        for proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip = ''.join(proxy.xpath(xpath_str))
                port = proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                ip_port = '{}:{}'.format(ip, port)
                ip_ports.append(ip_port)
            except Exception as e:
                pass
        return ip_ports


class ProxyKuaiDaiLi(_ProxyBase):
    """
    快代理 https://www.kuaidaili.com
    :return:
    """

    def crawl(self):
        urls = [
            'https://www.kuaidaili.com/free/inha/',
            'https://www.kuaidaili.com/free/intr/',
        ]
        ip_ports = []
        for url in urls:
            page = self.request.get(url).content
            root = html.fromstring(page)
            proxy_list = root.xpath('.//table//tr')
            for tr in proxy_list[1:]:
                ip_port = ':'.join(tr.xpath('./td/text()')[0:2])
                ip_ports.append(ip_port)
        return ip_ports


class ProxyYunDaiLi(_ProxyBase):
    """
    云代理 http://www.ip3366.net/free/
    :return:
    """

    def crawl(self):
        url = 'http://www.ip3366.net/free/'
        r = self.request.get(url)
        proxys = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
        ip_ports = []
        for proxy in proxys:
            ip_port = ":".join(proxy)
            ip_ports.append(ip_port)
        return ip_ports


class ProxyIPHai(_ProxyBase):
    """
    IP海 http://www.iphai.com/free/ng
    :return:
    """

    def crawl(self):
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp',
        ]
        ip_ports = []
        for url in urls:
            r = self.request.get(url)
            proxys = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                r.text)
            for proxy in proxys:
                ip_port = ":".join(proxy)
                ip_ports.append(ip_port)
        return ip_ports


class ProxyMianFeiDaiLi(_ProxyBase):
    """
    http://ip.jiangxianli.com/?page=
    免费代理库
    超多量
    :return:
    """

    def crawl(self):
        page = 2
        ip_ports = []
        for i in range(1, page + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            page = self.request.get(url).content
            root = html.fromstring(page)
            tr_list = root.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            for tr in tr_list:
                ip_port = tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]
                ip_ports.append(ip_port)
        return ip_ports


class ProxyChinaIP(_ProxyBase):
    """
    墙外网站 cn-proxy
    :return:
    """

    def crawl(self):
        urls = [
            'http://cn-proxy.com/',
            'http://cn-proxy.com/archives/218',
        ]
        ip_ports = []
        for url in urls:
            r = self.request.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                ip_port = ':'.join(proxy)
                ip_ports.append(ip_port)
        return ip_ports


def main():
    proxys = [
        # ProxyDaiLi66,
        # ProxyGuoBanJia,
        # ProxyIPHai,
        # ProxyKuaiDaiLi,
        # ProxyMianFeiDaiLi,
        ProxyWuYou,
        ProxyXiCi,
        ProxyYunDaiLi,
        # ProxyChinaIP,
    ]
    for Proxy in proxys:
        p = Proxy()
        ip_ports = p.crawl()
        print(ip_ports)


if __name__ == '__main__':
    main()
