"""
GUI for KEXP DJ Assistants.  Checks and asks for API Keys.  Gets current playing song on KEXP and finds
KEXP events, KEXP YouTube videos, and local (WA & OR) events for the artist.
Also checks whether it is an anniversary for the album and calculates age.

Author: Michael Appleton
Date: August 20, 2022
"""

import flet
from flet import Page, Text, Row, icons, Divider, alignment, colors, ElevatedButton, TextField
from os.path import exists

file_exists = exists('api_config.py')

if file_exists != True:
# API Check and entry
    def main(page: Page):
        page.title = 'KEXP DJ Assistant API Key Entry'
        page.window_width = 500

        def write_keys():
                    write_keys.ytf = TextField(label="Enter your YouTube API Key:")
                    write_keys.btf = TextField(label="Enter your bitly API Key:")
                    write_keys.skf = TextField(label="Enter your Songkick API Key:")

        def save_keys(e):
            f = open('api_config.py', 'w')
            f.write('youtube_api = ' + "'" + write_keys.ytf.value + "'" + '\n' +
                    'bitly_api = ' + "'" + write_keys.btf.value + "'" + '\n' +
                    'songkick_api = ' + "'" + write_keys.skf.value + "'" + '\n'
                    )
            f.close()

            t.value = f"API Keys are: \nYouTube: {write_keys.ytf.value} \nbitly: {write_keys.btf.value} \nSongkick: {write_keys.skf.value}\n\n You may now close this window and start the DJ Assistant app."
            page.update()


        write_keys()
        t = Text()
        b = ElevatedButton(text="Save Keys", on_click=save_keys)
        page.add(write_keys.ytf, write_keys.btf, write_keys.skf,  b, t)

    flet.app(target=main)
# end API Check and entry

elif file_exists == True:
    import kexp_assist_func as k
# main app start
    def main(page: Page):
        page.title = 'KEXP DJ Assistant'
        page.vertical_alignment = 'start'
        page.scroll = 'auto'
        page.window_width = 400
        page.window_height = 875

        def pull_data():
            pull_data.current_play = k.get_playlist()
            if pull_data.current_play['artist'] != 'airbreak':
                pull_data.in_studios = k.get_instudios(pull_data.current_play['artist'])
                pull_data.shows = k.get_shows(pull_data.current_play['artist'])
                pull_data.videos = k.get_youtube(pull_data.current_play['artist'])
                if pull_data.current_play['release_date'] is not None:
                    anni = k.get_anniversary(pull_data.current_play['release_date'])
                    pull_data.current_play['anniversary'] = anni
                else:
                    pull_data.current_play['anniversary'] = ' '
            elif pull_data.current_play['artist'] == 'airbreak':
                pull_data.in_studios = 'N/A'
                pull_data.shows = 'N/A'
                pull_data.videos = 'N/A'
                pull_data.current_play['anniversary'] = 'N/A'


        def build_page():
            page.add(
                Row(
                    [
                        Text(value='Current Play', weight='bold'),
                    ]
                )
            )
            for x in ['artist', 'album', 'song', 'release_date', 'anniversary']:
                page.add(
                    Row(
                    [
                        Text(value= x + ": ", weight='bold'),
                        Text(value=pull_data.current_play[x], selectable=True),
                    ]
                    ),
                )
            page.add(Divider(height=1, color="black"))
            short_videos = pull_data.videos = str.replace(str.replace(' '+pull_data.videos, 'Recorded', '\n Recorded'), 'http://KEXP.ORG presents ', '')
            for x, y in {'Upcoming In-studios': pull_data.in_studios,'WA & OR Shows': pull_data.shows,'Recorded Sessions': short_videos}.items():
                page.add(
                    Row(
                        [
                            Text(value=x + ": ", weight='bold'),
                        ]
                    ),
                    Row(
                        [
                            Text(value=str.replace(y, '<br>', '\n'), no_wrap=False, selectable=True, width=375)
                        ]
                    ),
                    Divider(height=1, color="black")
                ),



        def refresh_page(d):
            pull_data()
            for i in range(16):
                page.controls.pop()
            build_page()
            page.update()

        page.add(
            Row(
                [
                    ElevatedButton("Refresh", on_click=refresh_page, icon="autorenew_sharp")
                ],alignment="center",
            ),
            Divider(height=1, color="black")
        )

        page.update()
        pull_data()
        build_page()


    flet.app(target=main)
# main app end
