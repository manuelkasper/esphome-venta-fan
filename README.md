This is an ESPHome component designed to work with the <a href="https://github.com/Alex9779/Venta-LW-Controller/">Venta LW Controller PCB</a> by @Alex9779. The example supplied in that repository uses a custom component, which is no longer supported in recent ESPHome versions. Although workarounds are possible, I decided to create a "proper" component.

```yaml
# example configuration:

external_components:
  - source:
      type: git
      url: https://github.com/manuelkasper/esphome-venta-fan
    components: [ venta_fan ]

binary_sensor:
  - platform: venta_fan
    error_status:
      name: "Error"

fan:
  - platform: venta_fan
    name: Fan
    switch_fanspeed_pin: 16
    switch_power_pin: 17
    led_power_pin: 18
    led_low_pin: 19
    led_mid_pin: 21
    led_high_pin: 22
```
