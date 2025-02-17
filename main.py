import ldclient
import os
from nicegui import app, ui, client
from ldclient import Context
from ldclient.config import Config
from nicegui import Client

### Set SDK key in environment variable or hard code below
sdk_key = 'sdk-12345'
# sdk_key = os.getenv("LDKEY") 
login_flag = "worldDomination"
missile_flag = "missile"

def country_from_ip(ip):
    return 'United States'

# @ui.refreshable
@ui.page('/')
def main_page(flag_change=None):

    with ui.header(elevated=True) as header:
        ui.label('Investments').classes('text-h6')
        ui.space()
        user = {}
        feature_flag_key = 'worldDomination'
        context = Context.builder('username') \
            .kind('user') \
            .name(user) \
            .set('country', 'United States') \
            .build()
        if not app.storage.user.get('data',{}).get('authed'):
            if ldclient.get().variation(login_flag, context, False):
                ui.input(label='user', placeholder='user@user.com',
                    validation={'Input too long': lambda value: len(value) < 100}).bind_value_to(user, 'name')
                def open_other_page():
                    user['authed'] = True
                    app.storage.user.update(data=user)
                    ui.navigate.to('/home')
                ui.button('Login', on_click=open_other_page)
        else:
            username = app.storage.user.get('data', {}).get('name', {})
            ui.label('Welcome, {}'.format(username))
            def logout():
                app.storage.user.update(data={})
                ui.navigate.to('/')
            
            ui.button('Logout', on_click=logout)

    with ui.row().classes('w-full justify-center'):
        with ui.card().classes('max-w-3xl w-full p-8'):
            ui.image('https://picsum.photos/800/300').classes('w-full')
            ui.label('Totally not a missile launcher').classes('text-h4 text-center')
            if app.storage.user.get('data',{}).get('authed'):
                with ui.row().classes('w-full justify-center'):
                    ui.button('Check Portfolio', color='Primary', on_click=lambda: ui.notify('You have no money :/'))

    with ui.footer().classes('bg-grey-2'):
        ui.label('© 2024 My Company').classes('text-grey-6')

@ui.page('/home')
def user_home():
    if not app.storage.user.get('data',{}).get('authed'):
        ui.navigate.to('/')
    username = app.storage.user.get('data', {}).get('name', '')
    
    client_ip = str(Client.ip)
    country = country_from_ip(client_ip)
    context = Context.builder(username) \
                .kind('user') \
                .name(username) \
                .set('country', country) \
                .build()
    with ui.header(elevated=True):
        ui.label('Investments').classes('text-h6')
        ui.space()
        ui.label('Welcome, {}'.format(username))
        app.storage.user.update(authed=True)
        def logout():
            app.storage.user.update(data={})
            ui.navigate.to('/')
        
        ui.button('Logout', on_click=logout)

    if ldclient.get().variation(missile_flag, context, False):
         with ui.row().classes('w-full justify-center'):
            with ui.card().classes('max-w-3xl w-full p-8'):
                ui.image('static/missile.png').classes('w-160')
                ui.label('Missile Launcher').classes('text-h4 text-center')
                ui.label('Launch the missile!').classes('text-center')
                with ui.row().classes('w-full justify-center'):
                    ui.button('Launch', color='Red', on_click=lambda: ui.notify('LAUNCHING THE MISSILE!'))
    else:
        ui.navigate.to('/')

if __name__ == "__main__":
    ldclient.set_config(Config(sdk_key))
    def refresh_page(flag_change=None):
        for client in Client.instances.values():
            with client:
                ui.navigate.reload()
    context = Context.builder('username').kind('user').name('').build()
    listener = ldclient.get().flag_tracker.add_flag_value_change_listener(login_flag,context,refresh_page)
    ui.run(storage_secret="this-is-a-secret", reload=False)