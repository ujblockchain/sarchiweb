# import settings
from django.conf import settings

JAZZMIN_SETTINGS = {  # type: ignore
    'site_title': 'UJ Blockchain Admin',
    'site_header': 'UJ Blockchain',
    'site_brand': 'UJ Blockchain',
    'site_logo': 'img/logo.png',
    'login_logo': 'img/logo.png',
    'login_logo_dark': 'img/logo.png',
    'site_logo_classes': 'img',
    'site_icon': 'favicon/favicon.ico',
    'welcome_sign': 'Welcome to UJ Blockchain',
    'copyright': 'UJ Blockchain',
    'user_avatar': None,
    
    # links to put along the top menu
    'topmenu_links': [
        {
            'name': 'Home',
            'url': f'/{settings.ADMIN_PATH}',
            'permissions': ['auth.view_user']
        },
        {
            'name': 'View Site',
            'url': '/',
            'new_window': False
        },
        {
            'model': 'auth.User'
        },
    ],
    
    # additional links to include in the user menu on the top right
    'usermenu_links': [
        {
            'name': 'View Site',
            'url': '/',
            'icon': 'fas fa-server',
            'new_window': False
        },
        {
            'name': 'User Contacts',
            'url': '/contacts',
            'icon': 'fas fa-sliders-h',
            'new_window': False
        },
    ],
    
    # whether to display the side menu
    'show_sidebar': True,
    # whether to aut expand the menu
    'navigation_expanded': True,
    
    'hide_apps': [],
    'hide_models': [],
    'custom_links': {},
    'icons': {
        # third party
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'axes.accessattempt': 'fas fa-door-open',
        'axes.accessfailurelog': 'fas fa-bomb',
        'axes.accesslog': 'fas fa-fingerprint',
        # project apps
        'contact.usercontact': 'fas fa-id-badge',
    },
    # icons that are used when one is not manually specified
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    
    # use modals instead of popups
    'related_modal_active': False,
    # relative paths to custom css/js scripts
    'custom_css': '/css/jazzmin.css',
    'custom_js': None,
    'show_ui_builder': False,
    'changeform_format': 'horizontal_tabs',
    # override change forms on a per modeladmin basis
    'changeform_format_overrides': {
        'auth.user': 'collapsible',
        'auth.group': 'vertical_tabs',
    },
    # add a language dropdown into the admin
    'language_chooser': False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': False,
    'body_small_text': False,
    'brand_small_text': False,
    'brand_colour': False,
    'accent': 'accent-primary',
    'navbar': 'navbar-dark',
    'no_navbar_border': False,
    'navbar_fixed': False,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': False,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': False,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': False,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': False,
    'theme': 'solar',
    'dark_mode_theme': 'darkly',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-outline-info',
        'warning': 'btn-outline-warning',
        'danger': 'btn-outline-danger',
        'success': 'btn-outline-success',
    },
    'actions_sticky_top': False,
}
