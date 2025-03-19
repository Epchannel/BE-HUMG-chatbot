import requests
from bs4 import BeautifulSoup
import re
import csv
import os

def crawl_humg_faculties():
    # URL of the faculties page
    base_url = "https://humg.edu.vn"
    faculties_url = f"{base_url}/gioi-thieu/co-cau-to-chuc/cac-khoa/Pages/Default.aspx"
    
    # Send HTTP request to the faculties page
    response = requests.get(faculties_url)          
    if response.status_code != 200:
        print(f"Failed to fetch the faculties page. Status code: {response.status_code}")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all faculty links in the table
    faculty_links = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href and '/gioi-thieu/co-cau-to-chuc/cac-khoa/Pages/' in href and 'Default.aspx' not in href:
            faculty_links.append(href)
    
    # Remove duplicates while preserving order
    faculty_links = list(dict.fromkeys(faculty_links))
    
    # Prepare data for CSV
    faculty_data = []
    
    # Visit each faculty page to extract information
    for link in faculty_links:
        full_url = base_url + link if link.startswith('/') else link
        faculty_info = extract_faculty_info(full_url)
        if faculty_info:
            faculty_data.append(faculty_info)
    
    # Save data to CSV
    save_to_csv(faculty_data)
    
    print(f"Successfully crawled information for {len(faculty_data)} faculties.")

def extract_faculty_info(url):
    try:
        print(f"Crawling: {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
        
        faculty_name_from_url = url.split('/')[-1].replace('.aspx', '')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract faculty name
        faculty_name = ""
        title_element = soup.find('h1', class_='ms-rteElement-H1')
        if title_element:
            faculty_name = title_element.text.strip()
        else:
            # Thử tìm tiêu đề theo cách khác
            title_element = soup.find('div', class_='article-title')
            if title_element:
                faculty_name = title_element.text.strip()
            else:
                # Thử tìm tiêu đề từ breadcrumb
                breadcrumb = soup.find('div', class_='breadcrumb')
                if breadcrumb:
                    last_link = breadcrumb.find_all('a')[-1]
                    if last_link:
                        faculty_name = last_link.text.strip()
                else:
                    # Lấy tên khoa từ URL
                    faculty_name = faculty_name_from_url.replace('-', ' ').title()
        
        print(f"Faculty name: {faculty_name}")
        
        # Tìm div chứa nội dung chính
        content_div = None
        
        # Cách 1: Tìm div chứa nội dung theo class hoặc id phổ biến
        content_selectors = [
            ('div', {'class_': 'ms-rtestate-field'}),
            ('div', {'class_': 'article-content'}),
            ('div', {'id': 'DeltaPlaceHolderMain'}),
            ('div', {'class_': 'content'}),
            ('div', {'class_': 'ms-webpart-zone'})
        ]
        
        for tag, attrs in content_selectors:
            if attrs:
                content_div = soup.find(tag, **attrs)
            else:
                content_div = soup.find(tag)
            
            if content_div and content_div.text.strip():
                print(f"Found content in {tag} with attrs {attrs}")
                break
        
        # Cách 2: Nếu không tìm thấy, tìm div chứa nội dung theo cấu trúc trang
        if not content_div:
            # Tìm div chứa nội dung trong s4-workspace
            workspace = soup.find('div', id='s4-workspace')
            if workspace:
                main_content = workspace.find('div', id='contentRow')
                if main_content:
                    content_div = main_content.find('div', id='ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField')
        
        # Cách 3: Tìm div chứa nội dung theo vị trí
        if not content_div:
            main_div = soup.find('div', id='s4-bodyContainer')
            if main_div:
                content_areas = main_div.find_all('div', class_='ms-webpart-chrome-vertical')
                if content_areas and len(content_areas) > 0:
                    # Thường nội dung chính nằm ở div thứ 2 hoặc 3
                    for area in content_areas:
                        if area.text.strip() and len(area.text) > 200:  # Nội dung có ý nghĩa thường dài
                            content_div = area
                            break
        
        if not content_div:
            print(f"Could not find content div for {url}")
            return {
                "faculty_name": faculty_name,
                "introduction": "",
                "management_team": "",
                "url": url
            }
        
        # Trích xuất giới thiệu và ban chủ nhiệm
        introduction = ""
        management_team = ""
        
        # Phương pháp đặc biệt: Tìm cấu trúc HTML cụ thể cho ban chủ nhiệm
        # Tìm các thẻ div có class ho-ten, hoc-vi, chuc-vu
        management_info = []
        
        # Tìm tất cả các cặp ho-ten và chuc-vu
        ho_ten_divs = content_div.find_all('div', class_='ho-ten')
        if ho_ten_divs:
            print(f"Found {len(ho_ten_divs)} ho-ten divs")
            for ho_ten_div in ho_ten_divs:
                person_info = []
                
                # Lấy học vị (nếu có)
                hoc_vi = ho_ten_div.find('span', class_='hoc-vi')
                hoc_vi_text = hoc_vi.text.strip() if hoc_vi else ""
                
                # Lấy họ tên (loại bỏ phần học vị nếu có)
                ho_ten_text = ho_ten_div.text.strip()
                if hoc_vi_text:
                    ho_ten_text = ho_ten_text.replace(hoc_vi_text, "").strip()
                
                # Tìm chức vụ (thường là div tiếp theo)
                chuc_vu_div = ho_ten_div.find_next_sibling('div', class_='chuc-vu')
                chuc_vu_text = chuc_vu_div.text.strip() if chuc_vu_div else ""
                
                # Tạo thông tin đầy đủ
                if hoc_vi_text:
                    person_info.append(f"{hoc_vi_text} {ho_ten_text}")
                else:
                    person_info.append(ho_ten_text)
                
                if chuc_vu_text:
                    person_info.append(f"Chức vụ: {chuc_vu_text}")
                
                management_info.append(" - ".join(person_info))
        
        # Nếu tìm thấy thông tin theo cấu trúc đặc biệt, sử dụng nó
        if management_info:
            management_team = "\n".join(management_info)
            print(f"Found management team using special structure: {len(management_info)} members")
        
        # Phương pháp 1: Tìm theo cấu trúc HTML thông thường
        # Tìm tất cả các đoạn văn và tiêu đề
        elements = []
        for elem in content_div.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'strong', 'table']):
            if elem.name in ['p', 'div'] and not elem.find_all(['p', 'div', 'h1', 'h2', 'h3', 'h4', 'table']):
                if elem.text.strip():
                    elements.append((elem.name, elem.text.strip(), elem))
            elif elem.name in ['h1', 'h2', 'h3', 'h4', 'strong']:
                if elem.text.strip():
                    elements.append((elem.name, elem.text.strip(), elem))
            elif elem.name == 'table':
                table_text = []
                for row in elem.find_all('tr'):
                    cells = [cell.text.strip() for cell in row.find_all(['td', 'th']) if cell.text.strip()]
                    if cells:
                        table_text.append(" | ".join(cells))
                if table_text:
                    elements.append((elem.name, "\n".join(table_text), elem))
        
        # Tìm phần giới thiệu
        intro_keywords = ["giới thiệu", "tổng quan", "tổng quát", "thông tin chung", "chức năng nhiệm vụ", "lịch sử"]
        intro_section_start = -1
        intro_section_end = -1
        
        # Tìm vị trí bắt đầu của phần giới thiệu
        for i, (tag, text, elem) in enumerate(elements):
            if tag in ['h1', 'h2', 'h3', 'h4', 'strong'] and any(keyword in text.lower() for keyword in intro_keywords):
                intro_section_start = i
                break
        
        # Nếu tìm thấy tiêu đề giới thiệu, tìm vị trí kết thúc
        if intro_section_start >= 0:
            for i in range(intro_section_start + 1, len(elements)):
                tag, text, elem = elements[i]
                if tag in ['h1', 'h2', 'h3', 'h4', 'strong']:
                    intro_section_end = i
                    break
        
            # Nếu không tìm thấy tiêu đề kết thúc, lấy đến hết hoặc đến khi gặp từ khóa về ban chủ nhiệm
            if intro_section_end == -1:
                for i in range(intro_section_start + 1, len(elements)):
                    tag, text, elem = elements[i]
                    if any(keyword in text.lower() for keyword in ["ban chủ nhiệm", "ban lãnh đạo", "trưởng khoa", "phó trưởng khoa"]):
                        intro_section_end = i
                        break
            
            # Nếu vẫn không tìm thấy, lấy tối đa 10 phần tử sau tiêu đề
            if intro_section_end == -1:
                intro_section_end = min(intro_section_start + 10, len(elements))
            
            # Trích xuất nội dung giới thiệu
            intro_parts = []
            for i in range(intro_section_start, intro_section_end):
                tag, text, elem = elements[i]
                intro_parts.append(text)
            
            introduction = "\n".join(intro_parts)
        
        # Nếu không tìm thấy tiêu đề giới thiệu, lấy các đoạn văn đầu tiên
        if not introduction:
            intro_parts = []
            for i, (tag, text, elem) in enumerate(elements):
                if i >= 5:  # Lấy tối đa 5 phần tử đầu tiên
                    break
                if tag in ['p', 'div'] and not any(keyword in text.lower() for keyword in ["ban chủ nhiệm", "ban lãnh đạo", "trưởng khoa"]):
                    intro_parts.append(text)
            
            introduction = "\n".join(intro_parts)
        
        # Tìm thêm thông tin ban chủ nhiệm từ cấu trúc HTML khác
        if not management_team:
            # Tìm các thẻ có chứa thông tin về trưởng khoa, phó trưởng khoa
            management_info = []
            
            # Tìm các thẻ p hoặc div có chứa từ khóa liên quan đến chức vụ
            position_keywords = ["trưởng khoa", "phó trưởng khoa", "phó khoa", "trợ lý khoa"]
            for elem in content_div.find_all(['p', 'div']):
                elem_text = elem.text.lower()
                if any(keyword in elem_text for keyword in position_keywords):
                    # Tìm thẻ strong hoặc b trong phần tử này (thường là tên người)
                    person_name = ""
                    for strong in elem.find_all(['strong', 'b']):
                        if strong.text.strip() and not any(keyword in strong.text.lower() for keyword in position_keywords):
                            person_name = strong.text.strip()
                            break
                    
                    # Nếu không tìm thấy tên trong thẻ strong, lấy toàn bộ nội dung
                    if not person_name:
                        management_info.append(elem.text.strip())
                    else:
                        # Tìm chức vụ
                        position = ""
                        for keyword in position_keywords:
                            if keyword in elem_text:
                                position_pattern = rf"{keyword}[^,.:]*"
                                position_match = re.search(position_pattern, elem_text, re.IGNORECASE)
                                if position_match:
                                    position = position_match.group(0).strip()
                                    break
                        
                        if position:
                            management_info.append(f"{person_name} - {position}")
                        else:
                            management_info.append(person_name)
            
            if management_info:
                if not management_team:
                    management_team = "\n".join(management_info)
                else:
                    management_team += "\n" + "\n".join(management_info)
        
        # Làm sạch dữ liệu
        introduction = clean_text(introduction)
        management_team = clean_text(management_team)
        
        print(f"Introduction length: {len(introduction)}")
        print(f"Management team length: {len(management_team)}")
        
        return {
            "faculty_name": faculty_name,
            "introduction": introduction,
            "management_team": management_team,
            "url": url
        }
    
    except Exception as e:
        print(f"Error extracting information from {url}: {e}")
        import traceback
        traceback.print_exc()
        return {
            "faculty_name": "",
            "introduction": "",
            "management_team": "",
            "url": url
        }

def clean_text(text):
    """Làm sạch văn bản, loại bỏ khoảng trắng thừa và ký tự đặc biệt"""
    if not text:
        return ""
    
    # Loại bỏ nhiều dòng trống liên tiếp
    text = re.sub(r'\n\s*\n', '\n\n', text)
    
    # Loại bỏ khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text)
    
    # Loại bỏ khoảng trắng ở đầu và cuối mỗi dòng
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    text = '\n'.join(lines)
    
    return text.strip()

def save_to_csv(faculty_data):
    filename = "humg_faculties.csv"
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["faculty_name", "introduction", "management_team", "url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for faculty in faculty_data:
            writer.writerow(faculty)
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    crawl_humg_faculties()

