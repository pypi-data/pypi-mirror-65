from django.template.loader import render_to_string
from django.conf import settings


CAMPOS_ENCABEZADOS = (
    ("clave_proveedor", "str"),
    ("no_siniestro", "str"),
    ("orden_pago", "str"),
	("cristales_deducible", "decimal"),
	("codigo_nags", "str"),
	("costo_honorarios", "decimal"),
	("costo_gruas", "decimal"),
	("costo_asistencia", "decimal"),
	("num_valuacion_inicial", "str"),
	("costo_reparaciones", "decimal"),
	("pase_medico", "str"),
	("costo_gmedicos", "decimal"),
)


def generar_addenda(diccionario):
    return render_to_string("cfdi/addendas/multiasistencia.xml", diccionario)
