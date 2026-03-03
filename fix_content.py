from bs4 import BeautifulSoup

HTML_FILE = 'ai_dashboard.html'

updates = {
    "claude 办公大进化": {
        "detail": "Anthropic 推出的 Claude for Work 升级版，核心在于打通了办公软件的壁垒。Claude 现在不仅能读取 Excel 中的复杂数据，还能直接理解其结构并生成分析图表，更进一步，它可以将这些分析结果直接转化为 PowerPoint 幻灯片。这意味着用户可以给出一个指令：“分析 Q4 销售数据并生成汇报 PPT”，Claude 就能自动完成从数据处理到演示文稿制作的全流程。这标志着 AI 从单纯的文本生成迈向了跨应用的工作流自动化。",
        "takeaway": "办公自动化的最后一公里被打通。Claude 不再只是聊天机器人，而是成为了能操作 Office 套件的“数字员工”。这对于企业效率提升是指数级的，同时也给微软 Copilot 带来了巨大的竞争压力。"
    },
    "OpenAI 语音 API 大进化": {
        "detail": "OpenAI 发布的 Realtime API 更新（gpt-4o-realtime-preview）带来了显著的性能提升。首先是“数字与专有名词”的识别准确率大幅提高，解决了以往 AI 听不懂人名、地名或复杂数字代码的痛点。其次，响应延迟降低了 40%，使得语音交互更加自然流畅，几乎感觉不到停顿。这对于构建语音客服、实时翻译设备以及车载语音助手等应用场景至关重要。此外，成本也得到了进一步优化，降低了开发者的接入门槛。",
        "takeaway": "语音交互的“iPhone 时刻”正在逼近。更低延迟、更高准确率意味着 AI 语音不再是“玩具”，而是可以真正用于商业级实时服务。这将加速 AI 在客服、教育和硬件终端上的落地。"
    },
    "Claude Code“远程控制”": {
        "detail": "Anthropic 为 Claude Code 引入了革命性的“远程控制”能力。开发者现在可以通过手机端的 Claude 应用，直接连接并控制远程的开发环境或电脑终端。不仅可以查看代码、运行脚本，甚至可以进行复杂的服务器维护操作。这种“口袋里的运维中心”极大地解放了开发者的物理限制，使得随时随地处理紧急 bug 或部署代码成为可能。同时，Anthropic 强调了该功能的安全机制，确保远程访问的合规性。",
        "takeaway": "移动办公的边界被重新定义。对于开发者而言，手机不再只是通讯工具，而是变成了生产力终端。这也展示了 Anthropic 在“Agent（智能体）”方向上的野心——让 AI 真正掌握操作系统的控制权。"
    },
    "3800 亿估值！Anthropic 再拿巨额融资": {
        "detail": "就在 OpenAI 融资传闻不断的关口，Anthropic 再次完成了一轮巨额融资，估值飙升至 3800 亿美元。这轮融资由亚马逊领投，谷歌跟投，显示出科技巨头们在“非 OpenAI 阵营”的重注。资金将主要用于下一代模型 Claude 5 的训练集群建设。分析认为，Anthropic 的稳健作风和在企业级市场的差异化竞争策略（如 Artifacts, Computer Use）是其获得资本青睐的关键。",
        "takeaway": "资本市场的双寡头格局已定。Anthropic 已坐稳了“第二极”的位置，不仅有钱，更有巨头的算力支持。对于创业公司而言，通用大模型的入场券已彻底售罄，应用层才是唯一出路。"
    },
    "春节 AI 大战，千问赢麻了": {
        "detail": "2026 年春节成为了 AI 应用的“练兵场”。极客公园复盘发现，阿里通义千问凭借“30亿免单”和“全家桶”生态联动，成为了最大赢家。日活用户数在假期期间翻了三倍，成功下沉到了三四线城市。相比之下，字节豆包虽然也有春晚曝光，但在转化留存上略逊一筹。文章指出，阿里的成功在于将 AI 隐形于生活服务（买票、点餐）之中，而不是让用户为了聊 AI 而聊 AI。",
        "takeaway": "AI 祛魅，场景为王。通义千问的胜利证明了，用户不在乎模型参数有多少，只在乎能领多少红包、能省多少事。AI 正在从“黑科技”回归到“工具”本质，谁能解决实际问题，谁就能留住用户。"
    }
}

def fix_content():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Find the latest week row
    week_row = soup.find('div', class_='week-row')
    if not week_row:
        print("Week row not found")
        return

    news_items = week_row.find_all('div', class_='news-item')
    count = 0
    
    for item in news_items:
        title_div = item.find('div', class_='news-title')
        if not title_div: continue
        
        title_text = title_div.get_text()
        
        matched_key = None
        for key in updates:
            if key in title_text:
                matched_key = key
                break
        
        if matched_key:
            print(f"Updating: {matched_key}")
            content_data = updates[matched_key]
            
            details_container = item.find('details', class_='details-container')
            if details_container:
                details_content = details_container.find('div', class_='details-content')
                if details_content:
                    # Clear existing content
                    details_content.clear()
                    
                    # Add new detail paragraph
                    p = soup.new_tag('p')
                    p.string = content_data['detail']
                    details_content.append(p)
                    
                    # Add takeaway box
                    takeaway_box = soup.new_tag('div', attrs={'class': 'takeaway-box'})
                    t_title = soup.new_tag('span', attrs={'class': 'takeaway-title'})
                    t_title.string = "Takeaway"
                    takeaway_box.append(t_title)
                    
                    # Add takeaway text (as text node)
                    takeaway_box.append(" " + content_data['takeaway'])
                    
                    details_content.append(takeaway_box)
                    count += 1

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"Updated {count} items.")

if __name__ == "__main__":
    fix_content()
