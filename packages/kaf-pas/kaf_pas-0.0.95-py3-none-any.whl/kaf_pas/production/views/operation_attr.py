from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.operation_attr import Operation_attr, Operation_attrManager


@JsonResponseWithException()
def Operation_attr_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operation_attr.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operation_attrManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Add(request):
    return JsonResponse(DSResponseAdd(data=Operation_attr.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operation_attr.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operation_attr.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operation_attr.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operation_attr.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_attr_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operation_attr.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
