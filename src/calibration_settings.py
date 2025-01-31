# https://github.com/pygobject/pgi/blob/master/pgi/overrides/GLib.py


from gi.repository import Gdk, GLib


class CalibrationSetting:
    def __init__(self, settings) -> None:
        self.settings = settings

        self.monitors = []

    def get_settings(self):
        va = self.settings.get_value("calibration")
        self.monitors = []
        for i in range(va.n_children()):
            vd = va.get_child_value(i)
            d = {}
            for j in range(vd.n_children()):
                m = vd.get_child_value(j)
                k = m.get_child_value(0).get_string()
                v = m.get_child_value(1).get_string()
                if k == "compute":
                    v = bool(v)
                elif k == "diagonal":
                    v = float(v)
                elif k == "ppmm":
                    v = int(v)
                d[k] = v
            self.monitors.append(d)
        print("== Monitors")
        print(self.monitors)

    def set_settings(self) -> None:
        display = Gdk.Display.get_default()
        array = GLib.VariantBuilder.new(GLib.VariantType.new("aa{ss}"))

        for monitor in display.get_monitors():
            d_monitor = GLib.VariantBuilder.new(GLib.VariantType.new("a{ss}"))

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "monitor"))
            entry.add_value(GLib.Variant("s", monitor.get_description()))
            d_monitor.add_value(entry.end())

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "compute"))
            entry.add_value(GLib.Variant("s", str(True)))
            d_monitor.add_value(entry.end())

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "diagonal"))
            entry.add_value(GLib.Variant("s", str(26.7)))
            d_monitor.add_value(entry.end())

            entry = GLib.VariantBuilder.new(GLib.VariantType.new("{ss}"))
            entry.add_value(GLib.Variant("s", "ppmm"))
            entry.add_value(GLib.Variant("s", str(4)))
            d_monitor.add_value(entry.end())

            array.add_value(d_monitor.end())
        self.settings.set_value("calibration", array.end())
        print(self.settings.get_value("calibration"))
