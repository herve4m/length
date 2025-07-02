project('length',
          version: '0.8.1',
    meson_version: '>= 1.1.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

if get_option('development')
  application_id = 'io.github.herve4m.Length.Devel'
  application_schema_path = '/io/github/herve4m/Length/'
else
  application_id = 'io.github.herve4m.Length'
  application_schema_path = '/io/github/herve4m/Length/Devel/'
endif

subdir('data')
subdir('src')
subdir('help')
subdir('po')

gnome.post_install(
     glib_compile_schemas: true,
    gtk_update_icon_cache: true,
  update_desktop_database: true,
)
