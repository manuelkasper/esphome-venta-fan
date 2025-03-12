import esphome.codegen as cg
from esphome.components import fan

venta_fan_ns = cg.esphome_ns.namespace('venta_fan')
VentaFan = venta_fan_ns.class_("VentaFan", cg.PollingComponent, fan.Fan)
