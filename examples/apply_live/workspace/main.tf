resource "time_sleep" "wait_1" {
  create_duration = "5s"
}

resource "time_sleep" "wait_2" {
  create_duration = "5s"

  depends_on = [time_sleep.wait_1]
}

resource "time_sleep" "wait_3" {
  create_duration = "5s"

  depends_on = [time_sleep.wait_2]
}

resource "time_sleep" "wait_4" {
  create_duration = "5s"

  depends_on = [time_sleep.wait_3]
}
