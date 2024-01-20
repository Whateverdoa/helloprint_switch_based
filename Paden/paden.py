from pathlib import Path

#prod
logpad = Path(r"C:\Users\Bgsystem\PycharmProjects_send_SWITCH_helloprint_cerm\pythonProject\logs\helloprint.log")
HP_CERM_CONN = Path(r"E:\SWITCH\HP_CERM_CONN")  # hier haalt het op

#test
logpad_test = Path(r"D:\programs\VS_CODE\hp\helloprint_switch_based\logs\helloprint_test.log")
HP_CERM_CONN_TEST = Path(
    r"D:\programs\VS_CODE\hp\HP_CERM_CONN_TEST"
)  # hier haalt het op in test omgevin

#pad nodig op workstation!
DOWNLOAD_PAD_VILA_TO_ESKO = Path(
    r"\\l02-app04.ad.optimumgroup.nl\Esko\Vila-to-Esko\resellers"
)  # hier gaat de zip naartoe

hp_cerm_conv_pad = Path(
    r"C:\Users\Bgsystem\PycharmProjects_send_SWITCH_helloprint_cerm\pythonProject\testfile\cerm_helloprint_conversions"
)
# dit is temp voor test

# test hp_cerm_conv_pad = Path(r'C:\Users\Bgsystem\PycharmProjects_send_SWITCH_helloprint_cerm\pythonProject\testfile\cerm_helloprint_conversions')
hp_cerm_conversion_test=Path(r'D:\programs\VS_CODE\hp\testfile\cerm_helloprint_conversions')