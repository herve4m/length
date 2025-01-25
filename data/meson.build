#
# freedesktop.org Desktop file
#

desktop_conf = configuration_data()
desktop_conf.set('icon', application_id)
desktop_file = i18n.merge_file(
        input: configure_file(
                        input: 'io.github.herve4m.Length.desktop.in.in',
                       output: '@BASENAME@',
                configuration: desktop_conf
               ),
       output: '@0@.desktop'.format(application_id),
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif


#
# freedesktop.org AppStream MetaInfo file
#

appstream_conf = configuration_data()
appstream_conf.set('application_id', application_id)
appstream_conf.set('version', meson.project_version())
appstream_file = i18n.merge_file(
        input: configure_file(
                        input: 'io.github.herve4m.Length.metainfo.xml.in.in',
                       output: '@BASENAME@',
                configuration: appstream_conf
               ),
       output: '@0@.metainfo.xml'.format(application_id),
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
  args: ['validate', '--no-net', '--explain', appstream_file])


#
# Gio Settings schema file
#

schema_conf = configuration_data()
schema_conf.set('application_schema_path', application_schema_path)
schema_conf.set('application_id', application_id)
configure_file(
          input: 'io.github.herve4m.Length.gschema.xml.in',
         output: '@0@.gschema.xml'.format(application_id),
  configuration: schema_conf,
    install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file', compile_schemas,
  args: ['--strict', '--dry-run', meson.current_source_dir()])


#
# D-Bus service file
#

service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
service_conf.set('application_id', application_id)
configure_file(
  input: 'io.github.herve4m.Length.service.in',
  output: '@0@.service'.format(application_id),
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)


#
# GNOME resources
#

gnome = import('gnome')

gnome.compile_resources('length', 'length.gresource.xml',
  gresource_bundle: true,
           install: true,
       install_dir: get_option('prefix') / get_option('datadir') / meson.project_name()
)

subdir('icons')
