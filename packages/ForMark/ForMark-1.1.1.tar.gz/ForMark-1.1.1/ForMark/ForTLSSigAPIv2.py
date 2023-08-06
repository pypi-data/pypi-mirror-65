import TLSSigAPIv2


def get_sig(name, sdkappid, key):
    api = TLSSigAPIv2.TLSSigAPIv2(sdkappid, key)
    sig = api.gen_sig(name)
    return sig
