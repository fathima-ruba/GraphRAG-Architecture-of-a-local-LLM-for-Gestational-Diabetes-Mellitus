import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2000-2024',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2000.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "2021"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2021.csv"
download_open_access_pdfs(csv_filename)

import shutil

folder_path = '/content/2022'
zip_filename = '2022'
shutil.make_archive(zip_filename, 'zip', folder_path)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2023',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2023.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2023.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2022',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2022.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2022.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2021',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2021.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2021.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2020',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2020.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2020.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2019',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2019.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2019.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2018',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2018.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2018.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2017',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2017.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2017.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2016',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2016.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2016.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2015',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2015.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2015.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2014',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2014.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2014.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2013',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2013.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2013.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2012',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2012.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2012.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2011',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2011.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2011.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2010',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2010.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2010.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2009',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2009.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2009.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2008',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2008.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2008.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2007',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2007.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2007.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2006',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2006.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2006.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2005',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2005.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2005.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2004',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2004.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2004.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2003',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2003.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2003.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2002',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2002.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2002.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2001',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2001.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2001.csv"
download_open_access_pdfs(csv_filename)

import requests
import csv

def fetch_and_save_papers(url, query_params, csv_filename):
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        response_json = response.json()
        papers = response_json['data']
        if papers:
            with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['Title', 'Publication Type', 'Publication Date', 'Abstract', 'Full Text URL', 'Paper ID', 'Corpus ID', 'DOI', 'Is Open Access', 'Open Access PDF'])
                if csvfile.tell() == 0:
                    writer.writeheader()
                for paper in papers:
                    writer.writerow({
                        'Title': paper.get('title', 'N/A'),
                        'Publication Type': ', '.join(paper.get('publicationTypes', ['N/A'])),
                        'Publication Date': paper.get('publicationDate', 'N/A'),
                        'Abstract': paper.get('abstract', 'N/A'),
                        'Full Text URL': paper.get('url', 'N/A'),
                        'Paper ID': paper.get('paperId', 'N/A'),
                        'Corpus ID': paper.get('corpusId', 'N/A'),
                        'DOI': paper.get('externalIds', {}).get('DOI', 'N/A'),
                        'Is Open Access': paper.get('isOpenAccess', 'N/A'),
                        'Open Access PDF': paper.get('openAccessPdf', {}).get('url') if paper.get('openAccessPdf') else 'N/A'
                    })
            return True
    return False

base_query_params = {
    'query': 'gestational diabetes intervention',
    'publicationTypes': 'JournalArticle',
    'fields': 'title,publicationTypes,publicationDate,url,abstract,paperId,corpusId,externalIds,isOpenAccess,openAccessPdf',
    'year': '2000',
    'limit': 100000000000000000000000
}

url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"

csv_filename = "2000.csv"
fetch_and_save_papers(url, base_query_params, csv_filename)

import os
import requests
import csv

folder_name = "PDFs"
os.makedirs(folder_name, exist_ok=True)

def download_open_access_pdfs(csv_filename):
    papers_downloaded = 0
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            open_access_pdf_url = row.get('Open Access PDF', None)
            if open_access_pdf_url and open_access_pdf_url != 'N/A':
                paper_id = row.get('Paper ID', 'N/A')
                pdf_file_name = f"{paper_id}.pdf"
                pdf_save_path = os.path.join(folder_name, pdf_file_name)
                try:
                    with open(pdf_save_path, 'wb') as pdf_file:
                        pdf_response = requests.get(open_access_pdf_url)
                        pdf_file.write(pdf_response.content)
                    print(f"Downloaded: {pdf_file_name}")
                    papers_downloaded += 1
                except Exception as e:
                    print(f"Error downloading {pdf_file_name}: {e}")
            else:
                print(f"No Open Access PDF available for {row.get('Title', 'N/A')}")

    print(f"Total papers downloaded: {papers_downloaded}")

csv_filename = "2000.csv"
download_open_access_pdfs(csv_filename)

import shutil

folder_path = '/content/PDFs'
zip_filename = 'PDFs'
shutil.make_archive(zip_filename, 'zip', folder_path)
