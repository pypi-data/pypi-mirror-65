#!/usr/bin/env python3

import sys
import os
import time
import datetime
import urwid # Curses interface
import requests # Fetch data from APIs
import ast # Safely parse "python" API output
import webbrowser # For Open command
import syslog
from threading import Thread # To run API requests non-blocking
import appdirs
import configparser

class Chk:
    project_name = 'checkmk-commander'
    list_position = 0
    version = '0.8.6'
    mode = 'normal'
    focused_line = None
    status = 'Starting...'
    list_position = 0
    config_path = ''
    api_base_url = ''
    host = None
    service = None

    @staticmethod
    def fetch_time():
        ''' Return a formated time '''
        return '{0:%H:%M:%S}'.format(datetime.datetime.now())

    @staticmethod
    def parse_time(text):
        ''' Input can be  2h, 100, 4h, 5m, 333s.
        Will return a positive number of seconds or -1 for no time.'''

        time_designators = {'s': 1, 'm': 60, 'h': 3600, 'd': 84600}

        text = text.strip()
        time_designator = ''
        number = text

        # Need more than one character, no spaces please, no negative values
        if len(text) < 2 or ' ' in text or '-' in text:
            return -1

        for td in time_designators.keys():
            if text.endswith(td):
                time_designator = td
                break

        try:
            number = int(text.replace(td,''))
        except ValueError:
            return -1

        try:
            number = number*time_designators[time_designator]
        except KeyError:
            pass

        return number

    @staticmethod
    def scrub_secret (text):
        ''' Check urls for the automation secret and scrubb it away '''

        if '_secret' in text:
            secret_start = text.index('_secret=')
            secret_end = text.index('&', secret_start)
            text = text[:secret_start] + text[secret_end:]
        return text

    def validate_config(self):
        if not self.config_path:
            self.config_path = appdirs.user_config_dir(self.project_name) + '.ini'

        config = configparser.ConfigParser()
        config.read(self.config_path)

        # Validate config
        if not os.path.isfile(self.config_path):
            print(f"No config found, creating one at {self.config_path}")
            self.checkmkhost = input("Full address to your checkmk host including 'site', example http://checkmk.example.com/mysite/: ")
            self.checkmkusername = input('Username. Must me a "machine" user with a secret, not a password: ')
            self.checkmksecret = input('Secret: ')

            config.add_section('main')
            config.set('main', 'host', self.checkmkhost)
            config.set('main', 'username', self.checkmkusername)
            config.set('main', 'secret', self.checkmksecret)
            config.set('main', 'delay', str(5)) # Default refresh value

            with open(self.config_path, 'w') as f:
                config.write(f)
        else:
            self.checkmkhost = config.get('main', 'host')
            self.checkmkusername = config.get('main', 'username')
            self.checkmksecret = config.get('main', 'secret')
            self.delay = config.getint('main', 'delay')

        self.api_base_url = self.checkmkhost + \
            'check_mk/view.py' + \
            '?_transid=-1' + \
            '&_do_actions=yes&_do_confirm=yes' + \
            '&output_format=json&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret

    def main(self):
        syslog.syslog(f"{self.project_name} version {self.version} started.")

        self.validate_config()

        # Load GUI
        self.setup_view()

        # Color palette
        palette = [ # http://urwid.org/manual/displayattributes.html#foreground-background
            # Name of the display attribute, typically a string
            # Foreground color and settings for 16-color (normal) mode
            # Background color for normal mode
            # Settings for monochrome mode (optional)
            # Foreground color and settings for 88 and 256-color modes (optional, see next example)
            # Background color for 88 and 256-color modes (optional)
            ('header', 'black', 'light gray'),
            ('reveal focus', 'black', 'dark cyan', 'standout'),
            ('CRIT', 'dark red', '', '', '', ''),
            ('WARN', 'yellow', '', '', '', ''),
            ('UNKN', 'dark magenta', '', '', '', ''),
            ('New', 'white', '', '', '', ''),
            ('Old', 'brown', '', '', '', ''),
            ('darker', '', 'dark gray', '', '', ''),
            ('Connected', '', 'dark green', '', '', ''),
            ('Disonnected', '', 'dark red', '', '', '')
        ]

        # Main loop
        self.loop = urwid.MainLoop(self.top, palette,
            unhandled_input=self.handle_key_input,
            handle_mouse=False
    )
        self.loop.set_alarm_in(self.delay, self.refresh_ui)
        self.loop.run()

    def refresh_ui(self, loop=None, data=None):
        ''' Refresh GUI, and set alarm for next refresh '''
        if self.mode == 'normal':
            self.setup_view()
            self.loop.widget = self.top
        self.loop.set_alarm_in(self.delay, self.refresh_ui)

    def handle_key_input(self, input):
        ''' Handle key presses '''

        # Hotkeys
        if input in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            self.list_position = int(input)
            self.listbox.set_focus(self.list_position)

        # Quit
        elif input in ['q', 'Q']:
            raise urwid.ExitMainLoop()

        # Escape from actions
        elif input == 'esc':
            if self.mode != 'normal':
                self.status = ''
                self.mode = 'normal'
                self.refresh_ui()

        # Navigate list
        elif (input == 'up' or input == 'k') and 0 < len(self.listbox.body):
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position > 0:
                self.list_position = self.list_position-1
            self.listbox.set_focus(self.list_position)

        elif (input == 'down' or input == 'j') and 0 < len(self.listbox.body):
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position+1 < len(self.listbox.body):
                self.list_position = self.list_position+1
            self.listbox.set_focus(self.list_position)

        elif (input == 'page down' or input == 'l') and 0 < len(self.listbox.body):
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position+10 < len(self.listbox.body):
                self.list_position = self.list_position+10
            self.listbox.set_focus(self.list_position)

        elif (input == 'page up' or input == 'h') and 0 < len(self.listbox.body):
            focus_widget, self.list_position = self.listbox.get_focus()
            if self.list_position-10 > len(self.listbox.body):
                self.list_position = self.list_position-10
            else:
                self.list_position = 0
            self.listbox.set_focus(self.list_position)

        elif input == '?': # Help
            #| Downtime | Reschedule | Sites | Filter | Sort | Select | Reinventorize | New | '),
            self.mode = 'help'
            self.dialog(
                [
                    'Help',
                    '? - This dialog\n' +\
                    'q - Quit\n' +\
                    '←↓→, hjkl - Select line\n' +\
                    'Enter - Show details for selected service\n' +\
                    'Esc - Abort\n' +\
                    '0-9 - Jump to list entry\n' +\
                    'a - Acknowledge\n' +\
                    'r - Reinventorize (fix missing/vanished)\n' +\
                    'c - Comment\n' +\
                    'w - Open checkmk in web browser'
                ],
                align = 'left',
            )

        elif input == 'a': # Acknowledge
            try:
                focus_widget, self.list_position = self.listbox.get_focus()
            except IndexError:
                return

            self.target = focus_widget.base_widget.widget_list[1].text
            self.service = focus_widget.base_widget.widget_list[2].text
            self.mode = 'ack'
            self.commandinput.set_caption('Ack > ')

            self.dialog(
                [
                    'Acknowledge',
                    'Ack <%s, %s> ?\n\n' % (self.target, self.service),
                    'Type an optional time designator, a required comment and' +
                    'hit enter.\n\n I.e. "2h Not in prod yet".\n\n',
                    'Esc to abort.\n'
                ],
            self.commandinput
            )

        elif input == 'c': # Comment
            try:
                focus_widget, self.list_position = self.listbox.get_focus()
            except IndexError:
                return

            self.target = focus_widget.base_widget.widget_list[1].text
            self.service = focus_widget.base_widget.widget_list[2].text
            self.mode = 'comment'
            self.commandinput.set_caption('Comment > ')

            self.dialog(
                [
                    'Comment <%s, %s> ?\n\n' % (self.target, self.service),
                    'Type a comment and hit enter.\n\n',
                    'Esc to abort.\n'
                ],
            self.commandinput
            )

        elif input == 'd': # Downtime
            try:
                focus_widget, self.list_position = self.listbox.get_focus()
            except IndexError:
                return

            self.target = focus_widget.base_widget.widget_list[1].text
            self.service = focus_widget.base_widget.widget_list[2].text
            self.mode = 'downtime'
            self.commandinput.set_caption('Down > ')

            self.dialog(
                [
                    'Downtime',
                    'Downtime <%s, %s> ?\n\n' % (self.target, self.service),
                    'Type an optional time designator, a required comment and' +
                    'hit enter.\n\n I.e. "2h Not in prod yet".\n\n',
                    'Esc to abort.\n'
                ],
            self.commandinput
            )

        elif input == 'r': # Reinventorize
            try:
                focus_widget, self.list_position = self.listbox.get_focus()
            except IndexError:
                return

            self.target = focus_widget.base_widget.widget_list[1].text
            self.service = focus_widget.base_widget.widget_list[2].text
            self.mode = 'reinventorize'
            self.commandinput.set_caption('Confirm > ')

            self.dialog(
                [
                    'Reinventorize',
                    'Fix all missing/vanished for <%s>?\n\n' % self.target,
                    'Enter to confirm, Esc to abort.\n'
                ],
            self.commandinput
            )

        elif input == 'w': # Open checkmk website
            self.status = f"{Chk.fetch_time()} Opening checkmk website"
            webbrowser.open(self.checkmkhost, new=2)

        elif input == 'enter': # Handle Enter, which could mean loads of stuff
            # Parse time
            time = self.commandinput.caption
            try:
                time = int(str(time.split('[')[1]).split(']')[0])
            except IndexError:
                time = None

            # Check if service or host
            if self.service and self.service == 'Host is down':
                self.service = None

            if self.mode == 'ack':
                self.acknowledge_service(
                    host = self.target,
                    service = self.service,
                    time = time,
                    comment = self.commandinput.get_edit_text())

            elif self.mode == 'comment':
                self.comment_service(
                    host = self.target,
                    service = self.service,
                    # TODO: time = time,
                    comment = self.commandinput.get_edit_text())

            elif self.mode == 'downtime':
                self.downtime_service(
                    host = self.target,
                    service = self.service,
                    time = time,
                    comment = self.commandinput.get_edit_text())

            elif self.mode == 'reinventorize':
                self.reinventorize_host(self.target)

            elif self.mode == 'details':
                self.mode = 'normal'
                self.refresh_ui()

            else: # Show details
                try:
                    focus_widget, self.list_position = self.listbox.get_focus()
                except IndexError:
                    return

                self.host = focus_widget.base_widget.widget_list[1].text
                self.service = focus_widget.base_widget.widget_list[2].text
                self.output = focus_widget.base_widget.widget_list[3].base_widget.text

                # Show last 5 service comments
                comment_list = self.fetch_comments(self.host, self.service)
                comments = "Last five comments:\n"
                for comment_author, comment_comment, comment_time, \
                    _, _ in comment_list[:5]:
                    comments += f"{comment_time} - {comment_author}: {comment_comment}\n"

                self.mode = 'details'
                self.dialog([
                        'Service details',
                        f"{self.host} - {self.service}\n",
                        f"{self.output}\n\n",
                        f"{comments}",
                    ]
                )

    def setup_view(self):
        line_number = 0
        services = self.fetch_serviceproblems()
        hosts = self.fetch_hostproblems()
        listbox_content = []

        for service_state, host, _, _, _, _, _, _ in hosts:

            listbox_content += urwid.Columns(
            [
                ('weight', 1, urwid.Text(str(line_number))),
                ('weight', 4, urwid.Text(host, wrap='clip')),
                ('weight', 4, urwid.Text('Host is down', wrap='clip')),
                ('weight', 10, urwid.AttrMap(urwid.Text('DOWN', wrap='clip'), service_state)),
                ('weight', 2, urwid.Text('', wrap='clip')),
            ], dividechars=1),
            line_number += 1

        for service_state, host, service_description, _, svc_plugin_output, \
            svc_state_age, _, _ in services:

            # Format time
            timestamp_style = 'Disconnected'
            if 'm' in svc_state_age: # Younger than an hour
               timestamp_style = 'New'
            if not 's' in svc_state_age \
                and not 'm' in svc_state_age \
                and not 'h' in svc_state_age:
                svc_state_age = svc_state_age.split()[0]

            listbox_content += urwid.Columns(
            [
                ('weight', 1, urwid.Text(str(line_number))),
                ('weight', 4, urwid.Text(host, wrap='clip')),
                ('weight', 4, urwid.Text(service_description, wrap='space')),
                ('weight', 10, urwid.AttrMap(urwid.Text(svc_plugin_output, wrap='clip'), service_state)),
                ('weight', 2, urwid.AttrMap(urwid.Text(svc_state_age, wrap='clip'), timestamp_style))
            ], dividechars=1),
            line_number += 1

        self.listbox = urwid.ListBox(urwid.SimpleListWalker([
                urwid.AttrMap(w, None, 'reveal focus') for w in listbox_content]))
        try:
            self.listbox.set_focus(self.list_position)
        except IndexError: # No alerts
            pass

        # Top menu
        self.show_key = urwid.Text([
            ('darker', f"{self.project_name} v{self.version} | Updated {Chk.fetch_time()} "),
            ' Type ? for help',
        ], wrap='space')
        head = urwid.AttrMap(self.show_key, 'header')

        # Input box
        self.commandinput = urwid.Edit()
        urwid.connect_signal(self.commandinput, 'postchange', self.command_changed)

        if self.status == 'Starting...':
            # Show site overview on start
            self.status = f'{Chk.fetch_time()} connected to sites: '
            sites = self.fetch_sites()
            for site_name, _ in sites:
               self.status += f"{site_name}, "

        self.statusbar = urwid.Text(('darker', self.status))

        # top : listbox, head
        self.top = urwid.Frame(self.listbox, header=head, footer=self.statusbar)

    def fetch_serviceproblems(self):
        ''' Fetch unhandled service problems
        
            # Example returned: [
            # ['service_state', 'host', 'service_description', 'service_icons', 'svc_plugin_output', 'svc_state_age', 'svc_check_age', 'perfometer'],
            # ['CRIT',u'laptop1016',u'Memory','themes/facelift/images/icon_menu themes/facelift/images/icon_pnp ack comment',u'CRIT - RAM used: 13.5 GB of 23.26 GB (58.1%), Largest Free  ...
         '''
        r = None
        url = self.api_base_url +\
                '&is_service_acknowledged=0' + \
                '&view_name=svcproblems'

        try:
            r = requests.get(url)
        except requests.exceptions.MissingSchema as e:
            print(f"Error fetching service problems. Wrong checkmk url? Check url in config file {self.config_path}. Error: {e}")
            sys.exit(1)
        except requests.exceptions.ConnectionError as e:
            self.write_status_and_log(message='Temporary error connecting to {url}')
            return None

        if 'ERROR: Invalid automation secret' in r.text:
            print(f"Error fetching service problems. Wrong auth? Check user and sercret in config file {self.config_path}. Error message from server: {r.text}")
            sys.exit(1)

        # Remove first line (header) and reverse the list
        return (r.json()[1::])[::-1]

    def fetch_hostproblems(self):
        ''' Fetch unhandled host problems

            # Example output
            ['DOWN', 'centos7.lxd', 'themes/facelift/ima.../icon_pnp', '37', '5', '0', '2', '0'] '''

        r = None
        try:
            r = requests.get(self.api_base_url + \
                '&is_host_acknowledged=0' + \
                '&view_name=hostproblems'
            )
        except requests.exceptions.ConnectionError as e:
            self.status = f'{self.fetch_time} Temporary error connecting to {url}'
            syslog.syslog(syslog.LOG_ERR, f'Temporary error connecting to {url}')
            return None

        # Remove first line (header) and reverse the list
        return (r.json()[1::])[::-1]

    def dialog(self, text, edit = None, align='center'):
        '''
        Overlays a dialog box on top of the console UI
        Args:
            text (list): A list of strings to display. First string will be header
            edit (edit widget): An edit box to type a response in
        '''

        # Header
        header_text = urwid.Text(('banner', f'{self.project_name} - %s' % text[0] ), align = 'center')
        header = urwid.AttrMap(header_text, 'banner')

        # Body
        body_text = urwid.Text(text[1:], align = align)
        body_filler = urwid.Filler(body_text, valign = 'top')
        body_padding = urwid.Padding(
            body_filler,
            left = 1,
            right = 1
        )
        body = urwid.LineBox(body_padding)

        footer = edit

        # Layout
        layout = urwid.Frame(
            body,
            header = header,
            footer = footer,
            focus_part = 'footer'
        )

        w = urwid.Overlay(
            urwid.LineBox(layout),
            self.top,
            align = 'center',
            valign = 'middle',
            width = 70,
            height = 15
        )
        self.loop.widget = w

    def acknowledge_service(self, host, service = None, time = None, comment=''):
        ''' Ack a service or host problem with optional comment and time '''

        url = self.api_base_url +\
            '&host=' + host + \
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&_ack_comment=' + comment + \
            '&host=' + host

        if service:
            url += '&view_name=service' + \
                '&service=' + service

        else: # Ack host
            url += '&view_name=hoststatus'

        if time:
            url += '&_ack_expire_minutes=' + str(time//60)

        t = Thread(target = self.background_request, args =(url, f'ack {host} - {service}' )) 
        t.start()

        self.mode = 'normal'

    def comment_service(self, host, service, comment = ''):
        ''' Comment a host or service problem '''

        url = self.api_base_url +\
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&host=' + host +\
            '&_ack_comment=' + comment +\
            '&_down_comment=' + comment +\
            '&_comment=' + comment +\
            '&_add_comment=Add+comment'

        if service:
            url += '&view_name=service' + \
                '&service=' + service
        else: # Downtime host
            url += '&view_name=hoststatus'


        t = Thread(target = self.background_request, args =(url, f'comment {host} - {service}' )) 
        t.start()

        self.mode = 'normal'

    def downtime_service(self, host, service = None, time = None, comment=''):
        ''' Downtime service or host problem with optional comment and time '''

        url = self.api_base_url +\
            '&_acknowledge=Acknowledge&_ack_sticky=on&_ack_notify=on' + \
            '&host=' + host +\
            '&_ack_comment=' + comment +\
            '&_down_comment=' + comment +\
            '&_comment=' + comment

        if service:
            url += '&view_name=service' + \
                '&service=' + service
        else: # Downtime host
            url += '&view_name=hoststatus'

        if time:
            from_time = datetime.datetime.now()
            to_time = from_time + datetime.timedelta(seconds=time)

            url += '&_down_minutes=' + str(time//60) + \
                '&_down_from_now=From+now+for' + \
                '&_down_from_date=' + '{:%Y-%m-%d}'.format(from_time) + \
                '&_down_from_time=' + '{:%H:%M}'.format(from_time) + \
                '&_down_to_date=' + '{:%Y-%m-%d}'.format(to_time) + \
                '&_down_to_time=' + '{:%H:%M}'.format(to_time)

        t = Thread(target = self.background_request, args =(url, f'ack {host} - {service}' )) 
        t.start()

        self.mode = 'normal'

    def reinventorize_host(self, host):
        ''' Reinventorize a host, meaning fix all missing/vanished '''
        # discover_services at https://checkmk.com/cms_web_api_references.html

        url = self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=discover_services' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret

        postdata={
                "hostname":host,
                "mode":"fixall"
                }

        t = Thread(target = self.background_request, args =(url, f'Reinv. {host}', 'post', postdata )) 
        t.start()

        self.mode = 'normal'

    def activate_wato_change(self, site=None, comment=''):
        ''' Activate a WATO change. Returns result string. '''
        # https://checkmk.com/cms_web_api_references.html#activate_changes

        r = requests.post(self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=activate_changes' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret,
            data={
                "mode": "dirty",
                "allow_foreign_changes": "0",
                "comment": comment
                }
        )

        return ''.join(ast.literal_eval(r.text)['result'])

    def fetch_comments(self, host, service):
        ''' Fetch all comments for a service '''

        r = requests.get(self.api_base_url +\
            '&view_name=comments_of_service' + \
            '&host=' + host + \
            '&service=' + service)

        self.status = f"{Chk.fetch_time()} Found {len(r.json())-1} comments for {host}-{service}."
        return (r.json()[1:])[::-1] # Skip header, sort by latest first

    def fetch_sites(self, site=None):
        ''' Fetch sites (this user has access to)'''
        # https://checkmk.com/cms_web_api_references.html

        r = requests.get(self.checkmkhost + \
            'check_mk/webapi.py' + \
            '?action=get_user_sites' + \
            '&output_format=python&_username=' + \
            self.checkmkusername + \
            '&_secret=' + \
            self.checkmksecret)

        return ast.literal_eval(r.text)['result']

    def command_changed(self, widget, text):
        ''' In ack, comment, downtime, attempt to parse a time from comment '''

        if self.mode in ['ack', 'comment', 'downtime']:
            default_caption = '> '
            word = widget.get_edit_text()

            if len(word) < 3 or ' ' not in word:
                widget.set_caption(default_caption)
                return

            time = Chk.parse_time(word.split()[0])
            if time == -1 or time < 60:
                widget.set_caption(default_caption)
            else:
                widget.set_caption(f"(Time: [{time}] seconds) {default_caption}")

    def background_request(self, url, description='', type='get', postdata={}):
        ''' Run a web request in background, and update status line.
            Assume any POST request needs a WATO activation request after.'''

        self.write_status_and_log(
            message=f"Running {description}...",
            message_short=f'Calling url in background, {url}')

        response = ''
        status_code = 0

        if type == 'get':
            r = requests.get(url)
            status_code = r.status_code
            response = r.text.replace(os.linesep, '')
        else:
            r = requests.post(url, data=postdata)
            status_code = r.status_code
            response = str(ast.literal_eval(r.text)['result'])[:60].replace(os.linesep, '')

            syslog.syslog(f"Activating WATO change {description}")
            response += self.activate_wato_change(self, comment=f"Activate WATO")

        self.write_status_and_log(
            message=f"{description}: {status_code} {response}")

    def write_status_and_log (self, message, message_short = ''):
        ''' Write a short message to status bar, and the full message to log.
            If a short version of message is inclued, it's used for the status bar.
        '''

        for m in [message, message_short]:
            m = chk.scrub_secret(m)

        if len(message_short) == 0:
            message_short = message[:100]

        syslog.syslog(f'{message}')
        self.status = f'{Chk.fetch_time()} {message_short}'

if __name__=="__main__":
    chk = Chk()
    sys.exit(chk.main())
