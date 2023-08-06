from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.planing.models.sections import Sections, SectionsManager


@JsonResponseWithException()
def Sections_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Sections.objects.
                filter().
                get_range_rows1(
                request=request,
                function=SectionsManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Add(request):
    return JsonResponse(DSResponseAdd(data=Sections.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Update(request):
    return JsonResponse(DSResponseUpdate(data=Sections.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Sections.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Sections.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Info(request):
    return JsonResponse(DSResponse(request=request, data=Sections.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Sections_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Sections.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
