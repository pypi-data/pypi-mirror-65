from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.production.models.resource import Resource, ResourceManager


@JsonResponseWithException()
def Resource_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Resource.objects.
                filter().
                get_range_rows1(
                request=request,
                function=ResourceManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Resource_Add(request):
    return JsonResponse(DSResponseAdd(data=Resource.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Resource_Update(request):
    return JsonResponse(DSResponseUpdate(data=Resource.objects.updateFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Resource_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Resource.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Resource_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Resource.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Resource_Info(request):
    return JsonResponse(DSResponse(request=request, data=Resource.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)
