from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.operations_template_material import Operations_template_material, Operations_template_materialManager


@JsonResponseWithException()
def Operations_template_material_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operations_template_material.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operations_template_materialManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Add(request):
    return JsonResponse(DSResponseAdd(data=Operations_template_material.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operations_template_material.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_material.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_material.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_material.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_material_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_material.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
