import json
import os
import dns.resolver
from datetime import datetime, timedelta, timezone
# 引入多线程查询
from concurrent.futures import ThreadPoolExecutor


# 更新时间修订北京时间
def get_bj_time_str():
    utc_dt = datetime.now(timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    str_date = bj_dt.strftime("%Y-%m-%d %H:%M:%S")
    return str_date


def write_to_file(contents, filename):
    with open(filename, 'w') as file:
        file.write(contents)
    print(f"{filename}文件写入成功")


def dns_lookup(domain):
    try:
        answers = dns.resolver.resolve(domain, "A")
        # 返回所有查询结果的地址列表
        return [str(answer) for answer in answers]
        # # 返回第一个查询结果的地址
        # return str(answers[0])
    except Exception as e:
        print(f"{domain}解析DNS出错：")
        print(e)
        # 如果查询失败，返回空列表
        return []


def load_domain_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("文件 domain.json 不存在")
        return {}
    except json.JSONDecodeError:
        print("文件 domain.json 格式错误")
        return {}


# 主程序
def main(filename):
    # 从domain.json文件中读取域名数据
    domain_data = load_domain_data(filename)

    # 存储解析后的域名和IP
    resolved_domains = {}

    # 使用线程池来并行执行DNS解析
    with ThreadPoolExecutor(max_workers=10) as executor:  # 你可以根据需要调整线程池大小
        for key, domains in domain_data.items():
            """
            # 遍历domain_data字典中所有域名
            # 对每个域名，异步执行dns_lookup函数，并将其添加到字典中，
            # 字典的键是域名，值是对应的异步任务
            """
            future_to_domain = {domain: executor.submit(dns_lookup, domain) for domain in domains}
            """
            /**
             * 根据提供的future对象映射，生成一个包含解析后的IP地址列表或错误标记的字典。
             * 
             * 该函数遍历`future_to_domain`字典中的每一个项，对于每一个future对象，
             * 如果该future对象没有异常（即`dns_lookup`返回非空列表），则将其解析的结果（IP地址列表）与对应的domain组成键值对加入到新的字典中。
             * 如果future对象存在异常（`dns_lookup`返回空列表）或查询失败，则将其value设置为"#"来标记错误。
             * 
             * @param future_to_domain 一个映射，其中键是域名，值是对应域名的Future对象，这些Future对象来自异步执行的`dns_lookup`函数。
             * @return 一个字典，键为域名，值为解析后的IP地址列表（如果查询成功）或错误标记"#"（如果查询失败）。
             */
            """
            resolved_ips = {domain: future.result() if future.result() else "#"
                            for domain, future in future_to_domain.items()}
            resolved_domains[key] = resolved_ips

    update_time = get_bj_time_str()
    key_content = {}
    hosts_content = ""

    for key, domains_ips in resolved_domains.items():
        hosts_content += f"# {key} Hosts Start\n"
        content = f"# {key} Hosts Start\n"
        # 处理每个域名进行dnslookup查询时可能返回的多个 IP 地址
        for domain, ips in domains_ips.items():
            for ip in ips:
                if ip:  # 确保IP地址不为空
                    content += f"{ip}\t\t{domain}\n"
                    # 同时构建hosts.txt的内容
                    hosts_content += f"{ip}\t\t{domain}\n"

        content += f"# Update Time: {str(update_time)} (UTC+8) \n"
        content += f"# Update URL: https://raw.githubusercontent.com/oopsunix/hosts/main/host_{key.lower()}\n"
        content += f"# {key} Hosts End"

        # 将准备好的内容保存到key_file_contents字典中
        key_content[key] = content

        # 在hosts.txt内容中添加分隔标记
        hosts_content += f"# {key} Hosts End\n\n"
        # hosts_content += content

    # 写入每个键对应的文件
    for key, contents in key_content.items():
        write_to_file(contents, f'hosts_{key.lower()}')

    hosts_content += f"# Update Time: {str(update_time)} (UTC+8) \n"
    hosts_content += f"# Update URL: https://raw.githubusercontent.com/oopsunix/hosts/main/hosts\n"
    write_to_file(hosts_content, 'hosts')  # 写入hosts.txt

    print("Update Hosts Success")


if __name__ == '__main__':
    # 获取当前路径目录
    execPath = os.getcwd()
    domainFile = execPath + "/domain.json"

    main(domainFile)
