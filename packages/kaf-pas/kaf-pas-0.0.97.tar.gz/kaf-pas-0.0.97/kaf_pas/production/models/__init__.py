from isc_common.number import StrToInt
from kaf_pas.system.models.contants import Contants

progress_deleted = 'Прогресс удален.'
p_id = StrToInt(Contants.objects.get(code='audo_top_level').value)
