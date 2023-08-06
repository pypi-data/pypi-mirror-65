from django.db import transaction

from isc_common.http.DSRequest import DSRequest
from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.operation_material import Operation_material
from kaf_pas.production.models.operation_resources import Operation_resources
from kaf_pas.production.models.operations_item import Operations_item
from kaf_pas.production.models.operations_template_detail import Operations_template_detail, Operations_template_detailManager
from kaf_pas.production.models.operations_template_material import Operations_template_material
from kaf_pas.production.models.operations_template_resource import Operations_template_resource


@JsonResponseWithException()
def Operations_template_detail_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operations_template_detail.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operations_template_detailManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Add(request):
    return JsonResponse(DSResponseAdd(data=Operations_template_detail.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operations_template_detail.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_detail.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_detail.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_detail.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_detail.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_detail_CopyOpers(request):
    _request = DSRequest(request=request)
    source = _request.json.get('source')
    destination = _request.json.get('destination')

    if source and destination:
        srecords = source.get('records')
        source_name = source.get('source_name')
        drecord = destination.get('record')

        if isinstance(srecords, list) and isinstance(drecord, dict):
            with transaction.atomic():
                for srecord in srecords:
                    if source_name == 'templates':
                        old_operations_item = Operations_template_detail.objects.get(id=srecord.get('id'))
                    else:
                        old_operations_item = Operations_item.objects.get(id=srecord.get('id'))

                    operations_template, created = Operations_template_detail.objects.get_or_create(
                        operation=old_operations_item.operation,
                        template_id=drecord.get('id'),
                        defaults=dict(
                            ed_izm=old_operations_item.ed_izm,
                            qty=old_operations_item.qty,
                            num=old_operations_item.num,
                            description=old_operations_item.description,
                        ))

                    if created:
                        if source_name == 'templates':
                            for operation_resources in Operations_template_resource.objects.filter(template=old_operations_item):
                                Operations_template_resource.objects.get_or_create(
                                    template=operations_template,
                                    resource=operation_resources.resource,
                                    location=operation_resources.location
                                )
                        else:
                            for operation_resources in Operation_resources.objects.filter(operationitem=old_operations_item):
                                Operations_template_resource.objects.get_or_create(
                                    template=operations_template,
                                    resource=operation_resources.resource,
                                    location=operation_resources.location
                                )

                        if source_name == 'templates':
                            for operation_material in Operations_template_material.objects.filter(template=old_operations_item):
                                Operations_template_material.objects.get_or_create(
                                    template=operations_template,
                                    material=operation_material.material,
                                    material_askon=operation_material.material_askon,
                                    edizm=operation_material.edizm,
                                    qty=operation_material.qty,
                                )
                        else:
                            for operation_material in Operation_material.objects.filter(operationitem=old_operations_item):
                                Operations_template_material.objects.get_or_create(
                                    template=operations_template,
                                    material=operation_material.material,
                                    material_askon=operation_material.material_askon,
                                    ed_izm=operation_material.ed_izm,
                                    qty=operation_material.qty,
                                )

        return JsonResponse(DSResponse(request=request, status=RPCResponseConstant.statusSuccess).response)
    else:
        raise Exception(f'Копирование не выполнено.')
