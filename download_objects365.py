import urllib.request
import os
import concurrent.futures
train_urls = []
val_urls = []
test_urls = []

# val set
for i in range(0, 16):
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/val/images/v1/patch{i}.tar.gz"
    val_urls.append(url)

for i in range(16, 44):
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/val/images/v2/patch{i}.tar.gz"
    val_urls.append(url)

# test set

for i in range(0, 16):
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/test/images/v1/patch{i}.tar.gz"
    test_urls.append(url)

for i in range(16, 51):
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/test/images/v2/patch{i}.tar.gz"
    test_urls.append(url)

# train set
for i in range(51):
    url = f"https://dorc.ks3-cn-beijing.ksyun.com/data-set/2020Objects365%E6%95%B0%E6%8D%AE%E9%9B%86/train/patch{i}.tar.gz"
    train_urls.append(url)

def download_file(url, local_path):
    try:
        filename = os.path.join(local_path,os.path.basename(url))
        urllib.request.urlretrieve(url, filename)
        print(f"Done: {url}")
    except Exception as e:
        print(f"Error: {url}: {e}")

def download_files(urls, local_path, max_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(download_file, url, local_path): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error {url} {e}")

if __name__ == "__main__":
    # prepare folder
    train_folder = "./train"
    test_folder = "./test"
    val_folder = "./val"
    os.makedirs(train_folder, exist_ok=True)
    os.makedirs(test_folder, exist_ok=True)
    os.makedirs(val_folder, exist_ok=True)
    max_threads = 4
    # start
    print(f"downloading test set,{len(test_urls)} files")
    download_files(test_urls, test_folder, max_threads)
    print(f"downloading train set,{len(train_urls)}files")
    download_files(train_urls,train_folder,max_threads)
    print(f"downloading val set,{len(val_urls)}files")
    download_files(val_urls, val_folder, max_threads)
