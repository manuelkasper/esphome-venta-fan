# Venta LW fan control ESPHome component

This is an ESPHome component designed to work with the <a href="https://github.com/Alex9779/Venta-LW-Controller/">Venta LW Controller PCB</a> by @Alex9779. The example supplied in that repository uses a custom component, which is no longer supported in recent ESPHome versions. Although workarounds are possible, I decided to create a "proper" component.

It registers as a fan with two/three speeds in Home Assistant, and manual changes (on/off, speed) on the device are also reflected in HA. The error status LED is reflected as a binary sensor. The component supports airwashers with two (LW15) or three speeds (LW45 etc.). Depending on whether or not `led_mid_pin` is configured, it will present as a fan with two or three speeds to HA.

<img width="500" alt="Screenshot 2025-03-12 at 16 50 14" src="https://github.com/user-attachments/assets/97cb4654-792e-4a9c-9fc2-72eee1888f2f" />

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
    # led_mid_pin is optional; if not specified, a two-speed model is assumed
    led_mid_pin: 21
    led_high_pin: 22
```
