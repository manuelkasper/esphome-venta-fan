#include "venta_fan.h"
#include "esphome/core/log.h"

namespace esphome {
namespace venta_fan {

static const int SWITCH_DELAY = 50;
static const int SWITCH_INTERVAL = 100;
static const int SWITCH_MAX_TRIES = 10;

static const char *TAG = "venta_fan.fan";

void VentaFan::setup() {
  this->switch_fanspeed_pin_->setup();
  this->switch_power_pin_->setup();
  this->led_power_pin_->setup();
  this->led_low_pin_->setup();
  this->led_mid_pin_->setup();
  this->led_high_pin_->setup();
}

fan::FanTraits VentaFan::get_traits() {
  return fan::FanTraits(false, true, false, 3);
}

void VentaFan::update() {
  bool updated = false;
  bool error = false;

  bool cur_state = !this->led_power_pin_->digital_read();
  if (this->state != cur_state) {
    this->state = cur_state;
    updated = true;
  }

  int cur_speed = 0;
  if (!this->led_low_pin_->digital_read()) {
    cur_speed = 1;
  } else if (!this->led_mid_pin_->digital_read()) {
    cur_speed = 2;
  } else if (!this->led_high_pin_->digital_read()) {
    cur_speed = 3;
  } else {
    if (cur_state) {
      // On but no speed lit means error must be lit
      error = true;
    }
  }

  if (this->speed != cur_speed) {
    this->speed = cur_speed;
    updated = true;
  }

  if (updated) {
    this->publish_state();
  }

  if (this->error_status_sensor_ != nullptr) {
    if (this->error_status_sensor_->state != error || !this->error_status_sensor_->has_state()) {
      this->error_status_sensor_->publish_state(error);
    }
  }
}

void VentaFan::control(const fan::FanCall &call) {
  if (call.get_state().has_value()) {
    this->state = *call.get_state();
  }
  if (call.get_speed().has_value()) {
    this->speed = *call.get_speed();
  }

  this->write_state_();
  this->publish_state();
}

void VentaFan::write_state_() {
  if (!this->state || this->speed == 0) {
    // Turn power off
    if (!this->led_power_pin_->digital_read()) {
      click_switch_(this->switch_power_pin_);
    }
    return;
  }

  // Turn power on if necessary
  if (this->led_power_pin_->digital_read()) {
    click_switch_(this->switch_power_pin_);
  }

  GPIOPin *led_pin;
  switch (this->speed) {
  case 1:
    led_pin = this->led_low_pin_;
    break;
  case 2:
    led_pin = this->led_mid_pin_;
    break;
  case 3:
    led_pin = this->led_high_pin_;
    break;
  default:
    status_set_error("Invalid speed setting");
    return;
  }

  // Toggle fanspeed until we reach desired speed
  int tries = 0;
  while (led_pin->digital_read()) { // pin readings are inverted!
    click_switch_(this->switch_fanspeed_pin_);
    tries++;
    if (is_internal_error_() || tries > SWITCH_MAX_TRIES) {
      status_set_error("Internal error or too many tries to reach target speed setting");
      return;
    }
  }

  status_clear_error();
}

void VentaFan::dump_config() {
  LOG_FAN("", "Venta Fan:", this);
  LOG_PIN("  Switch Fanspeed Pin: ", this->switch_fanspeed_pin_);
  LOG_PIN("  Switch Power Pin: ", this->switch_power_pin_);
  LOG_PIN("  LED Power Pin: ", this->led_power_pin_);
  LOG_PIN("  LED Low Pin: ", this->led_low_pin_);
  LOG_PIN("  LED Mid Pin: ", this->led_mid_pin_);
  LOG_PIN("  LED High Pin: ", this->led_high_pin_);
}

void VentaFan::click_switch_(GPIOPin *output) {
  output->digital_write(true);
  delay(SWITCH_DELAY);
  output->digital_write(false);
  delay(SWITCH_INTERVAL);
}

bool VentaFan::is_internal_error_() {
  // LED states are inverted
  return (!this->led_power_pin_->digital_read() && this->led_low_pin_->digital_read() && 
          this->led_mid_pin_->digital_read() && this->led_high_pin_->digital_read());
}

}  // namespace venta_fan
}  // namespace esphome
