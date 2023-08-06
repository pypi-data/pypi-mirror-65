from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.operation_section import Operation_section, Operation_sectionManager


@JsonResponseWithException()
def Operation_section_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operation_section.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operation_sectionManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Add(request):
    return JsonResponse(DSResponseAdd(data=Operation_section.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operation_section.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operation_section.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operation_section.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operation_section.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operation_section_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operation_section.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
