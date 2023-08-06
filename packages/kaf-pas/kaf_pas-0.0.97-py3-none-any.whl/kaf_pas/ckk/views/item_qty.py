from isc_common.http.DSResponse import DSResponseUpdate, DSResponseAdd, DSResponse, JsonResponseWithException
from isc_common.http.RPCResponse import RPCResponseConstant
from isc_common.http.response import JsonResponse
from kaf_pas.ckk.models.item_qty import Item_qty, Item_qtyManager


@JsonResponseWithException()
def Item_qty_Fetch(request):
    return JsonResponse(
        DSResponse(
            request=request,
            data=Item_qty.objects.
                select_related().
                get_range_rows1(
                request=request,
                function=Item_qtyManager.getRecord
            ),
            status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Add(request):
    return JsonResponse(DSResponseAdd(data=Item_qty.objects.createFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Update(request):
    return JsonResponse(DSResponseUpdate(data=Item_qty.objects.updateFromRequest(request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Remove(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty.objects.deleteFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Lookup(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty.objects.lookupFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Info(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty.objects.get_queryset().get_info(request=request), status=RPCResponseConstant.statusSuccess).response)


@JsonResponseWithException()
def Item_qty_Copy(request):
    return JsonResponse(DSResponse(request=request, data=Item_qty.objects.copyFromRequest(request=request), status=RPCResponseConstant.statusSuccess).response)
