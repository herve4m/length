pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'length'

python = import('python')

conf = configuration_data()
conf.set('APPLICATION_ID', application_id)
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
          input: 'length.in',
         output: 'length',
  configuration: conf,
        install: true,
    install_dir: get_option('bindir'),
   install_mode: 'r-xr-xr-x'
)

length_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'unit_mng.py',
  'unit_cm.py',
  'unit_inch.py',
  'unit_pct.py',
  'unit_px.py',
  'unit.py',
  'draw_context.py',
  'offset.py',
  'opacity.py',
  'orientation.py',
  'pointer_tracking.py',
  'settings.py',
  'preferences.py'
]

install_data(length_sources, install_dir: moduledir)
