from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse

from kaf_pas.production.models.operations_template import Operations_template, Operations_templateManager


@JsonResponseWithException()
def Operations_template_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Operations_template.objects.
                filter().
                get_range_rows1(
                request=request,
                function=Operations_templateManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Add(request):
    return JsonResponse(DSResponseAdd(data=Operations_template.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Update(request):
    return JsonResponse(DSResponseUpdate(data=Operations_template.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Info(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Operations_template_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Operations_template.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
