from esphome import pins
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import fan
from esphome.const import (
    CONF_ID
)
from .. import venta_fan_ns, VentaFan

CONF_SWITCH_FANSPEED_PIN = "switch_fanspeed_pin"
CONF_SWITCH_POWER_PIN = "switch_power_pin"
CONF_LED_POWER_PIN = "led_power_pin"
CONF_LED_LOW_PIN = "led_low_pin"
CONF_LED_MID_PIN = "led_mid_pin"
CONF_LED_HIGH_PIN = "led_high_pin"

CONFIG_SCHEMA = fan.FAN_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(VentaFan),
        cv.Required(CONF_SWITCH_FANSPEED_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_SWITCH_POWER_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_LED_POWER_PIN): pins.gpio_input_pin_schema,
        cv.Required(CONF_LED_LOW_PIN): pins.gpio_input_pin_schema,
        cv.Optional(CONF_LED_MID_PIN): pins.gpio_input_pin_schema,
        cv.Required(CONF_LED_HIGH_PIN): pins.gpio_input_pin_schema
    }
).extend(cv.polling_component_schema("1s"))


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await fan.register_fan(var, config)

    switch_fanspeed_pin = await cg.gpio_pin_expression(config[CONF_SWITCH_FANSPEED_PIN])
    cg.add(var.set_switch_fanspeed_pin(switch_fanspeed_pin))

    switch_power_pin = await cg.gpio_pin_expression(config[CONF_SWITCH_POWER_PIN])
    cg.add(var.set_switch_power_pin(switch_power_pin))

    led_power_pin = await cg.gpio_pin_expression(config[CONF_LED_POWER_PIN])
    cg.add(var.set_led_power_pin(led_power_pin))

    led_low_pin = await cg.gpio_pin_expression(config[CONF_LED_LOW_PIN])
    cg.add(var.set_led_low_pin(led_low_pin))

    if led_mid_pin_num := config.get(CONF_LED_MID_PIN):
      led_mid_pin = await cg.gpio_pin_expression(led_mid_pin_num)
      cg.add(var.set_led_mid_pin(led_mid_pin))

    led_high_pin = await cg.gpio_pin_expression(config[CONF_LED_HIGH_PIN])
    cg.add(var.set_led_high_pin(led_high_pin))
