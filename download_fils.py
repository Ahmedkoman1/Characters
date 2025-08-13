import os
import requests
from tqdm import tqdm

def download_file(url, save_dir):
    file_name = url.split("/")[-1].replace("%2B", "+")
    dest_path = os.path.join(save_dir, file_name)
    temp_size = os.path.getsize(dest_path) if os.path.exists(dest_path) else 0

    headers = {}
    if temp_size > 0:
        headers['Range'] = f'bytes={temp_size}-'

    try:
        with requests.get(url, headers=headers, stream=True, timeout=60) as r:
            if r.status_code in (200, 206):
                # تحديد الحجم الكلي للملف
                if 'Content-Range' in r.headers:
                    total_size = int(r.headers['Content-Range'].split('/')[-1])
                else:
                    total_size = int(r.headers.get('Content-Length', 0))

                mode = 'ab' if temp_size > 0 else 'wb'

                with open(dest_path, mode) as f, tqdm(
                    total=total_size,
                    initial=temp_size,
                    unit='B',
                    unit_scale=True,
                    desc=f"⬇️ {file_name}"
                ) as pbar:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

                print(f"✅ تم تحميل: {dest_path}")
                return dest_path


            else:
                print(f"❌ فشل تحميل {file_name} (رمز الحالة: {r.status_code})")
    except Exception as e:
        print(f"⚠️ خطأ في تحميل {file_name}: {e}")
    return None

if __name__ == "__main__":
    cuda_url = "https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt"
    save_dir = os.path.expanduser(r"C:\Users\TOSHIBA\.cache\whisper")  # مجلد التنزيلات
    os.makedirs(save_dir, exist_ok=True)
    download_file(cuda_url, save_dir)
