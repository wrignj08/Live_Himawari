import os
import time
import json
import funcs
import pathlib
import itertools
import threading
from glob import glob
from PIL import Image
from datetime import datetime
from multiprocessing.pool import ThreadPool
# necessary to make pyinstaller not spawn multiple apps
from multiprocessing import freeze_support
freeze_support()

verbose = True

sf_hourglass = '⧖  '
sf_play = '▶ '
sf_stop = '■ '
sf_download = '⬇ '
sf_working = '⚙ '
sf_refresh = '↻ '

def main_thread():
    thread = threading.Thread(target=lambda: threading.Thread(target=main(),daemon = True))
    thread.start()

def main():

    if verbose:
        print('started main')

    funcs.set_state(sf_play+'Starting')
    # keep looping untill told to stop
    while True:

        settings = funcs.get_settings()
        quality = int(settings['quality'])
        thread_count = int(settings['dl_threads'])
        live = bool(settings['live'])

        if not live:
            if verbose:
                print('stopped')
            funcs.set_state(sf_stop+'Stopped')
            # break look if no longer live
            break

        # tile row and col count, 2 means the image is built from 2x2 tiles
        image_size = [2,4,8,16,20]

        # set quality
        row_col_count = image_size[quality]

        # calc final output image size
        img_size = 550
        array_px = row_col_count*img_size

        # generate all row and col combination
        tile_list = list(itertools.product(range(0,row_col_count), range(0,row_col_count)))

        # set directory for images
        working_path = funcs.get_image_dir()

        # url format for downlading images
        url_template = 'https://himawari8.nict.go.jp/img/D531106/{}d/550/{}/{}_{}_{}.png'

        # check every x secs if there is a new image to download
        found_new = False

        latest_date,latest_time = funcs.get_latest_time()

        # check if this image is already made
        final_output = os.path.join(working_path,(latest_date+latest_time).replace('/','_')+f'_LH_{quality}.png')
        if verbose:
            print(final_output)
        # funcs.set_state(final_output)
        if not os.path.isfile(final_output):

            args = []
            for coords in tile_list:
                args.append([coords,image_size,quality,latest_date,latest_time,working_path])

            # downlaod multible images at one to speed up the process
            if verbose:
                print('downloading tiles')
            funcs.set_state(sf_download+'Downloading tiles')
            # download images
            with ThreadPool(thread_count) as tp:
                files = list(tp.imap(funcs.prep_download,args))

            # mosaic all images
            if verbose:
                print('making mosaic')
            funcs.set_state(sf_working+'️Making mosaic')

            # make mosaic using PIL
            mosaiced_image = funcs.PIL_mosaic(files,array_px)

            # grab a list of any old mosaics so we can remove them later
            old_lh_files = glob(working_path+'/*.png')

            # save master array as image
            if verbose:
                print('saving wallpaper')
            mosaiced_image.save(final_output)

            if verbose:
                print('setting wallpaper')
            # funcs.set_wallpaper(final_output)
            threading.Thread(target=funcs.set_wallpaper(final_output))

            # remove old images
            if verbose:
                print('Removing wallpaper')
            for old_file in old_lh_files:
                os.remove(old_file)
            if verbose:
                print('done')

            # grab the current settings and add the new wp path
            settings = funcs.get_settings()
            settings['wp_path'] = final_output
            settings['date'] = latest_date
            settings['time'] = latest_time
            funcs.write_settings(settings)

        else:
            # if there is nothing new to download, sleep
            if verbose:
                print(f'nothing new, sleeping for 5 minutes')
            sleep_time  = 300

            for i in range(0,sleep_time):
                # calc remaining sleep time and set state
                sleep_time_remaining = sleep_time-i
                if sleep_time_remaining > 60:
                    sleep_time_remaining_str = f'{round(sleep_time_remaining/60)} mins'
                else:
                    sleep_time_remaining_str = f'{sleep_time_remaining} secs'

                funcs.set_state(sf_hourglass+f'Next check in {sleep_time_remaining_str}')
                # check the settings file
                settings = funcs.get_settings()
                # if live is False end sleep early
                if not bool(settings['live']):
                    break
                # if refresh is set end sleep early
                if bool(settings['refresh']):
                    funcs.set_state(sf_refresh+'Refreshing')
                    # remove old wallpaper
                    if os.path.isfile(final_output):
                        os.remove(final_output)
                    # reset to False and end sleep early
                    settings['refresh'] = False
                    funcs.write_settings(settings)
                    break

                else:
                    time.sleep(1)
