# result = twain.acquire("output.png", ds_name=b'PaperStream IP fi-65F', dpi=300, pixel_type='color')

from lib_photo_scanner import get_scanner

if __name__ == '__main__':
    ls, scanners, scanner_dict, scanner_name = get_scanner()
    image = ls.scan(scanner_name=scanner_name, return_type="based64")
    import ipdb; ipdb.set_trace()
