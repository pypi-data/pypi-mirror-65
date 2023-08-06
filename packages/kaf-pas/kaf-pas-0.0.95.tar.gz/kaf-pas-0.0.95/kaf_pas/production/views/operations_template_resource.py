from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.operations_template_resource import Operations_template_resource, Operations_template_resourceManager


@JsonResponseWithException()
def Operations_template_resource_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operations_template_resource.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operations_template_resourceManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Add(request):
    return JsonResponse(DSResponseAdd(data=Operations_template_resource.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operations_template_resource.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_resource.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_resource.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_resource.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_resource_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template_resource.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
