import os_android_launcher_creator.launcher_creator as lc
import os_tools.FileHandler as fh

resize_percent = 50
background_color_hex = '#ffffff'
custom_android_project_path = '/Users/home/Programming/android/coroutine/rwdc-coroutines-materials/starter'
STATICa_RES_RELATIVE_PATH = 'app/src/main/res'
icon_files_path = '/Users/home/Desktop/stock_exchange/icons/files'
output_path = '/Users/home/Desktop/stock_exchange/icons/temp'

icon_files_1 = fh.search_files(icon_files_path, False, False, False, '.png')
icon_files_2 = fh.search_files(icon_files_path, False, False, False, '.svg')
icon_files = icon_files_1 + icon_files_2

lc.create_launcher_icons(custom_android_project_path=custom_android_project_path,
                         icon_files_list=icon_files,
                         output_path=output_path,
                         shortcut_keys_to_open_image_asset=['shift', 'b'],
                         launcher_resize_percent=35,
                         launcher_background_color_hex='#ffffff',
                         delete_icon_after_done=True)
