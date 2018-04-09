QUEUES = {
    "sthlm": "Bostadskön"
}  # todo: fetch other queues?

BUILDING_TYPES = {
    "nyproduktion": "Endast nyproduktion",
    "ej_nyproduktion": "Utan nyproduktion"
}

YEARS = range(2000, 2019)

QUEUE_TIME_GROUPS = [
  "0-2",
  "2-4",
  "4-6",
  "6-8",
  "8-10",
  "10-12",
  "12-14",
  "14-16",
  "16-18",
  "18-20",
  "20 <",
]


def get_raw_list_file_path(queue, year, building_type, group):
    return 'data/%s/%s/%s/%s.html' % (queue, year, building_type, group)
