# 抓取网页表格中的特定数据

使用bs4中的BeautifulSoup来解析网页，定位table标签，将table的子节点tr写入到csv中，循环读取子节点tr的下一级节点td，并将表格内容写入csv中（会自动按照网页格式），
判断定位关键词，并返回关键词，之后根据关键词读取一列数据，然后根据要取词的所在行进行取值。
