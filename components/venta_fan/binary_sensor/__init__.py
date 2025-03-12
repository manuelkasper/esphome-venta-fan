import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_PROBLEM,
)

from .. import venta_fan_ns, VentaFan

CONF_VENTA_FAN_ID = "venta_fan_id"
CONF_ERROR_STATUS = "error_status"

VentaFanBinarySensor = venta_fan_ns.class_(
    "VentaFanBinaryComponent", cg.Component
)


CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(VentaFanBinarySensor),
        cv.GenerateID(CONF_VENTA_FAN_ID): cv.use_id(VentaFan),
        cv.Optional(CONF_ERROR_STATUS): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_PROBLEM,
        ),
    }
)


async def to_code(config):
    venta_fan = await cg.get_variable(config[CONF_VENTA_FAN_ID])
    bin_component = cg.new_Pvariable(config[CONF_ID], venta_fan)
    await cg.register_component(bin_component, config)

    if error_status_sensor := config.get(CONF_ERROR_STATUS):
      sensor = await binary_sensor.new_binary_sensor(error_status_sensor)
      cg.add(venta_fan.set_error_status_sensor(sensor))
