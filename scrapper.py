import requests
from bs4 import BeautifulSoup


def search_incruit(keyword, page=1):
    jobs = []

    for i in range(page):
        start_no = 30 * i
        url = f"https://search.incruit.com/list/search.asp?col=job&kw={keyword}&startno={start_no}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        
        lis = soup.find_all("li", class_="c_col")[:30]

        for li in lis:
            company = li.find("a", class_="cpname").text
            title = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").text
            location = li.find("div", class_="cl_md").find_all("span")[0].text
            link = li.find("div", class_="cell_mid").find("div", class_="cl_top").find("a").get("href")

            job_data = {
                "company": company,
                "title": title,
                "location": location,
                "link": link
            }

            jobs.append(job_data)
            
    return jobs


def search_saramin(keyword, page=1):
    jobs = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for i in range(page):
        page_num = i + 1
        url = f"https://www.saramin.co.kr/zf_user/search/recruit?searchword={keyword}&recruitPage={page_num}"
        
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        
        item_recruit = soup.find_all("div", class_="item_recruit")[:30]

        for item in item_recruit:
            company_div = item.find("div", class_="area_corp")
            company = company_div.find("a").text.strip() if company_div else "회사명 없음"
            
            title_div = item.find("h2", class_="job_tit")
            if title_div:
                title_a = title_div.find("a")
                title = title_a.text.strip()
                link = "https://www.saramin.co.kr" + title_a.get("href")
            else:
                continue
            
            conditions_div = item.find("div", class_="job_condition")

            if conditions_div:
                location = conditions_div.find_all("span")[0].text.strip()
            else:
                location = "지역 정보 없음"

            job_data = {
                "company": company,
                "title": title,
                "location": location,
                "link": link
            }
            jobs.append(job_data)
            
    return jobs


if __name__ == '__main__':
    
    incruit_result = search_incruit("간호사", 2)
    saramin_result = search_saramin("간호사", 2)
    
    total_result = incruit_result + saramin_result