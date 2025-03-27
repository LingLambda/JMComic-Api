import gc
from pathlib import Path

from jmcomic import download_album

from pdf_util import merge_webp_to_pdf


def get_album_pdf_path(jm_album_id, pdf_dir, is_pwd, opt):
    # 下载本子（只下载单文件，不需要 unpack tuple）
    album, _ = download_album(jm_album_id, option=opt)
    title = album.title
    pdf_path = f"{pdf_dir}/{title}.pdf"

    if not Path(pdf_path).exists():
        webp_folder = f"./{title}"
        merge_webp_to_pdf(webp_folder, pdf_path=pdf_path, is_pwd=is_pwd, password=jm_album_id)
        gc.collect()  # 强制垃圾回收

    return pdf_path, f"{title}.pdf"
