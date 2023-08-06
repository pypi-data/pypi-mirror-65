import time


class PyProfTool:

    def __init__(self, description):
        self.enabled = True
        self.prof_points = {}
        self.description = description

    def start_point(self, name):
        if not self.enabled:
            return

        if name not in self.prof_points:
            self.prof_points[name] = {}
            self.prof_points[name]["times"] = 0
            self.prof_points[name]["time_acc"] = 0
            self.prof_points[name]["running"] = False
            self.prof_points[name]["start_ts"] = 0
            self.prof_points[name]["end_ts"] = 0
            self.prof_points[name]["time_max"] = 0
            self.prof_points[name]["time_min"] = 0
            self.prof_points[name]["time_mean"] = 0

        if self.prof_points[name]["running"]:
            raise TypeError('Não foi encontrado um end_point para o script "' + name +
                            '" ou não está corretamente posicionado na iteração')

        self.prof_points[name]["running"] = True
        self.prof_points[name]["start_ts"] = time.time()
        return

    def end_point(self, name):
        ts = time.time()

        if not self.enabled:
            return

        if name not in self.prof_points:
            raise TypeError('Não foi encontrado o script "' + name + '". Pode estar faltando um start_point.')

        if not self.prof_points[name]["running"]:
            raise TypeError('Não foi encontrado um start_point para o script "' + name +
                            '" ou não está corretamente posicionado na iteração')

        self.prof_points[name]["end_ts"] = ts
        delta_time = ts - self.prof_points[name]["start_ts"]
        self.prof_points[name]["time_acc"] = self.prof_points[name]["time_acc"] + delta_time
        if self.prof_points[name]["time_max"] < delta_time:
            self.prof_points[name]["time_max"] = delta_time

        if self.prof_points[name]["time_min"] == 0:
            self.prof_points[name]["time_min"] = delta_time
        else:
            if self.prof_points[name]["time_min"] > delta_time:
                self.prof_points[name]["time_min"] = delta_time

        times = self.prof_points[name]["times"] + 1
        self.prof_points[name]["times"] = times
        self.prof_points[name]["time_mean"] = self.prof_points[name]["time_acc"] / times

        self.prof_points[name]["running"] = False

    def show(self):
        print("\n" + self.description + ":")
        print("{0:20}{1:20}{2:20}{3:20}{4:20}{5:20}{6:20}"
              .format("Point", "|   Mean Time (ms)", "|   Mean Freq(cy/s)", "|   Min Time(ms)", "|   Max Time(ms)",
                      "|   Num Exec", "|   Total Time(ms)"))
        print("{0:20}{1:20}{2:20}{3:20}{4:20}{5:20}{6:20}"
              .format("----------------", "|   --------------", "|   --------------", "|   --------------",
                      "|   --------------", "|   --------------", "|   --------------"))
        for point in self.prof_points:
            print("{0:<20}{1:<20}{2:<20}{3:<20}{4:<20}{5:<20}{6:<20}"
                  .format(point,
                          "|   " + format(self.prof_points[point]["time_acc"]*1000 /
                                          self.prof_points[point]["times"], ".4f"),
                          "|   " + format(self.prof_points[point]["times"] /
                                          self.prof_points[point]["time_acc"], ".1f"),
                          "|   " + format(self.prof_points[point]["time_min"]*1000, ".4f"),
                          "|   " + format(self.prof_points[point]["time_max"]*1000, ".4f"),
                          "|   " + format(self.prof_points[point]["times"]),
                          "|   " + format(self.prof_points[point]["time_acc"]*1000, ".3f")))

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
