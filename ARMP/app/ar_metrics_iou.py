from ARMP.lib.loader import dic, setting
from ARMP.metrics.iou import iou
from ARMP.io.input import nc_in


def AR_IOU(dic, case_name, case_name_ref):

    dir_out = dic['dir_out']

    da_ts = nc_in('occur', 'ts.nc', case_name, dir_out)
    da_ts_ref = nc_in('occur', 'ts.nc', case_name_ref, dir_out)

    iou_result = iou(da1, da2) * 100

    return iou_result



if __name__ == "__main__":

    model = dic['model_list'][1]
    ARDT = dic['ARDT_list'][1]
    ARDT_ref = dic['ARDT_list'][0]
    region = dic['region_list'][0]
    season = dic['season_list'][0]

    case_name = "{}_tag".format('_'.join([model,ARDT,region,season]))
    case_name_ref = "{}_tag".format('_'.join([model,ARDT_ref,region,season]))

    iou_result = AR_IOU(dic, case_name, case_name_ref)

    print('AR concurrence between')
    print(case_name)
    print('and')
    print(case_name_ref)
    print("is {:.0f}%".format(iou_result))
