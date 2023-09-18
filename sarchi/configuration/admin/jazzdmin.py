# import settings
from django.conf import settings

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    'site_title': 'UJ Blockchain Admin',
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_header': 'UJ Blockchain',
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_brand': 'UJ Blockchain',
    # Logo to use for your site, must be present in static files, used for brand on top left
    'site_logo': 'images/logo.png',
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    'login_logo': 'images/logo.png',
    # Logo to use for login form in dark themes (defaults to login_logo)
    'login_logo_dark': 'images/logo.png',
    # CSS classes that are applied to the logo above
    'site_logo_classes': 'img',
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    'site_icon': 'favicon/favicon.ico',
    # Welcome text on the login screen
    'welcome_sign': 'Welcome to UJ Blockchain',
    # Copyright on the footer
    'copyright': 'UJ Blockchain',
    # The model admin to search from the search bar, search bar omitted if excluded
    #'search_model': ['...'],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    'user_avatar': None,
    ############################################################
    # Top Menu #
    ############################################################
    # Links to put along the top menu
    'topmenu_links': [
        # Url that gets reversed (Permissions can be added)
        {'name': 'Home', 'url': f'/{settings.ADMIN_PATH}', 'permissions': ['auth.view_user']},
        # external url that opens in a new window (Permissions can be added)
        {'name': 'View Site', 'url': '/', 'new_window': False},
        {'model': 'auth.User'},
        # {'model': '...'},
        # {'model': '...'},
    ],
    ######################################################
    # User Menu #
    ######################################################
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    'usermenu_links': [
        {'name': 'View Site', 'url': '/', 'icon': 'fas fa-server', 'new_window': False},
    ],
    #####################################################
    # Side Menu #
    #####################################################
    # Whether to display the side menu
    'show_sidebar': True,
    # Whether to aut expand the menu
    'navigation_expanded': True,
    # Hide these apps when generating side menu e.g (auth)
    'hide_apps': [],
    # Hide these models when generating side menu (e.g auth.user)
    'hide_models': [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # 'order_with_respect_to': ['auth', '...', '...'],
    # Custom links to append to app groups, keyed on app name
    'custom_links': {},
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.user': 'fas fa-user',
        'auth.Group': 'fas fa-users',
        'axes.accessattempt': 'fas fa-door-open',
        'axes.accessfailurelog': 'fas fa-bomb',
        'axes.accesslog': 'fas fa-fingerprint',
        'reversion.revision': 'fas fa-feather-alt',
        'reversion.version': 'fas fa-code-branch',
        'blog.blog': 'fas fa-blog',
        'bootcamps.bootcampfirst': 'fas fa-chalkboard-teacher',
        'contact.usercontact': 'fas fa-id-badge',
        'facilitators.facilitators': 'fas fa-user-check',
        'newsletters.newsletteremail': 'fas fa-envelope-open-text',
        'newsletters.sendnewsletteremails': 'fas fa-paper-plane',
        'partners.partners': 'fas fa-handshake',
        'projects.projects': 'fas fa-project-diagram',
        'repository.repoinfo': 'fas fa-code',
    },
    # Icons that are used when one is not manually specified
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    ######################################################
    # Related Modal #
    ######################################################
    # Use modals instead of popups
    'related_modal_active': False,
    ######################################################
    # UI Tweaks #
    ######################################################
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    'custom_css': '/css/jazzmin.css',
    'custom_js': None,
    # Whether to show the UI customized on the sidebar
    'show_ui_builder': False,
    ########################################################
    # Change view #
    ########################################################
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    'changeform_format': 'horizontal_tabs',
    # override change forms on a per modeladmin basis
    'changeform_format_overrides': {
        'auth.user': 'collapsible',
        'auth.group': 'vertical_tabs',
    },
    # Add a language dropdown into the admin
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
